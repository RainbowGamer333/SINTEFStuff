from graphDisplay.cypherDisplay import CypherDisplay
from openAI.cypherbot import CypherBot

if __name__ == "__main__":
    connection = CypherDisplay('https', 'demo.neo4jlabs.com', 7473, auth=('recommendations', 'recommendations'))

    bot = CypherBot(prompt="prompt.txt", history=False)
    while True:
        query = bot.ask_question()
        if query:
            connection.execute_query(query)

            connection.create_html_graph('graph.html')
            connection.open_graph('graph.html')
        else:
            break
