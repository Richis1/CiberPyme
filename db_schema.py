import sqlite3

def extract_schema():
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cur.fetchall()]
    
    with open('schema_output.txt', 'w', encoding='utf-8') as f:
        f.write("=== TABLAS EN LA BASE DE DATOS ===\n\n")
        for table in tables:
            f.write(f"Table: {table}\n")
            cur.execute(f"PRAGMA table_info('{table}');")
            columns = cur.fetchall()
            for col in columns:
                # col structure: (cid, name, type, notnull, dflt_value, pk)
                pk_mark = "(Primary Key)" if col[5] else ""
                not_null = "NOT NULL" if col[3] else "NULL"
                f.write(f"  - {col[1]}: {col[2]} {not_null} {pk_mark}\n")
            f.write("-" * 40 + "\n")
        
    conn.close()
    print("Schema exported to schema_output.txt successfully!")

if __name__ == '__main__':
    extract_schema()
