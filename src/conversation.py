import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.openAI.chatbot import *
from graphDisplay import GraphDisplay


def start_conversation(graphName='graph.html'):
    """Starts a conversation with the user. The conversation is generated in the console."""
    
    connection = GraphDisplay('https', 'demo.neo4jlabs.com', 7473, auth=('recommendations', 'recommendations'))
    
    # queryBot is used to get the query from the user's question
    queryBot = ChatBot(prompt="questionToQuery.txt", temperature=0.4, max_tokens=200, presence_penalty=-1, history=True, log=False)
    # finalBot is used to get the response from the data retrieved from the query
    finalBot = ChatBot(prompt="dataToNatural.txt", temperature=0.05, max_tokens=1000, presence_penalty=-2, history=True)

    while True:
        # ask question
        question = input('Type in your question, or type "QUIT"\n> ')
        if question.lower() == 'quit':
            finalBot.log_conversation()
            return
        queryBot.add_message('user', question)

        # get queryBot reply
        query = queryBot.reply(add_message=True)

        # execute query and return data
        connection.execute_query(query)
        graph = connection.create_graph('graph.html', result=True)
        assert graph is not None
        nodes = str(graph.nodes)
        queryBot.add_message('system', nodes)

        # get finalBot reply
        finalBot.add_message('user', question)
        finalBot.add_message('system', nodes)
        response = finalBot.reply(add_message=True)

        # display graph
        showGraph = ''
        while showGraph not in ['y', 'n']:
            showGraph = input("Would you like to display the graph? (y/n)\n> ")
            if showGraph == 'y':
                connection.open_graph(graphName)


def continue_conversation(connection, messages, graph_name='graph.html'):
    
    new_messages = format_all_messages(messages)
    # queryBot is used to get the query from the user's question
    queryBot = ChatBot(prompt="questionToQuery.txt", temperature=0.6, max_tokens=200, presence_penalty=-1, history=True, log=False)
    queryBot.messages = new_messages
    # finalBot is used to get the response from the data retrieved from the query
    finalBot = ChatBot(prompt="dataToNatural.txt", temperature=0.05, max_tokens=1000, presence_penalty=-2, history=True)
    finalBot.messages = new_messages

    question = new_messages[-1]['content']
    query = queryBot.reply(add_message=True)

    connection.execute_query(query)
    graph = connection.create_graph(graph_name, result=True)
    assert graph is not None
    
    nodes = str(graph.nodes)
    queryBot.add_message('system', nodes)

    finalBot.add_message('user', question)
    finalBot.add_message('system', nodes)
    response = finalBot.reply(add_message=True)

    return response


def format_all_messages(messages):
    new_messages = []
    for message in messages:
        new_messages.append(format_message(message['role'], message['content']))
    new_messages[-1]['content'] += " Answer only query no extra text"
    return new_messages


def conversationOnlyQuery():
    queryBot = ChatBot(prompt="questionToQuery.txt", temperature=0.6, max_tokens=200, presence_penalty=-1, history=True, log=True)
    
    while True:
        question = input('Type in your question, or type "QUIT"\n> ')
        if question.lower() == 'quit':
            queryBot.log_conversation()
            return
        queryBot.add_message('user', question)
        query = queryBot.reply(add_message=True)
        print(f"\n{query}\n\n")
        

if __name__ == "__main__":
    connection = GraphDisplay('https', 'demo.neo4jlabs.com', 7473, auth=('recommendations', 'recommendations'))
    messages = [{'role': "assistant", 'content': "Welcome to the Neo4j Chatbot!"}, {'role': "user", 'content': "Who directed the movie Interstellar"}]
    response = continue_conversation(connection, messages)
    print(response)