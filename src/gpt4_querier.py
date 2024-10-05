from openai import OpenAI

api_key = "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"
client = OpenAI(api_key=api_key)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": """
        System prompt:
        You are a concise assistant. Prioritize brevity and clear, step-by-step responses.
        Avoid unnecessary enthusiasm or excessive politeness.
        Focus on delivering logical, precise answers.
        Keep responses short and to the point, offering only what is needed to address the query.
        """},
        {
            "role": "user",
            "content": input("Prompt: ")
        }
    ]
)
# TODO: make code blocks different
print()
print(completion.choices[0].message.content)
# legacy api key: sk-3w1nHSB3v-Qo1YOft0ZjzZ_82GZCrqJWsntXzxTAvPT3BlbkFJPOfvPtYRp-wfC3qAvG1cd6II6vYbdpqfzqwhN_01kA
# project api key: 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
