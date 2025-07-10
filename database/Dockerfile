FROM postgres:16

# Set environment variables for default user and database
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=postgres

# Allow connections from the local system by modifying pg_hba.conf and postgresql.conf
# Use Docker's entrypoint to override configs at container start
COPY ./init-db.sh /docker-entrypoint-initdb.d/init-db.sh
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh

EXPOSE 5432