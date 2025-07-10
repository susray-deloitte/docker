# Project Overview

This repository provides a setup for running a PostgreSQL database and monitoring its metrics (CPU, RAM, and connections) using Prometheus, Grafana, cAdvisor, and postgres_exporter. Each service is containerized using Docker.

---
# Directory Structure

```
.
├── README.md
├── database
│   ├── Dockerfile
│   ├── init-db.sh
│   ├── pg_db_connection_cpu.py
│   └── pg_db_connection_ram.py
└── monitoring
    ├── Dockerfile.cadvisor
    ├── Dockerfile.grafana
    ├── Dockerfile.postgresExporter
    ├── Dockerfile.prometheus
    └── prometheus.yml
```

---
# 1. Docker Network Setup

Create a custom Docker network named `monitoring` to allow containers to communicate:

```bash
docker network create monitoring
```
---
# 2. Build Docker Images

Navigate to each relevant directory and build the Docker images using the provided Dockerfiles.

Database Image

```bash
cd database
docker build -t my_postgres_db -f Dockerfile .
```

Monitoring Images

```bash
cd ../monitoring

cAdvisor
docker build -t my_cadvisor -f Dockerfile.cadvisor .

Prometheus
docker build -t my_prometheus -f Dockerfile.prometheus .

Grafana
docker build -t my_grafana -f Dockerfile.grafana .

Postgres Exporter
docker build -t my_postgres_exporter -f Dockerfile.postgresExporter .
```
---
# 3. Run Docker Containers

Run each container on the `monitoring` network:

**PostgreSQL Database**

```bash
docker run -d --name postgres-db --network monitoring my_postgres_db
```

**cAdvisor**

```bash
docker run -d --name cadvisor --network monitoring \
    -v /:/rootfs:ro \
    -v /var/run:/var/run:ro \
    -v /sys:/sys:ro \
    -v /var/lib/docker/:/var/lib/docker:ro \
my_cadvisor
```

**Prometheus**

```bash
docker run -d --name prometheus --network monitoring \
    -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
my_prometheus
```

**Postgres Exporter**

```bash
docker run -d --name postgres_exporter --network monitoring \
    -e DATA_SOURCE_NAME="postgresql://<user>:<password>@postgres-db:5432/<db>?sslmode=disable" \
my_postgres_exporter
```

**Grafana**

```bash
docker run -d --name grafana --network monitoring -p 3000:3000 my_grafana
```
---
# 4. Grafana Dashboard Setup

1. Access Grafana:
Open [http://localhost:3000](http://localhost:3000) in your browser.

2. **Login:**
Default credentials are usually `admin` / `admin`.

3. Add Prometheus Data Source:
    - Go to Configuration > Data Sources.
    - Click Add data source.
    - Choose Prometheus.
    - Set the URL to `http://prometheus:9090` (since both are on the same Docker network).
    - Click Save & Test.

4. Create a New Dashboard:

    ``` bash
    Click + > Dashboard > Add new panel.
    ```

5. PromQL Queries for Metrics

CPU Utilization (%)

```promql
sum by (name) (
rate(container_cpu_usage_seconds_total{name="postgres-db"}[1m])
) * 100
```

RAM Utilization (%)

```promql
(
container_memory_usage_bytes{name="postgres-db"}
/
container_spec_memory_limit_bytes{name="postgres-db"}
) * 100
```

Number of PostgreSQL Connections

If using postgres_exporter:

```promql
pg_stat_activity_count{job="postgres_exporter"}
```
or
```promql
pg_stat_activity_count{datname="<your_database_name>"}
```


6. Grafana Gauge Panel Configuration

    - Query: Use the PromQL queries above.
    - Visualization: Set to Gauge.
    - Unit: Percent (`%`) for CPU and RAM; Number for connections.
    - Thresholds:
    - For CPU/RAM, set a threshold at 90 to change color to red when exceeded.

7. Additional Notes

    - Replace `<user>`, `<password>`, and `<db>` in the Postgres Exporter run command with your actual database credentials.
    - Make sure your Prometheus configuration (`prometheus.yml`) is set up to scrape metrics from cAdvisor and postgres_exporter.

8. Stopping and Removing Containers

To stop all containers:

```bash
docker stop postgres-db cadvisor prometheus postgres_exporter grafana
```

To remove all containers:

```bash
docker rm postgres-db cadvisor prometheus postgres_exporter grafana
```


9. References

    - [Prometheus Documentation](https://prometheus.io/docs/)
    - [Grafana Documentation](https://grafana.com/docs/)
    - [cAdvisor Documentation](https://github.com/google/cadvisor)
    - [postgres_exporter Documentation](https://github.com/prometheus-community/postgres_exporter)
    - [Docker documentation](https://docs.docker.com/reference/cli/docker/)

    ---

Feel free to modify the queries or configuration files as needed for your environment!
