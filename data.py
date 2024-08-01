from neo4j import GraphDatabase
import csv
import os

# Neo4j connection setup
uri = "bolt://localhost:7687"
username = "neo4j"
password = "12345678"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Directory containing Cypher queries
query_dir = "queries"
# Directory to export .csv data to
data_dir = "data"

def export_data(query, filename):
    with driver.session() as session:
        # Running the query
        result = session.run(query)
        # Open a CSV file and write the data
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Writing headers
            writer.writerow(result.keys())
            # Writing rows
            for record in result:
                writer.writerow(record.values())

# Main execution
if __name__ == "__main__":
    # List all Cypher files in the queries directory
    for file in os.listdir(query_dir):
        if file.endswith(".cypher"):
            file_path = os.path.join(query_dir, file)
            # Construct the CSV filename from the Cypher file name
            csv_filename = file.replace('.cypher', '.csv')
            # Read the query from the Cypher file
            with open(file_path, 'r') as cypher_file:
                query = cypher_file.read()
                # Export the data to CSV
                export_data(query, f'{data_dir}/{csv_filename}')

    print("Data has been exported to CSV files.")