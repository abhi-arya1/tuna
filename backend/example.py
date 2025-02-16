from openai import OpenAI

client = OpenAI(
    api_key="runway_basic_key",
    base_url="http://localhost:8000/v1"
)

stream = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Give me a graph of a binary tree with a inorder traversal of 2, 3, 4, 5, 6, 7, 8"
        }
    ],
    model="runway_example",
)


print(stream)