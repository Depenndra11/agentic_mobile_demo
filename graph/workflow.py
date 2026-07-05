from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents.planner import Planner
from agents.ui_inspector import UIInspector
from agents.page_agent import PageAgent
from agents.executor import Executor

from tests.conftest import get_driver


# -------------------------------------------------
# Workflow State
# -------------------------------------------------

class AgentState(TypedDict):

    planner: bool
    inspector: bool
    locator: bool
    page: bool
    executor: bool


# -------------------------------------------------
# Planner Node
# -------------------------------------------------

def planner_node(state):

    print("\nPlanner Agent\n")

    Planner().run()

    state["planner"] = True

    return state


# -------------------------------------------------
# UI Inspector
# -------------------------------------------------

def inspector_node(state):

    print("\nUI Inspector Agent\n")

    driver = get_driver()

    UIInspector(driver).capture_page_source()

    driver.quit()

    state["inspector"] = True

    return state


# -------------------------------------------------
# Locator Agent
# -------------------------------------------------

def locator_node(state):

    print("\nLocator Agent\n")

    LocatorAgent().run()

    state["locator"] = True

    return state


# -------------------------------------------------
# Page Agent
# -------------------------------------------------

def page_node(state):

    print("\nPage Agent\n")

    PageAgent().run()

    state["page"] = True

    return state


# -------------------------------------------------
# Executor
# -------------------------------------------------

def executor_node(state):

    print("\nExecutor Agent\n")

    Executor().run()

    state["executor"] = True

    return state


# -------------------------------------------------
# Build Graph
# -------------------------------------------------

builder = StateGraph(AgentState)

builder.add_node("planner", planner_node)

builder.add_node("inspector", inspector_node)



builder.add_node("page", page_node)

builder.add_node("executor", executor_node)

builder.set_entry_point("planner")

builder.add_edge("planner", "inspector")

builder.add_edge("inspector", "page")

builder.add_edge("page", "executor")

builder.add_edge("executor", END)

workflow = builder.compile()