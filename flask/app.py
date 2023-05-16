import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, url_for
from datetime import datetime
from py2neo.errors import ClientError
from openai.error import APIError

from src.cypherInterpretation.graphDisplay import GraphDisplay
from src.conversation import *

app = Flask(__name__, template_folder='templates')

@app.route("/", methods=['GET', 'POST'])
def load_index():
    print(url_for('static', filename='style.css'))
    if request.method == 'POST':
        # if button clear is pressed, reset messages
        try:
            request.form['clear']
            reset_messages()
        except Exception:
            question = request.form['user-message']
            print("question : ", question)
            try:
                reply(question)
                
                graph_name='graph.html'
                return render_template('index.html', connection=graphDisplay, messages=messages, graph_name=graph_name, error=False)
            # if user input cannot be interpreted, display error message
            except (ClientError, APIError):
                add_message('assistant', 'An error has occurred. Please clear conversation...')
                return render_template('index.html', connection=graphDisplay, messages=messages, error=True)

    return render_template('index.html', messages=messages, connection=graphDisplay, error=False)


def reply(question):
    add_message('user', question)
    response = continue_conversation(graphDisplay, messages=messages)
    add_message('assistant', response)


def reset_messages():
    global messages
    messages = []
    add_message('assistant', 'Welcome to the Neo4j Chatbot')


def add_message(role, message):
    messages.append({'role': role, 'time': datetime.now().strftime("%H:%M"), 'content': message})



if __name__ == "__main__":
    graphDisplay = GraphDisplay('https', 'demo.neo4jlabs.com', 7473, auth=('recommendations', 'recommendations'))
    reset_messages()
    app.run()