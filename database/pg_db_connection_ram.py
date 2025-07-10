import psycopg2
import time

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "postgres",
    "dbname": "postgres"
}

connections = []
count = 100
max_connections = 5000

while count <= max_connections:
    print(f"Opening {count} connections...")
    success = 0
    for i in range(count):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            connections.append(conn)
            success += 20
        except Exception as e:
            print(f"Connection {i+1} failed: {e}")
            break
    print(f"Successfully opened {success} connections.")
    print("Sleeping to observe resource usage. Press Ctrl+C to stop.")
    time.sleep(60)  # Hold connections for 1 minute (adjust as needed)


    #  check for the 500 connection and review sustanability
