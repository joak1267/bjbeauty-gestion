import sqlite3
import re
import os

sql_file = os.path.join(os.path.dirname(__file__), 'backup_bj_beauty.sql')
db_path = os.path.join(os.path.dirname(__file__), 'bj_beauty.db')

if os.path.exists(db_path):
    try:
        os.remove(db_path)
    except Exception:
        pass

con = sqlite3.connect(db_path)
cur = con.cursor()

# 1. Compras
cur.execute('''
CREATE TABLE IF NOT EXISTS compras_mercaderia (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fecha TEXT NOT NULL,
  proveedor TEXT NOT NULL DEFAULT 'Proveedor General',
  tipo_producto TEXT NOT NULL DEFAULT 'perfume',
  descripcion TEXT NOT NULL,
  cantidad INTEGER NOT NULL DEFAULT 1,
  costo_unitario REAL NOT NULL DEFAULT 0.00,
  costo_total REAL NOT NULL DEFAULT 0.00,
  metodo_pago TEXT NOT NULL DEFAULT 'Efectivo',
  notas TEXT DEFAULT '',
  creado_en TEXT DEFAULT CURRENT_TIMESTAMP
);
''')

# 2. Reservas
cur.execute('''
CREATE TABLE IF NOT EXISTS reservas_pedidos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fecha TEXT DEFAULT CURRENT_TIMESTAMP,
  cliente TEXT NOT NULL,
  telefono TEXT DEFAULT '',
  tipo_producto TEXT NOT NULL DEFAULT 'perfume',
  nombre_fragancia TEXT NOT NULL,
  cantidad INTEGER NOT NULL DEFAULT 1,
  precio_estimado REAL DEFAULT 0.00,
  tipo_operacion TEXT NOT NULL DEFAULT 'Reserva Cliente',
  estado TEXT NOT NULL DEFAULT 'Pendiente',
  notas TEXT DEFAULT '',
  creado_en TEXT DEFAULT CURRENT_TIMESTAMP,
  actualizado_en TEXT DEFAULT CURRENT_TIMESTAMP
);
''')

# 3. Stock
cur.execute('''
CREATE TABLE IF NOT EXISTS stock (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tipo_producto TEXT NOT NULL,
  categoria TEXT DEFAULT 'Perfume',
  nombre_fragancia TEXT NOT NULL,
  marca TEXT DEFAULT '',
  cantidad INTEGER NOT NULL DEFAULT 0,
  costo_unitario REAL DEFAULT 0.00,
  precio_venta REAL DEFAULT 0.00,
  actualizado_en TEXT DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(tipo_producto, nombre_fragancia, marca)
);
''')

# 4. Ventas
cur.execute('''
CREATE TABLE IF NOT EXISTS ventas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fecha TEXT DEFAULT CURRENT_TIMESTAMP,
  cliente TEXT NOT NULL DEFAULT 'Cliente Mostrador',
  telefono TEXT DEFAULT '',
  tipo_producto TEXT NOT NULL,
  nombre_fragancia TEXT NOT NULL,
  cantidad INTEGER NOT NULL DEFAULT 1,
  precio_unitario REAL NOT NULL,
  costo_unitario REAL NOT NULL DEFAULT 0.00,
  total_venta REAL NOT NULL,
  ganancia_neta REAL NOT NULL,
  metodo_pago TEXT NOT NULL DEFAULT 'Efectivo',
  estado_entrega TEXT NOT NULL DEFAULT 'Entregado',
  notas TEXT DEFAULT NULL,
  creado_en TEXT DEFAULT CURRENT_TIMESTAMP
);
''')

with open(sql_file, 'r', encoding='latin1') as f:
    content = f.read()

inserts = re.findall(r'INSERT INTO `(\w+)` VALUES (.*?);', content, re.DOTALL)
print(f'Bloques encontrados: {len(inserts)}')

for tbl, vals in inserts:
    # Convert escaped quotes \' to ''
    clean_vals = vals.replace(r"\'", "''")
    # Replace backslashes
    clean_vals = clean_vals.replace(r'\"', '"')
    sql = f'INSERT OR REPLACE INTO {tbl} VALUES {clean_vals};'
    try:
        cur.execute(sql)
        print(f'Tabla {tbl} importada con éxito.')
    except Exception as e:
        print(f'Error en {tbl}: {e}')

con.commit()

for t in ['ventas', 'compras_mercaderia', 'reservas_pedidos', 'stock']:
    c = cur.execute(f'SELECT count(*) FROM {t}').fetchone()[0]
    print(f'Total {t}: {c} filas')

con.close()
print('Proceso SQLite completado!')
