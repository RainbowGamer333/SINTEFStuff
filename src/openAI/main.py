import openai
import remoteapi


def testChatGPT(question):
    """
    Documentation: https://platform.openai.com/docs/api-reference/completions/create?lang=python
    Search create chat completion
    """
    remoteapi.loadCredential()

    with open("../prompt/prompt.txt", "r") as prompt:

        response = openai.ChatCompletion.create(
            engine="gpt-35",
            messages=[
                {"role":"system", "content": prompt.read()},
                {"role":"user","content": question}
            ],
            temperature=0,
            max_tokens=80,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        print(response["choices"][-1]["message"]["content"])


if __name__ == "__main__":
    testChatGPT("When was Interstellar released?")
    # with open("../prompt.txt", "r") as prompt:
    #     content = prompt.readlines()
    #     print(len(content))