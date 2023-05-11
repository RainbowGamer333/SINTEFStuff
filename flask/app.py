import sys
import os
import py2neo.errors
from datetime import datetime
from flask import Flask, render_template, request
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cypherInterpretation.graphDisplay import GraphDisplay
from src.conversation import *

app = Flask(__name__, template_folder='templates')

@app.route("/", methods=['GET', 'POST'])
def load_index():
    print("Loading index...")
    if request.method == 'POST':
        print("POST request received...")
        print([f for f in request.form])
        try:
            request.form['clear']
            print("Clearing conversation...")
            reset_messages()
        except Exception:
            question = request.form['user-message']
            try:
                reply(question)
                return render_template('index.html', messages=messages, connection=graphDisplay, error=False)
            except py2neo.errors.ClientError:
                add_message('assistant', 'An error has occurred. Please try again...')
                return render_template('index.html', messages=messages, connection=graphDisplay, error=True)

    return render_template('index.html', messages=messages, connection=graphDisplay, error=False)


def reply(question):
    add_message('user', question)
    response = continue_conversation(graphDisplay, messages=messages)
    add_message('assistant', response)


def reset_messages():
    global messages
    messages = []
    add_message('assistant', 'Welcome to the Neo4j Chatbot!')


def add_message(role, message):
    messages.append({'role': role, 'time': datetime.now().strftime("%H:%M"), 'content': message})



if __name__ == "__main__":
    graphDisplay = GraphDisplay('https', 'demo.neo4jlabs.com', 7473, auth=('recommendations', 'recommendations'))
    reset_messages()
    app.run()