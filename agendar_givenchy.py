# -*- coding: utf-8 -*-
"""
Script para registrar en la base de datos (TiDB Cloud y SQLite local)
los encargos a proveedor de los perfumes Givenchy solicitados.
"""

import os
import sys
import datetime
import sqlite3
import pymysql

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from servidor_db import TIDB_CONFIG, SQLITE_DB_PATH

encargos = [
    {
        'cliente': 'Proveedor / Fábrica',
        'telefono': '',
        'tipo_producto': 'perfume',
        'nombre_fragancia': 'Very Irresistible For Men (Givenchy)',
        'cantidad': 1,
        'precio_estimado': 22000.0,
        'tipo_operacion': 'Encargo Proveedor',
        'estado': 'Por Encargar',
        'notas': 'Encargo a proveedor / reposición de stock. Costo mayorista: $12.000 | Venta catálogo: $22.000.'
    },
    {
        'cliente': 'Proveedor / Fábrica',
        'telefono': '',
        'tipo_producto': 'perfume',
        'nombre_fragancia': 'Pour Homme (Givenchy)',
        'cantidad': 1,
        'precio_estimado': 22000.0,
        'tipo_operacion': 'Encargo Proveedor',
        'estado': 'Por Encargar',
        'notas': 'Encargo a proveedor / reposición de stock. Costo mayorista: $12.000 | Venta catálogo: $22.000.'
    },
    {
        'cliente': 'Proveedor / Fábrica',
        'telefono': '',
        'tipo_producto': 'perfume',
        'nombre_fragancia': 'Gentleman Only Absolut (Givenchy)',
        'cantidad': 1,
        'precio_estimado': 22000.0,
        'tipo_operacion': 'Encargo Proveedor',
        'estado': 'Por Encargar',
        'notas': 'Encargo a proveedor / reposición de stock. Costo mayorista: $12.000 | Venta catálogo: $22.000.'
    },
    {
        'cliente': 'Proveedor / Fábrica',
        'telefono': '',
        'tipo_producto': 'perfume',
        'nombre_fragancia': 'Blue Label (Givenchy)',
        'cantidad': 1,
        'precio_estimado': 22000.0,
        'tipo_operacion': 'Encargo Proveedor',
        'estado': 'Por Encargar',
        'notas': 'Encargo a proveedor / reposición de stock. Costo mayorista: $12.000 | Venta catálogo: $22.000.'
    }
]

def main():
    print("=== REGISTRANDO ENCARGOS GIVENCHY EN BASE DE DATOS ===")
    
    # 1. Conexión a TiDB Cloud
    print("\n1. Conectando a TiDB Cloud (AWS Sao Paulo)...")
    c_tidb = pymysql.connect(**TIDB_CONFIG)
    insertados = []
    with c_tidb.cursor() as cur:
        for item in encargos:
            cur.execute("""
                SELECT id FROM reservas_pedidos 
                WHERE nombre_fragancia = %s AND tipo_operacion = 'Encargo Proveedor' AND estado = 'Por Encargar';
            """, (item['nombre_fragancia'],))
            existente = cur.fetchone()
            if existente:
                print(f"  [EXISTENTE] {item['nombre_fragancia']} (ID: {existente['id']})")
                item['id'] = existente['id']
            else:
                cur.execute("""
                    INSERT INTO reservas_pedidos (
                        fecha, cliente, telefono, tipo_producto, nombre_fragancia,
                        cantidad, precio_estimado, tipo_operacion, estado, notas
                    ) VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    item['cliente'], item['telefono'], item['tipo_producto'], item['nombre_fragancia'],
                    item['cantidad'], item['precio_estimado'], item['tipo_operacion'], item['estado'], item['notas']
                ))
                item['id'] = cur.lastrowid
                print(f"  [INSERTADO] {item['nombre_fragancia']} -> ID {item['id']}")
            insertados.append(item)
    c_tidb.close()
    print("TiDB Cloud actualizado con exito.")

    # 2. Sincronización con SQLite local (bj_beauty.db)
    print("\n2. Sincronizando SQLite local (bj_beauty.db)...")
    c_sq = sqlite3.connect(SQLITE_DB_PATH)
    cur_sq = c_sq.cursor()
    fecha_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for item in insertados:
        cur_sq.execute("""
            INSERT INTO reservas_pedidos (
                id, fecha, cliente, telefono, tipo_producto, nombre_fragancia,
                cantidad, precio_estimado, tipo_operacion, estado, notas, creado_en, actualizado_en
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                cliente = excluded.cliente,
                nombre_fragancia = excluded.nombre_fragancia,
                tipo_operacion = excluded.tipo_operacion,
                estado = excluded.estado,
                notas = excluded.notas;
        """, (
            item['id'], fecha_now, item['cliente'], item['telefono'], item['tipo_producto'], item['nombre_fragancia'],
            item['cantidad'], item['precio_estimado'], item['tipo_operacion'], item['estado'], item['notas'],
            fecha_now, fecha_now
        ))
    c_sq.commit()
    c_sq.close()
    print("SQLite local sincronizado con exito.")

    # 3. Verificacion final de todas las reservas y encargos activos
    print("\n3. Listado actual de Reservas y Encargos activos:")
    c_tidb = pymysql.connect(**TIDB_CONFIG)
    with c_tidb.cursor() as cur:
        cur.execute("SELECT id, fecha, cliente, tipo_operacion, nombre_fragancia, cantidad, estado FROM reservas_pedidos ORDER BY id ASC;")
        todas = cur.fetchall()
        for r in todas:
            print(f"  * ID {r['id']} | {r['tipo_operacion']} | {r['nombre_fragancia']} ({r['cantidad']}u) -> Estado: {r['estado']} | Destino: {r['cliente']}")
    c_tidb.close()
    print("\nOperación completada exitosamente.")

if __name__ == '__main__':
    main()
