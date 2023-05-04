import graphDisplay
import pandas as pd

class DataCollection:
    def __init__(self, data):
        self.table = pd.DataFrame(data)


if __name__ == '__main__':
    graph = graphDisplay.GraphDisplay('bolt', 'localhost', 7687, auth=('neo4j', 'password'))
    info = graph.execute_query("match (n) -[r]- (m) return n, r, m limit 15").data()
    data = DataCollection(info)