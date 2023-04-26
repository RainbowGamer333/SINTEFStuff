from cypherDisplay import CypherDisplay

cypher = CypherDisplay('https', 'demo.neo4jlabs.com', 7473, 'recommendations', 'recommendations')

if __name__ == '__main__':
    cypher.execute_query("MATCH (p:Person) -[r]-> (m:Movie) WHERE EXISTS(p.name) RETURN p, r, m limit 20")
    cypher.create_html_graph('example')
    cypher.open_graph('example')
    # print(cypher.get_data_as_table())
