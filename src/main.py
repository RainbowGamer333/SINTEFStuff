from cypherInterpretation.graphDisplay import GraphDisplay
from conversation import *

if __name__ == "__main__":
    graphDisplay = GraphDisplay('https', 'demo.neo4jlabs.com', 7473, auth=('recommendations', 'recommendations'))
    start_conversation(graphDisplay)

