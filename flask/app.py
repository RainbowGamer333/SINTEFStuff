import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request
from datetime import datetime
from py2neo.errors import ClientError, ConnectionUnavailable
from openai.error import APIError

from src.graphDisplay import GraphDisplay
from src.conversation import *

app = Flask(__name__, template_folder='templates')

@app.route("/", methods=['GET', 'POST'])
def run_app():
    if request.method == 'POST':
        # if button clear is pressed, reset messages
        try:
            request.form['clear']
            reset_messages()
            
        # if button send is pressed, get chatbot response
        except Exception:
            error = True
            question = request.form['user-message']
            try:
                reply(question)
                error = False
            except ConnectionUnavailable:
                add_message('assistant', "Connection unavailable. Please try again later.")
            # if user input cannot be interpreted, display error message
            except (ClientError, APIError):
                add_message('assistant', 'An error has occurred. Please clear conversation and try again')
            except Exception as e:
                add_message('assistant', e)
                
            
            finally:
                return render_template('index.html', messages=messages, graph_name="graph.html", error=error)

    return render_template('index.html', messages=messages, connection=True, graph_name=None)


def reply(question):
    add_message('user', question)
    response = continue_conversation(connection, messages)
    add_message('assistant', response)
    
    
def add_message(role, message):
    messages.append({'role': role, 'time': datetime.now().strftime("%H:%M"), 'content': message})
    

def reset_messages():
    global messages
    messages = []
    add_message('assistant', 'Welcome to the Neo4j Chatbot')


if __name__ == "__main__":
    connection = GraphDisplay('https', 'demo.neo4jlabs.com', 7473, auth=('recommendations', 'recommendations'))
    reset_messages()
    app.run()