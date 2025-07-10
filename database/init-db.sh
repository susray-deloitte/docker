#!/bin/bash
set -e

# Create an additional database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE mydb;
    \c mydb
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOSQL