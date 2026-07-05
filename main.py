from graph.workflow import workflow


if __name__ == "__main__":

    print("=" * 70)
    print("Agentic Mobile Automation using LangGraph")
    print("=" * 70)

    workflow.invoke({

        "planner": False,
        "inspector": False,
        "locator": False,
        "page": False,
        "executor": False

    })

    print("\nPipeline Completed Successfully")