from cypherDisplay import CypherDisplay

cypher = CypherTesting('https', 'demo.neo4jlabs.com', 7473, 'recommendations', 'recommendations')

if __name__ == '__main__':
    cypher.execute_query("MATCH (a:Actor) -[r]-> () WHERE EXISTS(a.name) RETURN a, r limit 20")
    cypher.get_html_graph('example')
    cypher.open_graph('example')
    # print(cypher.get_data_as_table())
