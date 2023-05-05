import os
import webbrowser

from networkx import MultiDiGraph
import py2neo
from py2neo import Graph
from pyvis.network import Network


class GraphDisplay:
    """
    A class to handle the execution of cypher queries and to display the results.
    """

    def __init__(self, sch, h, p, auth=(None, None), query=None):
        self.graph = Graph(scheme=sch, host=h, port=p, auth=(auth[0], auth[1]))
        self.data = self.execute_query(query) if query is not None else None
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
        result = self.graph.run(query)
        self.data = result.data()


    def get_graph_from_data(self) -> MultiDiGraph:
        """
        Convert the data returned from a query into a networkx graph.
        :return: networkx MultiDiGraph containing the data returned from the query
        """

        assert self.data is not None, 'No data has been set. Execute a query first.'
        g = MultiDiGraph()
        for record in self.data:
            for value in record.values():

                # if node
                if isinstance(value, py2neo.data.Node):
                    display, colour = self.get_node_display(value)
                    g.add_node(display, color=colour)


                # if relationship
                elif isinstance(value, py2neo.data.Relationship):
                    rel = type(value).__name__
                    startDisplay, _ = self.get_node_display(value.start_node)
                    endDisplay, _ = self.get_node_display(value.end_node)

                    if not g.has_edge(startDisplay, endDisplay):
                        g.add_edge(startDisplay, endDisplay, label=rel, arrows="to", color="grey")

                    else:
                        # if specific relationship doesn't already exist, add it
                        edge_data = g.get_edge_data(startDisplay, endDisplay)
                        if rel not in [edge_data[key]['label'] for key in edge_data.keys()]:
                            g.add_edge(startDisplay, endDisplay, label=rel, arrows="to", color="grey")
        return g

    def get_node_display(self, node) -> (str, str):
        """
        Get the display and colour of a node.
        If the node has the correct display attribute then that will be used, otherwise the node's identity will be used.
        """

        attr = self.__nodeDisplay[list(node.labels)[0]]

        display = node[attr['display']] if node[attr['display']] is not None else str(node.identity)
        colour = attr['colour']

        return display, colour

    def create_graph(self, filename=None, result=False) -> MultiDiGraph:
        """
        Display the result of a query as a network graph. You can view the graph as a html file.
        :param filename: the name of the file to be created. Will be automatically appended with '.html' if not already.
        If None then the function will use the current self.filename
        :param result: if True then the function will return the networkx graph
        :return: None
        """
        assert filename is not None or self.filename is not None, 'No filename has been set'

        if filename is not None:
            self.set_filename(filename)

        g = self.get_graph_from_data()

        nt = Network(notebook=True, directed=True, height="1400px", cdn_resources="remote")
        nt.from_nx(g)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        graph_path = os.path.join(os.path.dirname(current_dir), 'graphs', self.filename)

        nt.write_html(graph_path)

        if result:
            return g

    def open_graph(self, name=None):
        """
        Open a file and return its content.
        :return: the content of the file
        """
        assert name is not None or self.filename is not None, 'No filename has been set'
        if name is not None:
            self.set_filename(name)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        graph_path = os.path.join(os.path.dirname(current_dir), 'graphs', self.filename)

        assert os.path.exists(graph_path), self.filename + ' does not exist'
        webbrowser.open(graph_path)

    def set_node_displays(self, nodeDisplays):
        """
        Set the nodeDisplay dictionary to the given dictionary.
        :param nodeDisplays: a dictionary containing the node displays
        :return: None
        """
        self.__nodeDisplay = nodeDisplays

    def add_node_displays(self, label, display, colour):
        """
        Add a node display to the nodeDisplay dictionary. If the label already exists, then it will be replaced.
        :param label: the name of the node
        :param display: the attribute of the node to be displayed. If a node does not have this attribute then its identity will be used.
        :param colour: the colour of the node
        :return: None
        """
        self.__nodeDisplay[label] = {'display': display, 'colour': colour}


if __name__ == '__main__':
    cypher = GraphDisplay('https', 'demo.neo4jlabs.com', 7473, auth=('recommendations', 'recommendations'))
    cypher.execute_query("match (p:Person) return p limit 15")
    g = cypher.create_graph('graph', result=True)
    cypher.open_graph()
    print(g.nodes)