import psycopg2
import time
import threading

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "postgres",
    "dbname": "postgres"
}

connections = []
count = 100
max_connections = 1000  # Set this to your new max_connections

def cpu_stress(duration=600):
    # Busy loop for 'duration' seconds
    end_time = time.time() + duration
    while time.time() < end_time:
        x = 0
        for i in range(10000):
            x += i*i

while count <= max_connections:
    print(f"Opening {count} connections...")
    success = 0
    threads = []
    for i in range(count):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            connections.append(conn)
            # Start a CPU stress thread for each connection
            t = threading.Thread(target=cpu_stress, args=(600,))
            t.daemon = True
            t.start()
            threads.append(t)
            success += 1
        except Exception as e:
            print(f"Connection {i+1} failed: {e}")
            break
    print(f"Successfully opened {success} connections.")
    print("Sleeping to observe resource usage. Press Ctrl+C to stop.")
    time.sleep(60)  # Hold connections for 1 minute (adjust as needed)
