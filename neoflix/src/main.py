from cypherTesting import CypherTesting

if __name__ == '__main__':
    cypher = CypherTesting('neo4j+s', 'demo', 7687, 'recommendations', 'recommendations')
    cypher.execute_query("MATCH (p:Person) -[r]- (m:Movie) RETURN p, r, m limit 20")
    cypher.get_html_graph('example')
    cypher.open_graph()
    print(cypher.get_data_as_table())
