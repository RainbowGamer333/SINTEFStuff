import remoteapi
import openai
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
        with open('../log/' + filename, 'w') as f:
            for item in self.messages:
                f.write('[' + item['role'] + ']: ')
                f.write(item['content'] + '\n')
            f.write(str(self.usage))
        print("The conversation has concluded. You will find it at : ", filename)



    def start_conversation(self):
        while True:
            question = input('Continue, or type "END"\n> ')
            if question.lower() == 'end':
                self.log_conversation()
                return

            self.add_message('user', question)
            response = self.get_ai_response()
            reply = response['choices'][0]['message']
            self.messages.append(reply)
            print(reply['content'])

            for i in self.usage:
                self.usage[i] += response['usage'][i]



if __name__ == "__main__":
    chat = CypherBot("../prompt/prompt.txt")
    chat.start_conversation()





















