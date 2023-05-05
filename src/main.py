from cypherInterpretation.graphDisplay import GraphDisplay
from openAI.chatbot import ChatBot

def start_conversation(graph, bot):
    while True:
        # ask question
        question = input('Type in your question, or type "QUIT"\n> ')
        if question.lower() == 'quit':
            bot.log_conversation()
            return
        bot.add_message('user', question)

        # get chatbot reply
        query = bot.reply()
        print(query)
        # execute query and return data
        graph.execute_query(query)
        g = graph.create_graph('graph.html', result=True)

        # get data and return response

        newBot = ChatBot(prompt="dataToNatural.txt", history=True, log=False)
        newBot.add_message('system', str(g.nodes))
        newBot.add_message('user', question)
        response = newBot.reply()
        bot.add_message('assistant', response)
        print(response)

        showGraph = ''
        while showGraph not in ['y', 'n']:
            showGraph = input("Would you like to display the graph? (y/n)\n> ")
            if showGraph == 'y':
                graph.open_graph('graph.html')



if __name__ == "__main__":
    connection = GraphDisplay('https', 'demo.neo4jlabs.com', 7473, auth=('recommendations', 'recommendations'))
    chatbot = ChatBot(prompt="questionToQuery.txt", history=True)
    start_conversation(connection, chatbot)
