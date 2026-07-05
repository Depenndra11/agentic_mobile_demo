from typing import Any, Optional, TypedDict

from langgraph.graph import StateGraph, END

from agents.planner import Planner
from agents.ui_inspector import UIInspector
from agents.page_agent import PageAgent
from agents.executor import Executor

from tests.conftest import get_driver
from utils.logger import get_logger

logger = get_logger(__name__)


# -------------------------------------------------
# Workflow State
#
# Each node both reports whether it completed AND
# carries forward the data the next node needs, so
# steps aren't just side-effecting through disk I/O.
# -------------------------------------------------

class AgentState(TypedDict, total=False):

    planner_done: bool
    inspector_done: bool
    page_done: bool
    executor_done: bool

    testcases: Optional[list]
    screen_xml_path: Optional[str]

    error: Optional[str]


# -------------------------------------------------
# Planner Node
# -------------------------------------------------

def planner_node(state: AgentState) -> AgentState:

    logger.info("Running Planner agent")

    testcases = Planner().run()

    state["planner_done"] = True
    state["testcases"] = testcases

    return state


# -------------------------------------------------
# UI Inspector Node
# -------------------------------------------------

def inspector_node(state: AgentState) -> AgentState:

    logger.info("Running UI Inspector agent")

    driver = get_driver()

    try:
        path = UIInspector(driver).capture_page_source()
    finally:
        driver.quit()

    state["inspector_done"] = True
    state["screen_xml_path"] = str(path)

    return state


# -------------------------------------------------
# Page Node
# -------------------------------------------------

def page_node(state: AgentState) -> AgentState:

    logger.info("Running Page agent")

    PageAgent().run()

    state["page_done"] = True

    return state


# -------------------------------------------------
# Executor Node
# -------------------------------------------------

def executor_node(state: AgentState) -> AgentState:

    logger.info("Running Executor agent")

    Executor().run()

    state["executor_done"] = True

    return state


# -------------------------------------------------
# Error Handling
#
# If any node above raises, LangGraph propagates the
# exception by default. Wrapping each node lets us
# record which step failed instead of a bare traceback
# with no indication of pipeline progress.
# -------------------------------------------------

def _guarded(node_fn, name: str):

    def wrapper(state: AgentState) -> AgentState:
        try:
            return node_fn(state)
        except Exception as exc:
            logger.error("%s agent failed: %s", name, exc)
            state["error"] = f"{name} failed: {exc}"
            raise

    return wrapper


# -------------------------------------------------
# Build Graph
# -------------------------------------------------

builder = StateGraph(AgentState)

builder.add_node("planner", _guarded(planner_node, "Planner"))
builder.add_node("inspector", _guarded(inspector_node, "UI Inspector"))
builder.add_node("page", _guarded(page_node, "Page"))
builder.add_node("executor", _guarded(executor_node, "Executor"))

builder.set_entry_point("planner")

builder.add_edge("planner", "inspector")
builder.add_edge("inspector", "page")
builder.add_edge("page", "executor")
builder.add_edge("executor", END)

workflow = builder.compile()
