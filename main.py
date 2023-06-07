from flask import Flask
from flaskApplication import server
from src.graphDisplay import GraphDisplay


if __name__ == "__main__":
    connection = GraphDisplay('https', 'demo.neo4jlabs.com', 7473, auth=('recommendations', 'recommendations'))
    server.reset_messages()
    server.app.run()