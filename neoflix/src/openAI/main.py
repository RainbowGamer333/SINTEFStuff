import openai
import remoteapi

def testChatGPT():
    remoteapi.loadCredential()
    response = openai.ChatCompletion.create(
        engine="gpt-35",
        messages=[
            {"role":"system", "content":"You will give Cypher queries corresponding to the question the user will give you. Give only the query, no text before or after"},
            {"role":"user","content":"Who directed Interstellar?"}
        ],
        temperature=0,
        max_tokens=80,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    print(response["choices"][0]["message"]["content"])


if __name__ == "__main__":
    testChatGPT()