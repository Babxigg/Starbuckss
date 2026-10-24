import sqlite3

def init_db():
    conn = sqlite3.connect("inventario.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        precio REAL,
        archivo TEXT,
        estado TEXT DEFAULT 'disponible'
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS ordenes (
        order_id TEXT PRIMARY KEY,
        chat_id INTEGER,
        producto_id INTEGER,
        estado TEXT DEFAULT 'pendiente'
    )""")
    c.execute("SELECT COUNT(*) FROM productos")
    if c.fetchone()[0] == 0:
        productos = [
            (1, "Producto 1", 100, "banca_1.txt"),
            (2, "Producto 2", 150, "banca_2.txt"),
            (3, "Producto 3", 200, "banca_3.txt"),
            (4, "Producto 4", 250, "banca_4.txt"),
            (5, "Producto 5", 300, "banca_5.txt"),
            (6, "Producto 6", 350, "banca_6.txt"),
            (7, "Producto 7", 400, "banca_7.txt"),
            (8, "Producto 8", 450, "banca_8.txt"),
            (9, "Producto 9", 500, "banca_9.txt"),
            (10, "Producto 10", 550, "banca_10.txt"),
        ]
        c.executemany(
            "INSERT INTO productos VALUES (?,?,?,?,'disponible')", productos
        )
    conn.commit()
    conn.close()

def obtener_disponibles():
    conn = sqlite3.connect("inventario.db")
    c = conn.cursor()
    c.execute("SELECT id, nombre, precio FROM productos WHERE estado = 'disponible'")
    resultado = c.fetchall()
    conn.close()
    return resultado
