from flask import Flask, render_template, request
from cypherInterpretation.graphDisplay import GraphDisplay
from conversation import *

app = Flask(__name__, template_folder='templates')
graphDisplay = GraphDisplay('https', 'demo.neo4jlabs.com', 7473, auth=('recommendations', 'recommendations'))
messages = [{'role': 'assistant', 'time': datetime.now().strftime("%H:%M"), 'content': 'Welcome to the Neo4j Chatbot!'}]


@app.route("/", methods=('GET', 'POST'))
def load_index():
    if request.method == 'POST':
        question = request.form['user-message']
        try:
            reply(question)
            return render_template('index.html', messages=messages, connection=graphDisplay, error=False)
        except Exception:
            messages.append({'role': 'assistant', 'time': datetime.now().strftime("%H:%M"), 'content': 'An error has occurred. Please try again.'})
            return render_template('index.html', messages=messages, connection=graphDisplay, error=True)

    return render_template('index.html', messages=messages, connection=graphDisplay, error=False)



# @app.errorhandler(500)
# def internal_error():
#     print("Error message worked")
#     return render_template('index.html', messages=messages, connection=graphDisplay, error=True)


def reply(question):
    messages.append({'role': 'user', 'time': datetime.now().strftime("%H:%M"), 'content': question})
    response = continue_conversation(graphDisplay, messages=messages)
    messages.append({'role': 'assistant', 'time': datetime.now().strftime("%H:%M"), 'content': response})


if __name__ == "__main__":
    app.run()