# agents/approval_agent.py

def request_approval(state):

    sql = state.get("optimized_sql")

    print("\n================ APPROVAL ================")
    print(sql)
    print("=========================================\n")

    decision = input("Approve execution? (y/n): ")

    return decision.lower() == "y"