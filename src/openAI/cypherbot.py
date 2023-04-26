from . import remoteapi

import openai
import os
from datetime import datetime


# todo: implement the API into the rest of the code

class CypherBot:
    def __init__(self, promptPath=None):
        remoteapi.loadCredential()

        self.usage = {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}
        self.messages = []

        self.set_prompt(promptPath) if promptPath else None


    def add_message(self, role, content):
        self.messages.append({'role': role, 'content': content})


    def set_prompt(self, promptPath):
        with open(promptPath, "r") as prompt:
            self.add_message('system', prompt.read())

    def get_ai_response(self):
        return openai.ChatCompletion.create(
            engine="gpt-35",
            messages=self.messages,
            max_tokens=200,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )

    def log_conversation(self):
        filename = datetime.now().strftime("%Y%m%d-%H.%M.%S") + '.txt'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        log_filepath = os.path.join(os.path.dirname(current_dir), "log", filename)

        with open(log_filepath, 'w') as f:
            for item in self.messages:
                f.write('[' + item['role'] + ']: ')
                f.write(item['content'] + '\n')
            f.write(str(self.usage))

        print("The conversation has concluded. You will find it at : ", filename)


    def ask_question(self):
        question = input('Type in your question, or type "QUIT"\n> ')
        if question.lower() == 'quit':
            return

        self.add_message('user', question)
        response = self.get_ai_response()
        reply = response['choices'][0]['message']
        self.messages.append(reply)

        for i in self.usage:
            self.usage[i] += response['usage'][i]

        self.log_conversation()
        print(reply['content'])
        return reply['content']


if __name__ == '__main__':
    bot = CypherBot(__file__ + "\\..\\prompt\\prompt.txt")
    while True:
        query = bot.ask_question()
        if query:
            print(query)
        else:
            break






















