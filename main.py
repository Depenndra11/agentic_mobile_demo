from agents.planner import PlannerAgent


def main():

    planner = PlannerAgent()

    requirement = """
    Verify that a user can log in successfully using
    valid username and password.
    """

    plan = planner.plan(requirement)

    print(plan)


if __name__ == "__main__":
    main()