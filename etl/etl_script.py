import psycopg2
import os
from sqlalchemy import create_engine, inspect
import pandas as pd

# Database connection details
SOURCE_DB_CONFIG = {
    "dbname": "source_db",
    "user": "root",
    "password": "root",
    "host": "sourcepg",
    "port": "5432",
}

DEST_DB_CONFIG = {
    "dbname": "dest_db",
    "user": "root",
    "password": "root",
    "host": "destpg",
    "port": "5432",
}

# Create SQLAlchemy engines
source_engine = create_engine(
    f"postgresql://{SOURCE_DB_CONFIG['user']}:{SOURCE_DB_CONFIG['password']}@{SOURCE_DB_CONFIG['host']}:{SOURCE_DB_CONFIG['port']}/{SOURCE_DB_CONFIG['dbname']}"
)
dest_engine = create_engine(
    f"postgresql://{DEST_DB_CONFIG['user']}:{DEST_DB_CONFIG['password']}@{DEST_DB_CONFIG['host']}:{DEST_DB_CONFIG['port']}/{DEST_DB_CONFIG['dbname']}"
)

# Get all table names from the source database
inspector = inspect(source_engine)
tables = inspector.get_table_names()
print(f"Found {len(tables)} tables to copy: {tables}")
if not tables:
    print("⚠️ No se encontraron tablas en la base de datos de origen. Verifica la conexión y permisos.")
    exit(1)

# Copy each table from source to destination
for table in tables:
    print(f"📤 Copiando tabla: {table}...")

    # Copiar datos en chunks para evitar alto consumo de memoria
    chunksize = 10000
    for chunk in pd.read_sql(f"SELECT * FROM {table}", source_engine, chunksize=chunksize):
        chunk.to_sql(table, dest_engine, if_exists="append", index=False)

    print(f"✅ Tabla {table} copiada exitosamente.")

# Close connections
source_engine.dispose()
dest_engine.dispose()

print("ETL process completed.")
