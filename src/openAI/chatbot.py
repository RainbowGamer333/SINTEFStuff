import os
from datetime import datetime

import nltk
import openai
from nltk.corpus import stopwords

if __name__ != '__main__':
    from . import remoteapi
else:
    import remoteapi



class ChatBot:
    def __init__(self, prompt, history=False, log=True):
        """
        Initialise the chatbot.
        :param prompt: the name of the file containing the prompt to be used. Will search for it in the prompt folder.
        :param history: if True then the AI will use the prompt and all previous messages as context. If False then the AI will only use the prompt and the current message as context.
        :param log: if True then the AI will log the conversation to a file.
        """
        remoteapi.loadCredential()

        self.usage = {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}
        self.messages = []
        self.prompt = ''
        self.set_prompt(prompt)
        self.history = history
        self.log = log

    def add_message(self, role, content):
        self.messages.append(format_message(role, content))

    def set_prompt(self, promptFile):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_filepath = os.path.join(os.path.dirname(current_dir), "prompt", promptFile)
        with open(prompt_filepath, "r") as file:
            self.prompt = format_message('system', file.read())

    def get_ai_response(self):

        # If self.history is false, the AI will only use the prompt and the current message as context
        if self.history:
            message = [self.prompt]
            message.extend(self.messages)
        else:
            message = [self.prompt, self.messages[-1]]

        return openai.ChatCompletion.create(
            engine="gpt-35",
            messages=message,
            max_tokens=200,
            temperature=0.05,
            frequency_penalty=-1,
            presence_penalty=-1
        )

    def log_conversation(self):
        """
        Log the conversation to a file. The file will be named with the current date and time.
        """
        if not self.log:
            return

        filename = datetime.now().strftime("%Y_%m_%d-%H.%M.%S") + '.txt'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        log_filepath = os.path.join(os.path.dirname(current_dir), "log", filename)

        with open(log_filepath, 'w') as f:
            for item in self.messages:
                f.write('[' + item['role'] + ']: ')
                f.write(item['content'] + '\n')
            f.write(str(self.usage))

        print("The conversation has ended. You will find the chat history at : ", filename)


    def reply(self):
        """
        Add the user's message to the messages list, and return the AI's response.
        """

        # If history is true, then the AI will use the entire conversation as context.
        response = self.get_ai_response()
        reply = response['choices'][0]['message']

        for i in self.usage:
            self.usage[i] += response['usage'][i]

        return reply['content']


def format_message(role, message):
    """
    Format the message to be used as context for the AI.
    """
    return {'role': role, 'content': message}