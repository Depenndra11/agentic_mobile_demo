from graph.workflow import workflow
from utils.logger import get_logger

logger = get_logger(__name__)


if __name__ == "__main__":

    logger.info("Agentic Mobile Automation using LangGraph — starting")

    initial_state = {
        "planner_done": False,
        "inspector_done": False,
        "page_done": False,
        "executor_done": False,
        "testcases": None,
        "screen_xml_path": None,
        "error": None,
    }

    try:
        workflow.invoke(initial_state)
    except Exception:
        logger.error("Pipeline failed — see error above for the failing agent")
        raise
    else:
        logger.info("Pipeline completed successfully")