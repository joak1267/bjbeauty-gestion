import sqlite3
import pymysql
import os

print("Iniciando migración a TiDB Cloud...")

# 1. Conexión local a SQLite con los datos verificados
sqlite_path = os.path.join(os.path.dirname(__file__), 'bj_beauty.db')
sq_con = sqlite3.connect(sqlite_path)
sq_con.row_factory = sqlite3.Row

# 2. Conexión a TiDB Cloud
tidb_con = pymysql.connect(
    host='gateway01.sa-east-1.prod.aws.tidbcloud.com',
    port=4000,
    user='2EKaBZP9bt9e87H.root',
    password='wIQ2ebdbi9IhMVWP',
    database='bj_beauty_db',
    ssl_verify_cert=True,
    ssl_verify_identity=True,
    autocommit=True
)

with tidb_con.cursor() as cur:
    print("Creando tablas en TiDB Cloud...")
    
    # 1. compras_mercaderia
    cur.execute("""
    CREATE TABLE IF NOT EXISTS compras_mercaderia (
      id int(11) NOT NULL AUTO_INCREMENT,
      fecha date NOT NULL,
      proveedor varchar(150) NOT NULL DEFAULT 'Proveedor General',
      tipo_producto varchar(50) NOT NULL DEFAULT 'perfume',
      descripcion varchar(255) NOT NULL,
      cantidad int(11) NOT NULL DEFAULT 1,
      costo_unitario decimal(10,2) NOT NULL DEFAULT 0.00,
      costo_total decimal(10,2) NOT NULL DEFAULT 0.00,
      metodo_pago varchar(50) NOT NULL DEFAULT 'Efectivo',
      notas text DEFAULT NULL,
      creado_en datetime DEFAULT current_timestamp(),
      PRIMARY KEY (id)
    );
    """)

    # 2. reservas_pedidos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reservas_pedidos (
      id int(11) NOT NULL AUTO_INCREMENT,
      fecha datetime DEFAULT current_timestamp(),
      cliente varchar(150) NOT NULL,
      telefono varchar(50) DEFAULT '',
      tipo_producto varchar(50) NOT NULL DEFAULT 'perfume',
      nombre_fragancia varchar(150) NOT NULL,
      cantidad int(11) NOT NULL DEFAULT 1,
      precio_estimado decimal(10,2) DEFAULT 0.00,
      tipo_operacion varchar(50) NOT NULL DEFAULT 'Reserva Cliente',
      estado varchar(50) NOT NULL DEFAULT 'Pendiente',
      notas text DEFAULT NULL,
      creado_en datetime DEFAULT current_timestamp(),
      actualizado_en datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
      PRIMARY KEY (id)
    );
    """)

    # 3. stock
    cur.execute("""
    CREATE TABLE IF NOT EXISTS stock (
      id int(11) NOT NULL AUTO_INCREMENT,
      tipo_producto varchar(50) NOT NULL,
      categoria varchar(80) DEFAULT 'Perfume',
      nombre_fragancia varchar(150) NOT NULL,
      marca varchar(100) DEFAULT '',
      cantidad int(11) NOT NULL DEFAULT 0,
      costo_unitario decimal(10,2) DEFAULT 0.00,
      precio_venta decimal(10,2) DEFAULT 0.00,
      actualizado_en datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
      PRIMARY KEY (id),
      UNIQUE KEY uq_stock_full (tipo_producto, nombre_fragancia, marca)
    );
    """)

    # 4. ventas
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
      id int(11) NOT NULL AUTO_INCREMENT,
      fecha datetime DEFAULT current_timestamp(),
      cliente varchar(150) NOT NULL DEFAULT 'Cliente Mostrador',
      telefono varchar(50) DEFAULT '',
      tipo_producto varchar(50) NOT NULL,
      nombre_fragancia varchar(150) NOT NULL,
      cantidad int(11) NOT NULL DEFAULT 1,
      precio_unitario decimal(10,2) NOT NULL,
      costo_unitario decimal(10,2) NOT NULL DEFAULT 0.00,
      total_venta decimal(10,2) NOT NULL,
      ganancia_neta decimal(10,2) NOT NULL,
      metodo_pago varchar(50) NOT NULL DEFAULT 'Efectivo',
      estado_entrega varchar(50) NOT NULL DEFAULT 'Entregado',
      notas text DEFAULT NULL,
      creado_en datetime DEFAULT current_timestamp(),
      PRIMARY KEY (id)
    );
    """)

    # Copiar compras
    compras = sq_con.execute("SELECT * FROM compras_mercaderia").fetchall()
    for c in compras:
        cur.execute("""
        INSERT INTO compras_mercaderia (id, fecha, proveedor, tipo_producto, descripcion, cantidad, costo_unitario, costo_total, metodo_pago, notas, creado_en)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE id=id;
        """, tuple(c))
    print(f"Compras migradas: {len(compras)}")

    # Copiar reservas
    reservas = sq_con.execute("SELECT * FROM reservas_pedidos").fetchall()
    for r in reservas:
        cur.execute("""
        INSERT INTO reservas_pedidos (id, fecha, cliente, telefono, tipo_producto, nombre_fragancia, cantidad, precio_estimado, tipo_operacion, estado, notas, creado_en, actualizado_en)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE id=id;
        """, tuple(r))
    print(f"Reservas migradas: {len(reservas)}")

    # Copiar stock
    stock = sq_con.execute("SELECT * FROM stock").fetchall()
    for s in stock:
        cur.execute("""
        INSERT INTO stock (id, tipo_producto, categoria, nombre_fragancia, marca, cantidad, costo_unitario, precio_venta, actualizado_en)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE cantidad=VALUES(cantidad), precio_venta=VALUES(precio_venta), costo_unitario=VALUES(costo_unitario);
        """, tuple(s))
    print(f"Stock migrado: {len(stock)} fragancias")

    # Copiar ventas
    ventas = sq_con.execute("SELECT * FROM ventas").fetchall()
    for v in ventas:
        cur.execute("""
        INSERT INTO ventas (id, fecha, cliente, telefono, tipo_producto, nombre_fragancia, cantidad, precio_unitario, costo_unitario, total_venta, ganancia_neta, metodo_pago, estado_entrega, notas, creado_en)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE id=id;
        """, tuple(v))
    print(f"Ventas migradas: {len(ventas)}")

tidb_con.close()
sq_con.close()
print("¡MIGRACIÓN A TIDB CLOUD COMPLETADA CON ÉXITO!")
