# -*- coding: utf-8 -*-
"""
Script de sincronización e inicialización:
1. Asegura estructura de tablas: stock y reservas_pedidos
2. Extrae y carga todos los perfumes y productos del catálogo (PDFs) en MySQL
3. Registra las ventas y reservas solicitadas (Silvia Ferbola, Maria Laura, Gabriela Nicola, Erba Pura)
"""

import os
import json
import pymysql

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_db():
    return pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='',
        database='bj_beauty_db',
        charset='utf8mb4',
        autocommit=True
    )

def setup_tables(conn):
    with conn.cursor() as cur:
        # 1. Crear tabla reservas_pedidos
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reservas_pedidos (
                id INT(11) NOT NULL AUTO_INCREMENT,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                cliente VARCHAR(150) NOT NULL,
                telefono VARCHAR(50) DEFAULT '',
                tipo_producto VARCHAR(50) NOT NULL DEFAULT 'perfume',
                nombre_fragancia VARCHAR(150) NOT NULL,
                cantidad INT(11) NOT NULL DEFAULT 1,
                precio_estimado DECIMAL(10,2) DEFAULT 0.00,
                tipo_operacion VARCHAR(50) NOT NULL DEFAULT 'Reserva Cliente',
                estado VARCHAR(50) NOT NULL DEFAULT 'Pendiente',
                notas TEXT DEFAULT NULL,
                creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
                actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # 2. Revisar stock y agregar columna categoria si no existe
        cur.execute("DESCRIBE stock;")
        cols = [r[0] for r in cur.fetchall()]
        if 'categoria' not in cols:
            cur.execute("ALTER TABLE stock ADD COLUMN categoria VARCHAR(80) DEFAULT 'Perfume' AFTER tipo_producto;")
            print("Columna 'categoria' agregada a tabla stock.")

        # 3. Ajustar indice unico para que permita misma fragancia en masc/fem
        cur.execute("SHOW INDEX FROM stock;")
        indexes = [r[2] for r in cur.fetchall()]
        if 'uq_prod' in indexes:
            cur.execute("ALTER TABLE stock DROP INDEX uq_prod;")
            print("Indice antiguo 'uq_prod' eliminado.")
        if 'uq_stock_full' not in indexes:
            cur.execute("ALTER TABLE stock ADD UNIQUE KEY uq_stock_full (tipo_producto, nombre_fragancia, marca);")
            print("Nuevo indice unico 'uq_stock_full' creado.")

def cargar_catalogo_stock(conn):
    # Cargar JSONs fuentes oficiales de los catálogos en PDF
    fem_path = os.path.join(BASE_DIR, 'fem.json')
    masc_path = os.path.join(BASE_DIR, 'masc.json')
    otros_path = os.path.join(BASE_DIR, 'otros.json')

    with open(fem_path, 'r', encoding='utf-8') as f:
        fem = json.load(f)
    with open(masc_path, 'r', encoding='utf-8') as f:
        masc = json.load(f)
    with open(otros_path, 'r', encoding='utf-8') as f:
        otros = json.load(f)

    productos = []

    # 1. Femeninos (222)
    for p in fem:
        nombre = p[0].strip()
        marca = p[1].strip() if len(p) > 1 else 'Genérica'
        productos.append({
            'tipo_producto': 'perfume',
            'categoria': 'Perfumería Clásica Femenina',
            'nombre_fragancia': nombre,
            'marca': marca,
            'costo_unitario': 12000.0,
            'precio_venta': 22000.0,
            'cantidad': 0
        })

    # 2. Masculinos (210)
    for p in masc:
        nombre = p[0].strip()
        marca = p[1].strip() if len(p) > 1 else 'Genérica'
        productos.append({
            'tipo_producto': 'perfume',
            'categoria': 'Perfumería Clásica Masculina',
            'nombre_fragancia': nombre,
            'marca': marca,
            'costo_unitario': 12000.0,
            'precio_venta': 22000.0,
            'cantidad': 0
        })

    # 3. Perfumería Árabe
    for p in otros.get('arabes_fem', []):
        productos.append({
            'tipo_producto': 'fusion',
            'categoria': 'Perfumería Árabe Femenina',
            'nombre_fragancia': p[0].strip(),
            'marca': p[1].strip() if len(p) > 1 else 'Lattafa / Oriental',
            'costo_unitario': 12000.0,
            'precio_venta': 24000.0,
            'cantidad': 0
        })
    for p in otros.get('arabes_masc', []):
        productos.append({
            'tipo_producto': 'fusion',
            'categoria': 'Perfumería Árabe Masculina',
            'nombre_fragancia': p[0].strip(),
            'marca': p[1].strip() if len(p) > 1 else 'Afnan / Lattafa',
            'costo_unitario': 12000.0,
            'precio_venta': 24000.0,
            'cantidad': 0
        })
    for p in otros.get('arabes_unisex', []):
        productos.append({
            'tipo_producto': 'fusion',
            'categoria': 'Perfumería Árabe Unisex',
            'nombre_fragancia': p[0].strip(),
            'marca': p[1].strip() if len(p) > 1 else 'Oriental Exclusivo',
            'costo_unitario': 12000.0,
            'precio_venta': 24000.0,
            'cantidad': 0
        })

    # 4. Unisex / Nicho
    for p in otros.get('unisex', []):
        productos.append({
            'tipo_producto': 'perfume',
            'categoria': 'Perfumes Unisex & Nicho',
            'nombre_fragancia': p[0].strip(),
            'marca': p[1].strip() if len(p) > 1 else 'Alta Gama',
            'costo_unitario': 12000.0,
            'precio_venta': 22000.0,
            'cantidad': 0
        })

    # 5. Cápsula Fusión
    for p in otros.get('fusion', []):
        productos.append({
            'tipo_producto': 'fusion',
            'categoria': 'Cápsula Fusión Exclusiva',
            'nombre_fragancia': p[0].strip(),
            'marca': p[1].strip() if len(p) > 1 else 'BJ Beauty Special',
            'costo_unitario': 12000.0,
            'precio_venta': 24000.0,
            'cantidad': 0
        })

    # 6. Nuevos Ingresos
    for p in otros.get('nuevos_fem', []):
        productos.append({
            'tipo_producto': 'perfume',
            'categoria': 'Nuevos Ingresos Femeninos',
            'nombre_fragancia': p[0].strip(),
            'marca': p[1].strip() if len(p) > 1 else 'Tendencia',
            'costo_unitario': 12000.0,
            'precio_venta': 22000.0,
            'cantidad': 0
        })
    for p in otros.get('nuevos_masc', []):
        productos.append({
            'tipo_producto': 'perfume',
            'categoria': 'Nuevos Ingresos Masculinos',
            'nombre_fragancia': p[0].strip(),
            'marca': p[1].strip() if len(p) > 1 else 'Tendencia',
            'costo_unitario': 12000.0,
            'precio_venta': 22000.0,
            'cantidad': 0
        })

    # 7. Línea Automotor & Textil (13 aromas)
    for p in otros.get('auto', []):
        productos.append({
            'tipo_producto': 'combo',
            'categoria': 'Línea Automotor & Textil',
            'nombre_fragancia': p[0].strip(),
            'marca': p[1].strip() if len(p) > 1 else 'BJ Beauty Auto',
            'costo_unitario': 6000.0,
            'precio_venta': 11000.0,
            'cantidad': 0
        })

    insertados = 0
    actualizados = 0

    with conn.cursor() as cur:
        sql = """
            INSERT INTO stock (
                tipo_producto, categoria, nombre_fragancia, marca,
                cantidad, costo_unitario, precio_venta
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                categoria = VALUES(categoria),
                costo_unitario = VALUES(costo_unitario),
                precio_venta = VALUES(precio_venta);
        """
        for prod in productos:
            res = cur.execute(sql, (
                prod['tipo_producto'],
                prod['categoria'],
                prod['nombre_fragancia'],
                prod['marca'],
                prod['cantidad'],
                prod['costo_unitario'],
                prod['precio_venta']
            ))
            if res == 1:
                insertados += 1
            elif res == 2:
                actualizados += 1

    print(f"Catálogo sincronizado con stock en MySQL: {insertados} insertados, {actualizados} actualizados. Total productos: {len(productos)}")

def registrar_pedidos_usuario(conn):
    with conn.cursor() as cur:
        # A) Venta Silvia Ferbola: 2 Perfumes (My Way + Scandal) 2x $40.000
        cur.execute("SELECT id FROM ventas WHERE cliente LIKE '%Silvia Ferbola%' AND nombre_fragancia LIKE '%My Way%';")
        existe_v = cur.fetchone()
        if not existe_v:
            # Insertar como 2 renglones o venta clara con promo aplicada
            cur.execute("""
                INSERT INTO ventas (
                    fecha, cliente, telefono, tipo_producto, nombre_fragancia,
                    cantidad, precio_unitario, costo_unitario, total_venta,
                    ganancia_neta, metodo_pago, estado_entrega, notas
                ) VALUES 
                (
                    NOW(), 'Silvia Ferbola', '', 'perfume', 'My Way (Giorgio Armani)',
                    1, 20000.00, 12000.00, 20000.00, 8000.00, 'Transferencia', 'Cobrado',
                    'Promo 2 Perfumes x $40.000 (1/2) - Silvia a confirmar aromatizante'
                ),
                (
                    NOW(), 'Silvia Ferbola', '', 'perfume', 'Scandal (Jean Paul Gaultier)',
                    1, 20000.00, 12000.00, 20000.00, 8000.00, 'Transferencia', 'Cobrado',
                    'Promo 2 Perfumes x $40.000 (2/2) - Silvia a confirmar aromatizante'
                );
            """)
            print("Venta de Silvia Ferbola (My Way + Scandal 2x $40.000) registrada con éxito.")
        else:
            print("Venta de Silvia Ferbola ya existía en la base de datos.")

        # B) Reservas y Encargos en reservas_pedidos
        # 1. Silvia a confirmar aromatizante
        cur.execute("SELECT id FROM reservas_pedidos WHERE cliente LIKE '%Silvia%' AND nombre_fragancia LIKE '%Aromatizante%';")
        if not cur.fetchone():
            cur.execute("""
                INSERT INTO reservas_pedidos (
                    fecha, cliente, telefono, tipo_producto, nombre_fragancia,
                    cantidad, precio_estimado, tipo_operacion, estado, notas
                ) VALUES (
                    NOW(), 'Silvia Ferbola', '', 'combo', 'Aromatizante Auto/Textil (Aroma a definir)',
                    1, 11000.00, 'A Confirmar', 'Pendiente de Confirmación',
                    'Silvia tiene a confirmar qué fragancia de aromatizante desea.'
                );
            """)
            print("Reserva/Pendiente de Silvia Ferbola registrado.")

        # 2. Maria Laura Reservar la Bomba
        cur.execute("SELECT id FROM reservas_pedidos WHERE cliente LIKE '%Maria Laura%' AND nombre_fragancia LIKE '%Bomba%';")
        if not cur.fetchone():
            cur.execute("""
                INSERT INTO reservas_pedidos (
                    fecha, cliente, telefono, tipo_producto, nombre_fragancia,
                    cantidad, precio_estimado, tipo_operacion, estado, notas
                ) VALUES (
                    NOW(), 'Maria Laura', '', 'perfume', 'La Bomba (Carolina Herrera)',
                    1, 22000.00, 'Reserva Cliente', 'Reservado',
                    'Reserva solicitada por Maria Laura.'
                );
            """)
            print("Reserva de Maria Laura (La Bomba) registrada.")

        # 3. Gabriela Nicola Reservar Ange ou Demon Le Secret Elixir
        cur.execute("SELECT id FROM reservas_pedidos WHERE cliente LIKE '%Gabriela Nicola%' AND nombre_fragancia LIKE '%Ange ou Demon%';")
        if not cur.fetchone():
            cur.execute("""
                INSERT INTO reservas_pedidos (
                    fecha, cliente, telefono, tipo_producto, nombre_fragancia,
                    cantidad, precio_estimado, tipo_operacion, estado, notas
                ) VALUES (
                    NOW(), 'Gabriela Nicola', '', 'perfume', 'Ange ou Demon Le Secret Elixir (Givenchy)',
                    1, 22000.00, 'Reserva Cliente', 'Reservado',
                    'Reserva solicitada por Gabriela Nicola.'
                );
            """)
            print("Reserva de Gabriela Nicola (Ange ou Demon Le Secret Elixir) registrada.")

        # 4. Encargar Aromatizante Erba Pura
        cur.execute("SELECT id FROM reservas_pedidos WHERE cliente LIKE '%Proveedor%' AND nombre_fragancia LIKE '%Erba Pura%';")
        if not cur.fetchone():
            cur.execute("""
                INSERT INTO reservas_pedidos (
                    fecha, cliente, telefono, tipo_producto, nombre_fragancia,
                    cantidad, precio_estimado, tipo_operacion, estado, notas
                ) VALUES (
                    NOW(), 'Proveedor / Fábrica', '', 'combo', 'Aromatizante Erba Pura (Línea Auto/Textil #6)',
                    1, 6000.00, 'Encargo Proveedor', 'Por Encargar',
                    'Encargar Aromatizante Erba Pura para reposición de stock.'
                );
            """)
            print("Encargo de Erba Pura a proveedor registrado.")

if __name__ == '__main__':
    conn = get_db()
    print("Conectado a MySQL:", conn.get_server_info())
    setup_tables(conn)
    cargar_catalogo_stock(conn)
    registrar_pedidos_usuario(conn)
    conn.close()
    print("¡Proceso de base de datos finalizado con éxito!")
