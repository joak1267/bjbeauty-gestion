import pymysql
import sqlite3
import os

print("Buscando fragancias Good Girl y agregando reserva para Maria Laura...")

# Conexión a TiDB Cloud
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
    # 1. Insertar reserva de Good Girl para Maria Laura
    sql = """
    INSERT INTO reservas_pedidos (
        cliente, telefono, tipo_producto, nombre_fragancia,
        cantidad, precio_estimado, tipo_operacion, estado, notas
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    cur.execute(sql, (
        'Maria Laura',
        '',
        'perfume',
        'Good Girl (Carolina Herrera)',
        1,
        22000.00,
        'Reserva Cliente',
        'Reservado',
        'Reserva solicitada por Maria Laura junto con La Bomba.'
    ))
    reserva_id = cur.lastrowid
    print(f"Reserva #{reserva_id} creada en TiDB Cloud: Maria Laura - Good Girl (Carolina Herrera)")

    # Actualizar nota en La Bomba
    cur.execute("""
    UPDATE reservas_pedidos 
    SET notas = 'Reserva solicitada por Maria Laura junto con Good Girl.'
    WHERE id = 2;
    """)

    # Mostrar reservas de Maria Laura
    cur.execute("SELECT id, cliente, nombre_fragancia, precio_estimado, estado, notas FROM reservas_pedidos WHERE cliente LIKE '%Maria Laura%';")
    for r in cur.fetchall():
        print(" ->", r)

tidb_con.close()

# También sincronizar en el SQLite local de respaldo
sqlite_path = os.path.join(os.path.dirname(__file__), 'bj_beauty.db')
if os.path.exists(sqlite_path):
    sq = sqlite3.connect(sqlite_path)
    sq.execute("""
    INSERT OR REPLACE INTO reservas_pedidos (
        id, cliente, telefono, tipo_producto, nombre_fragancia,
        cantidad, precio_estimado, tipo_operacion, estado, notas
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        reserva_id,
        'Maria Laura',
        '',
        'perfume',
        'Good Girl (Carolina Herrera)',
        1,
        22000.00,
        'Reserva Cliente',
        'Reservado',
        'Reserva solicitada por Maria Laura junto con La Bomba.'
    ))
    sq.execute("UPDATE reservas_pedidos SET notas = 'Reserva solicitada por Maria Laura junto con Good Girl.' WHERE id = 2;")
    sq.commit()
    sq.close()
    print("Reserva sincronizada también en SQLite local de respaldo.")
