import remoteapi
import openai
from termcolor import colored
from datetime import datetime


def fixed_invoke(messages):
    return openai.ChatCompletion.create(
        engine="gpt-35",
        messages=messages,
        temperature=0,
        max_tokens=200,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )


messages = []
usage = {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}


def init():
    hint = input(colored("What is the role of API?\n> "))
    messages.append({'role': 'system', 'content': hint})


def log_conversation():
    f = open('../log/' + datetime.now().strftime("%Y%m%d-%H.%M.%S") + '.txt', 'w')
    for item in messages:
        f.write('[' + item['role'] + ']: ')
        f.write(item['content'] + '\n')
    f.write(str(usage))
    f.close()


def ask():
    question = input(colored('Continue, or type "END"\n> '))
    if question == 'END':
        log_conversation()
        return True

    messages.append({'role': 'user', 'content': question})
    response = fixed_invoke(messages)
    reply = response['choices'][0]['message']
    messages.append(reply)
    print(reply['content'])

    oneusage = response['usage']
    for i in usage:
        usage[i] = usage[i] + oneusage[i]

    return False


if __name__ == "__main__":
    remoteapi.loadCredential()
    init()
    while True:
        if ask():
            break