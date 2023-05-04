import os
from datetime import datetime

import nltk
import openai
from nltk.corpus import stopwords

from . import remoteapi


class CypherBot:
    def __init__(self, prompt=None, history=False):
        remoteapi.loadCredential()

        self.usage = {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}
        self.messages = []
        self.set_prompt(prompt) if prompt else None
        self.history = history

    def add_message(self, role, content):
        self.messages.append({'role': role, 'content': content})

    def set_prompt(self, promptFile):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_filepath = os.path.join(os.path.dirname(current_dir), "prompt", promptFile)
        with open(prompt_filepath, "r") as file:
            prompt = file.read()
            self.add_message('system', prompt)

    def get_ai_response(self, m=None):

        # If self.history is false, the AI will only use the prompt and the current message as context
        message = m if m else self.messages if self.history else [self.messages[0], self.messages[-1]]

        # TODO: try out the stream parameter
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
        filename = datetime.now().strftime("%Y_%m_%d-%H.%M.%S") + '.txt'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        log_filepath = os.path.join(os.path.dirname(current_dir), "log", filename)

        with open(log_filepath, 'w') as f:
            for item in self.messages:
                f.write('[' + item['role'] + ']: ')
                f.write(item['content'] + '\n')
            f.write(str(self.usage))

        print("The conversation has ended. You will find the chat history at : ", filename)

    def ask_question(self):
        """
        Asks for the user's question and returns the response from the AI.
        """
        question = input('Type in your question, or type "QUIT"\n> ')
        if question.lower() == 'quit':
            self.log_conversation()
            return

        reply = self.reply(question)
        print(reply + "\n")
        return reply

    def reply(self, message):
        """
        Add the user's message to the messages list, and return the AI's response.
        """
        self.add_message('user', message)

        # If history is true, then the AI will use the entire conversation as context.
        response = self.get_ai_response()
        reply = response['choices'][0]['message']
        self.messages.append(reply)

        for i in self.usage:
            self.usage[i] += response['usage'][i]

        return reply['content']


    def start_conversation(self):
        """
        Start a conversation with the AI.
        """
        while self.ask_question():
            pass

    def remove_stopwords(self, text):
        """
        Tokenize the text and return a list of tokens.
        """
        text = nltk.word_tokenize(text)
        newText = []

        stop_words = set(stopwords.words('english'))
        for word in text:
            if word.lower() not in stop_words:
                newText.append(word)
        return ' '.join(newText)


if __name__ == '__main__':
    bot = CypherBot("../prompt/prompt.txt")
    bot.start_conversation()
