from cypherInterpretation.graphDisplay import GraphDisplay
from openAI.chatbot import ChatBot

def start_conversation(connection):
    # queryBot is used to get the query from the user's question
    queryBot = ChatBot(prompt="questionToQuery.txt", history=True, log=False)
    # finalBot is used to get the response from the data retrieved from the query
    finalBot = ChatBot(prompt="dataToNatural.txt", history=True)

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

        # get finalBot reply
        finalBot.add_message('system', str(graph.nodes))
        finalBot.add_message('user', question)
        response = finalBot.reply(add_message=True)
        display_response(response)

        # display graph
        showGraph = ''
        while showGraph not in ['y', 'n']:
            showGraph = input("Would you like to display the graph? (y/n)\n> ")
            if showGraph == 'y':
                connection.open_graph('graph.html')


def display_response(answer):
    print(answer)


if __name__ == "__main__":
    graphDisplay = GraphDisplay('https', 'demo.neo4jlabs.com', 7473, auth=('recommendations', 'recommendations'))
    start_conversation(graphDisplay)
