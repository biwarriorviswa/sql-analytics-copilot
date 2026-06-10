from config import llm


def insight_agent(state):

    analytics = state.get("analytics", {})
    user_query = state.get("user_query", "")
    data = state.get("data")

    metric = analytics.get("metric")
    dimension = analytics.get("dimension")

    # ----------------------------
    # DataFrame -> records
    # ----------------------------

    if data is not None:
        try:
            records = data.to_dict(
                orient="records"
            )
        except Exception:
            records = []
    else:
        records = []

    total = analytics.get("total", 0)

    # ----------------------------
    # Add percentages dynamically
    # ----------------------------

    enriched_data = []

    for row in records:

        value = row.get(metric, 0)

        percentage = (
            round((value / total) * 100, 2)
            if total
            else 0
        )

        enriched_row = {
            **row,
            "percentage": percentage
        }

        enriched_data.append(
            enriched_row
        )

    # ----------------------------
    # Dynamic ranking
    # ----------------------------

    sorted_data = sorted(
        enriched_data,
        key=lambda x: x.get(metric, 0),
        reverse=True
    )

    analytics["data"] = enriched_data
    analytics["ranked"] = sorted_data
    analytics["top_3"] = sorted_data[:3]

    # ----------------------------
    # Prompt
    # ----------------------------

    with open(
        "prompts/insight_prompt.txt",
        "r",
        encoding="utf-8"
    ) as f:

        template = f.read()

    prompt = template.format(
        user_query=user_query,
        analytics=analytics,
        data=enriched_data,
        data_type=analytics.get(
            "data_type",
            "static_snapshot"
        )
    )

    response = llm.invoke(prompt)

    insights = (
        response.content
        if hasattr(response, "content")
        else str(response)
    )

    return {
        "insights": insights
    }