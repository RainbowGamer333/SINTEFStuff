from flask import Flask, render_template, request
from datetime import datetime
from cypherInterpretation.graphDisplay import GraphDisplay
from conversation import *

app = Flask(__name__, template_folder='templates')

messages = [{'role': 'assistant', 'time': datetime.now().strftime("%H:%M"), 'content': 'Welcome to the Neo4j Chatbot!'}]

@app.route("/", methods=('GET', 'POST'))
def load_index():
    graphDisplay = GraphDisplay('https', 'demo.neo4jlabs.com', 7473, auth=('recommendations', 'recommendations'))
    if request.method == 'POST':
        question = request.form['user-message']
        reply(graphDisplay, question)

    return render_template('index.html', messages=messages, connection=graphDisplay)

def reply(connection, question):
    messages.append({'role': 'user', 'time': datetime.now().strftime("%H:%M"), 'content': question})
    response = continue_conversation(connection, messages=messages)
    messages.append({'role': 'assistant', 'time': datetime.now().strftime("%H:%M"), 'content': response})





if __name__ == "__main__":
    app.run()