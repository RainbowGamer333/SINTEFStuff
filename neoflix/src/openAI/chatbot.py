import remoteapi
import openai
from termcolor import colored
from datetime import datetime


# todo: implement the API into the rest of the code

class ChatBot:
    def __init__(self, promptPath):
        remoteapi.loadCredential()
        self.usage = {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}
        with open(promptPath, "r") as prompt:
            self.messages = [{'role': 'system', 'content': prompt.read()}]

    def get_ai_response(self):
        return openai.ChatCompletion.create(
            engine="gpt-35",
            messages=self.messages,
            temperature=0,
            max_tokens=200,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )

    def log_conversation(self):
        f = open('../log/' + datetime.now().strftime("%Y%m%d-%H.%M.%S") + '.txt', 'w')
        for item in self.messages:
            f.write('[' + item['role'] + ']: ')
            f.write(item['content'] + '\n')
        f.write(str(self.usage))
        f.close()


    def ask(self):
        question = input(colored('Continue, or type "END"\n> '))
        if question == 'END':
            self.log_conversation()
            return False

        self.messages.append({'role': 'user', 'content': question})
        response = self.get_ai_response()
        reply = response['choices'][0]['message']
        self.messages.append(reply)
        print(reply['content'])

        oneusage = response['usage']
        for i in self.usage:
            self.usage[i] = self.usage[i] + oneusage[i]

        return True


if __name__ == "__main__":
    chat = ChatBot("../prompt/prompt.txt")
    while chat.ask():
        pass





















