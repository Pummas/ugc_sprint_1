from clickhouse_driver import Client




if __name__ == "__main__":


    client = Client(host='localhost')
    show = client.execute('SHOW DATABASES')
    data = client.execute('CREATE DATABASE IF NOT EXISTS example ON CLUSTER company_cluster')
    table = client.execute(
        'CREATE TABLE IF NOT EXISTS example.regular_table ON CLUSTER company_cluster (id Int64, x Int32) Engine=MergeTree() ORDER BY id')
    insert = client.execute('SELECT * FROM example.regular_table')
    print(client)