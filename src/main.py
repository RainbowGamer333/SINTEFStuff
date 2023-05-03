from graphDisplay.cypherDisplay import CypherDisplay
from openAI.cypherbot import CypherBot

if __name__ == "__main__":
    connection = CypherDisplay('https', 'demo.neo4jlabs.com', 7473, auth=('recommendations', 'recommendations'))

    bot = CypherBot(prompt="prompt.txt", history=True)
    while True:
        query = bot.ask_question()
        if not query: break

        show = ''
        while show not in ['y', 'n']:
            show = input("Would you like to display the graph? (y/n)\n> ")
            if show == 'y':
                connection.execute_query(query)

                connection.create_html_graph('graph.html')
                connection.open_graph('graph.html')
