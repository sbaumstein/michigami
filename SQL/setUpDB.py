import sqlite3

db_file = "michigami.db"
connection = sqlite3.connect(db_file)

schema_file = "schema.sql"
with open(schema_file, "r") as file:
    schema_script = file.read()

cursor = connection.cursor()
cursor.executescript(schema_script)

connection.commit()
connection.close()

print(f"Database '{db_file}' set up successfully!")
