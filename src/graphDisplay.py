import os
import webbrowser

from networkx import MultiDiGraph
from py2neo import Graph, data
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
        
        assert self.filename is not None


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
                if isinstance(value, data.Node):
                    display, colour = self.get_node_display(value)
                    g.add_node(display, color=colour)


                # if relationship
                elif isinstance(value, data.Relationship):
                    rel = type(value).__name__
                    startDisplay, _ = self.get_node_display(value.start_node)
                    endDisplay, _ = self.get_node_display(value.end_node)
                    
                    edge_data = g.get_edge_data(startDisplay, endDisplay)
                    # if nodes are not connected or specific relationship type doesn't already exist
                    if not g.has_edge(startDisplay, endDisplay) or rel not in [edge_data[key]['label'] for key in edge_data.keys()]:
                        g.add_edge(startDisplay, endDisplay, label=rel, arrows="to", color="grey")
        return g


    def create_graph(self, filename=None, result=False):
        """
        Display the result of a query as a network graph. You can view the graph as a html file.
        :param filename: the name of the file to be created. Will be automatically appended with '.html' if not already.
        If None then the function will use the current self.filename
        :param result: if True then the function will return the networkx graph
        :return: None
        """

        if filename is not None:
            self.set_filename(filename)
            
        assert self.filename is not None, 'No filename has been set'
        print(self.filename)

        g = self.get_graph_from_data()

        nt = Network(notebook=True, directed=True, height="500px", cdn_resources="remote")
        nt.from_nx(g, default_node_size=30)
        
        # center the graph
        nt.barnes_hut(central_gravity=0.7)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        graph_path = os.path.dirname(current_dir.encode())
        graph_path = os.path.join(graph_path, b'flask', b'static', b'graphs', self.filename.encode())

        nt.write_html(graph_path.decode())

        if result:
            return g


    def open_graph(self, name=None):
        """
        Open a file and return its content.
        :return: the content of the file
        """
        if name is not None:
            self.set_filename(name)
            
        assert self.filename is not None, 'No filename has been set'

        current_dir = os.path.dirname(os.path.abspath(__file__))
        graph_path = os.path.dirname(current_dir.encode())
        graph_path = os.path.join(graph_path, b'flask', b'static', b'graphs', self.filename.encode())

        assert os.path.exists(graph_path), self.filename + ' does not exist'
        webbrowser.open(graph_path.decode())
        
        
    def get_node_display(self, node):
        """
        Get the display and colour of a node.
        If the node has the correct display attribute then that will be used, otherwise the node's identity will be used.
        """

        attr = self.__nodeDisplay[list(node.labels)[0]]

        display = node[attr['display']] if node[attr['display']] is not None else str(node.identity)
        colour = attr['colour']

        return display, colour


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