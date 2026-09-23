# -*- coding: utf-8 -*-
import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='',
    database='bj_beauty_db',
    charset='utf8mb4',
    autocommit=True
)

with conn.cursor() as cur:
    cur.execute("""
        UPDATE ventas 
        SET metodo_pago = 'Transferencia' 
        WHERE cliente LIKE '%Silvia Ferbola%';
    """)
    filas = cur.rowcount
    print(f"Filas actualizadas: {filas}")

    cur.execute("SELECT id, cliente, nombre_fragancia, metodo_pago, total_venta, notas FROM ventas WHERE cliente LIKE '%Silvia Ferbola%';")
    for r in cur.fetchall():
        print("Venta:", r)

conn.close()
