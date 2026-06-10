def human_approval_agent(state):

    sql = state.get("optimized_sql") or state.get("generated_sql")

    print("\n================ HUMAN APPROVAL ================")
    print("SQL FOR REVIEW:\n", sql)

    # default: blocked until explicitly approved
    approved = state.get("approved", False)

    if not approved:
        return {
            "approval_status": "pending",
            "execution_blocked": True
        }

    return {
        "approval_status": "approved",
        "execution_blocked": False
    }