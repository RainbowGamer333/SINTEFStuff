from openAI.chatbot import ChatBot

def start_conversation(connection, graphName='graph.html'):
    # queryBot is used to get the query from the user's question
    queryBot = ChatBot(prompt="questionToQuery.txt", temperature=0.6, max_tokens=200, presence_penalty=-1, history=True, log=False)
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
        print(query)

        # execute query and return data
        connection.execute_query(query)
        graph = connection.create_graph('graph.html', result=True)
        nodes = str(graph.nodes)
        print(nodes)
        queryBot.add_message('system', nodes)

        # get finalBot reply
        finalBot.add_message('user', question)
        finalBot.add_message('system', nodes)
        response = finalBot.reply(add_message=True)
        print(response)

        # display graph
        showGraph = ''
        while showGraph not in ['y', 'n']:
            showGraph = input("Would you like to display the graph? (y/n)\n> ")
            if showGraph == 'y':
                connection.open_graph(graphName)