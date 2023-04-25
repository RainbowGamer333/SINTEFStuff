import os
import webbrowser
import py2neo
import pandas as pd
import networkx as nx
from py2neo import Graph
from pyvis.network import Network


class CypherTesting:
    """
    A class to handle the execution of cypher queries and to display the results.
    """

    def __init__(self, sch, h, p, user=None, password=None, que=None):
        """
        Initialise the class.
        """
        self.graph = Graph(scheme=sch, host=h, port=p, auth=(user, password))
        self.data = self.execute_query(que) if que is not None else None
        self.__nodeDisplay = {'Person': {'display': 'name', 'colour': 'green'},
                              'Movie': {'display': 'title', 'colour': 'red'},
                              'Genre': {'display': 'name', 'colour': 'orange'},
                              'User': {'display': 'name', 'colour': 'blue'},
                              'Actor': {'display': 'name', 'colour': 'lightgreen'},
                              'Director': {'display': 'name', 'colour': 'blue'}}
        self.filename = None

    def set_filename(self, fname):
        """
        Set the name of the file to be created.
        :param fname: the name of the file to be created. Will be automatically appended with '.html' if not already.
        :return: None
        """
        if not fname.endswith('.html'):
            fname += '.html'
        self.filename = fname

    def execute_query(self, query):
        """
        Set the data returned from the query.
        :return: None
        """
        self.data = self.graph.run(query).data()

    def get_data_as_table(self):
        """
        Display the result of a query as a DataFrame.
        :return: a DataFrame containing the data returned from the query
        """
        assert self.data is not None, 'No data has been set. Execute a query first.'
        return pd.DataFrame(self.data)

    def get_graph_from_data(self):
        """
        Convert the data returned from a query into a networkx graph.
        :return: networkx MultiDiGraph containing the data returned from the query
        """

        g = nx.MultiDiGraph()
        for record in self.data:
            # In case of unusual errors regarding the adding of edges, uncomment the following line.
            # This will create the nodes before the relationship, which may help.

            values = record.values()
            # values = sorted(values(), key=lambda x: x.__class__.__name__, reverse=True)

            for value in values:

                # if node
                if isinstance(value, py2neo.data.Node):
                    attr = self.__nodeDisplay[list(value.labels)[0]]
                    g.add_node(value[attr['display']], color=attr['colour'])
                    print(value.labels)

                # if relationship
                elif isinstance(value, py2neo.data.Relationship):
                    rel = type(value).__name__
                    startNode = value.start_node
                    endNode = value.end_node

                    startStr = startNode[self.__nodeDisplay[list(startNode.labels)[0]]['display']]
                    endStr = endNode[self.__nodeDisplay[list(endNode.labels)[0]]['display']]

                    if not g.has_edge(startStr, endStr):
                        g.add_edge(startStr, endStr, label=rel, arrows="to", color="grey")

                    else:
                        # if relationship doesn't already exist, add it
                        edge_data = g.get_edge_data(startStr, endStr)
                        if rel not in [edge_data[key]['label'] for key in edge_data.keys()]:
                            g.add_edge(startStr, endStr, label=rel, arrows="to", color="grey")
        return g

    def get_html_graph(self, fname=None):
        """
        Display the result of a query as a network graph. You can view the graph as a html file.
        :param fname: the name of the file to be created. Will be automatically appended with '.html' if not already.
        If None then the function will use the current self.filename
        :return: None
        """
        assert self.data is not None, 'No data has been set. Execute a query first.'
        assert fname is not None or self.filename is not None, 'No filename has been set. Set a filename first.'

        if fname is not None:
            self.set_filename(fname)

        g = self.get_graph_from_data()
        nt = Network(notebook=True, directed=True, height="1400px")
        nt.from_nx(g)
        nt.set_edge_smooth('dynamic')
        nt.show(self.filename)

    def open_graph(self, name=None):
        """
        Open a file and return its content.
        :return: the content of the file
        """
        assert name is not None or self.filename is not None, 'No filename has been set. Set a filename first.'

        if name is not None:
            self.set_filename(name)

        assert os.path.exists(
            self.filename), self.filename + ' does not exist. Use get_html_graph(str) to create the file.'
        webbrowser.open(self.filename)

    def add_node_displays(self, label, display, colour):
        """
        Add a node display to the nodeDisplay dictionary. Will replace the existing display if the label already exists.
        :param label: the name of the node
        :param display: the attribute of the node to be displayed
        :param colour: the colour of the node
        :return: None
        """
        self.__nodeDisplay[label] = {'display': display, 'colour': colour}