import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
import openai
from spellchecker import SpellChecker

import openAI.remoteapi as remoteapi


class ChatBot:
    def __init__(self, temperature, max_tokens, presence_penalty, prompt, history=False, log=True):
        """
        Initialise the chatbot.
        :param prompt: the name of the file containing the prompt to be used. Will search for it in the prompt folder.
        :param history: if True then the AI will use the prompt and all previous messages as context. If False then the AI will only use the prompt and the current message as context.
        :param log: if True then the AI will log the conversation to a file.
        """
        remoteapi.loadCredential()
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.presence_penalty = presence_penalty

        self.usage = {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}
        self.messages = []
        self.prompt = ''
        self.set_prompt(prompt)
        self.history = history
        self.log = log

    def add_message(self, role, content):
        """
        Add a message to the messages list.
        :param role: the role of the message. Can be:
            'system' for giving instructions to the bot,
            'assistant' for the bot's responses, or
            'user' for the user's messages
        :param content: the content of the message
        """
        self.messages.append(format_message(role, content))

    def set_prompt(self, promptFile):
        """
        Set the prompt to be used by the AI. This will overwrite the current prompt.
        :param promptFile: the name of the file containing the prompt to be used. Will search for it in the prompt folder.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_filepath = os.path.join(os.path.dirname(current_dir), "prompt", promptFile)
        with open(prompt_filepath, "r") as file:
            self.prompt = format_message('system', file.read())

    def get_ai_response(self) -> dict:
        """
        Get the AI's response to the current conversation.
        :return: a dictionary containing the AI's response and the usage of the API.
        To get the content of the response use response['choices'][n]['content'] where n is the index of the response.
        """

        # If self.history is false, the AI will only use the prompt and the current message as context
        if self.history:
            message = [self.prompt] + self.messages
        else:
            message = [self.prompt, self.messages[-1]]

        return openai.ChatCompletion.create(
            engine="gpt-35",
            messages=message,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            presence_penalty=self.presence_penalty
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
                if item['role'] != 'system':
                    f.write(f"[{item['role']}]: ")
                    f.write(item['content'] + '\n')
            f.write(str(self.usage))

        print("The conversation has ended. You will find the chat history at : ", filename)


    def reply(self, add_message=False) -> str:
        """
        Add the user's message to the messages list, and return the AI's response.
        """

        # If history is true, then the AI will use the entire conversation as context.
        response = self.get_ai_response()
        reply = response['choices'][0]['message']['content']

        for i in self.usage:
            self.usage[i] += response['usage'][i]

        self.add_message('assistant', reply) if add_message else None

        return reply


def format_message(role, message) -> dict:
    """
    Format the message to be used as context for the AI.
    """
    print("message : " + message)
    spellcheckMessage = spellcheck(message)
    print("spellchecked message : " + spellcheckMessage)
    return {'role': role, 'content': message}


def spellcheck(message):
    spell = SpellChecker()
    words = spell.unknown(message.split())
    for word in words:
        message = message.replace(word, spell.correction(word))
    return message


if __name__ == "__main__":
    # bot = ChatBot(prompt="questionToQuery.txt", temperature=0.6, max_tokens=200, presence_penalty=-1, history=True, log=False)
    # bot.add_message('user', 'Who directed Interstellar?')
    # print(bot.reply())
    m = "dorected is the name of the director of the movie interstellar"
    print(spellcheck(m))