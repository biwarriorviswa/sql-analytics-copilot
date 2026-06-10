from config import llm

response = llm.invoke(
    "What is SQL?"
)

print(response.content)