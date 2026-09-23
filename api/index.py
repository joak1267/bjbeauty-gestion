# -*- coding: utf-8 -*-
"""
Servidor Backend BJ BEAUTY - Conexión con MySQL Local
Base de datos: bj_beauty_db (XAMPP / MariaDB)
"""

import os
import sys
from datetime import datetime, date
from decimal import Decimal
from flask import Flask, request, jsonify, send_from_directory
import sqlite3
try:
    import pymysql
    from pymysql.cursors import DictCursor
    HAS_PYMYSQL = True
except ImportError:
    HAS_PYMYSQL = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DB_PATH = os.path.join(BASE_DIR, 'bj_beauty.db')

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')
try:
    from flask_cors import CORS
    CORS(app)
except Exception:
    pass

class PathFixMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        matched = (
            environ.get('HTTP_X_MATCHED_PATH') or
            environ.get('x-matched-path') or
            environ.get('HTTP_X_FORWARDED_URI') or
            environ.get('REQUEST_URI') or
            environ.get('RAW_URI')
        )
        if matched:
            path = matched.split('?')[0]
            if path:
                environ['PATH_INFO'] = path
        return self.wsgi_app(environ, start_response)

app.wsgi_app = PathFixMiddleware(app.wsgi_app)


TIDB_CONFIG = {
    'host': os.environ.get('TIDB_HOST', 'gateway01.sa-east-1.prod.aws.tidbcloud.com'),
    'port': int(os.environ.get('TIDB_PORT', 4000)),
    'user': os.environ.get('TIDB_USER', '2EKaBZP9bt9e87H.root'),
    'password': os.environ.get('TIDB_PASSWORD', 'wIQ2ebdbi9IhMVWP'),
    'database': os.environ.get('TIDB_DATABASE', 'bj_beauty_db'),
    'charset': 'utf8mb4',
    'cursorclass': DictCursor if HAS_PYMYSQL else None,
    'autocommit': True,
    'ssl_verify_cert': True,
    'ssl_verify_identity': True
}

LOCAL_MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'bj_beauty_db',
    'charset': 'utf8mb4',
    'cursorclass': DictCursor if HAS_PYMYSQL else None,
    'autocommit': True
}

class SQLiteCursorWrapper:
    def __init__(self, con):
        self.con = con
        self.cur = con.cursor()
        self.lastrowid = None
        self.rowcount = 0

    def execute(self, sql, params=None):
        sql = sql.replace('%s', '?').replace('GREATEST(0,', 'MAX(0,')
        if params is None:
            self.cur.execute(sql)
        else:
            self.cur.execute(sql, params)
        self.lastrowid = self.cur.lastrowid
        self.rowcount = self.cur.rowcount
        return self

    def fetchone(self):
        row = self.cur.fetchone()
        return dict(row) if row else None

    def fetchall(self):
        return [dict(r) for r in self.cur.fetchall()]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self.con.commit()

class SQLiteConnWrapper:
    def __init__(self, db_path):
        self.con = sqlite3.connect(db_path, check_same_thread=False)
        self.con.row_factory = sqlite3.Row

    def cursor(self):
        return SQLiteCursorWrapper(self.con)

    def close(self):
        self.con.close()

def get_db_connection():
    # 1. Intentar conectar a TiDB Cloud (Nube 24/7)
    if HAS_PYMYSQL:
        try:
            c = pymysql.connect(**TIDB_CONFIG)
            c.motor_name = 'TiDB Cloud (AWS Sao Paulo)'
            c.db_name = TIDB_CONFIG['database']
            return c
        except Exception as e:
            print("Fallo conexion TiDB:", e)
    # 2. Fallback a MySQL Local (si está prendido XAMPP)
    if HAS_PYMYSQL:
        try:
            c = pymysql.connect(**LOCAL_MYSQL_CONFIG)
            c.motor_name = 'MySQL Local (XAMPP)'
            c.db_name = LOCAL_MYSQL_CONFIG['database']
            return c
        except Exception:
            pass
    # 3. Fallback a SQLite local
    c = SQLiteConnWrapper(SQLITE_DB_PATH)
    c.motor_name = 'SQLite Local'
    c.db_name = 'bj_beauty.db'
    return c

def serializar_fila(row):
    resultado = {}
    for k, v in row.items():
        if isinstance(v, Decimal):
            resultado[k] = float(v)
        elif isinstance(v, (datetime, date)):
            resultado[k] = v.isoformat()
        else:
            resultado[k] = v
    return resultado

@app.route('/')
def root():
    html_path = os.path.join(os.path.dirname(BASE_DIR), 'sistema_ventas_y_ganancias.html')
    if os.path.exists(html_path):
        return send_from_directory(os.path.dirname(BASE_DIR), 'sistema_ventas_y_ganancias.html')
    return send_from_directory(BASE_DIR, 'sistema_ventas_y_ganancias.html')

@app.route('/api/debug', methods=['GET'])
@app.route('/debug', methods=['GET'])
def api_debug():
    return jsonify({
        'status': 'ok',
        'path': request.path,
        'path_info': request.environ.get('PATH_INFO'),
        'matched_path': request.environ.get('HTTP_X_MATCHED_PATH')
    })

@app.route('/api/estado', methods=['GET'])
@app.route('/estado', methods=['GET'])
def api_estado():
    try:
        conn = get_db_connection()
        motor_label = getattr(conn, 'motor_name', 'TiDB Cloud')
        db_label = getattr(conn, 'db_name', 'bj_beauty_db')
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS total_ventas FROM ventas;")
            res_v = cur.fetchone()
            cur.execute("SELECT COUNT(*) AS total_stock, COALESCE(SUM(cantidad), 0) AS unidades_stock FROM stock;")
            res_s = cur.fetchone()
            cur.execute("SELECT COUNT(*) AS total_compras FROM compras_mercaderia;")
            res_c = cur.fetchone()
            cur.execute("SELECT COUNT(*) AS total_reservas FROM reservas_pedidos WHERE estado != 'Entregado' AND estado != 'Cancelado';")
            res_r = cur.fetchone()
        conn.close()
        return jsonify({
            'status': 'ok',
            'conexion': 'activa',
            'motor': motor_label,
            'base_datos': db_label,
            'ventas_registradas': res_v['total_ventas'],
            'stock_registrado': res_s['total_stock'],
            'unidades_en_stock': res_s['unidades_stock'],
            'compras_registradas': res_c['total_compras'] if res_c else 0,
            'reservas_activas': res_r['total_reservas'] if res_r else 0
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'conexion': 'desconectado',
            'mensaje': str(e)
        }), 500

@app.route('/api/ventas', methods=['GET'])
@app.route('/ventas', methods=['GET'])
def get_ventas():
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM ventas ORDER BY fecha DESC, id DESC;")
            filas = cur.fetchall()
        conn.close()
        
        ventas = []
        for r in filas:
            fila_serial = serializar_fila(r)
            fila_serial['tipo'] = fila_serial.get('tipo_producto')
            fila_serial['fragancia'] = fila_serial.get('nombre_fragancia')
            fila_serial['precioVenta'] = fila_serial.get('precio_unitario')
            fila_serial['costoUnitario'] = fila_serial.get('costo_unitario')
            fila_serial['medioPago'] = fila_serial.get('metodo_pago')
            fila_serial['estadoPago'] = fila_serial.get('estado_entrega')
            
            if 'fecha' in fila_serial and fila_serial['fecha']:
                if 'T' in str(fila_serial['fecha']):
                    fila_serial['fecha'] = str(fila_serial['fecha']).split('T')[0]
            ventas.append(fila_serial)
            
        return jsonify({'ok': True, 'ventas': ventas})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/ventas', methods=['POST'])
@app.route('/ventas', methods=['POST'])
def add_venta():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({'ok': False, 'error': 'No se enviaron datos'}), 400

        fecha_str = data.get('fecha') or datetime.now().strftime('%Y-%m-%d')
        cliente = (data.get('cliente') or 'Cliente').strip()
        telefono = (data.get('telefono') or '').strip()
        tipo = data.get('tipo') or data.get('tipo_producto') or 'perfume'
        fragancia = data.get('fragancia') or data.get('nombre_fragancia') or 'Fragancia'
        cantidad = int(data.get('cantidad', 1))
        precio_unitario = float(data.get('precioVenta') or data.get('precio_unitario', 0))
        costo_unitario = float(data.get('costoUnitario') or data.get('costo_unitario', 0))
        medio_pago = data.get('medioPago') or data.get('metodo_pago') or 'Efectivo'
        estado_pago = data.get('estadoPago') or data.get('estado_entrega') or 'Cobrado'
        notas = data.get('notas', '')

        total_venta = precio_unitario * cantidad
        ganancia_neta = (precio_unitario - costo_unitario) * cantidad

        conn = get_db_connection()
        with conn.cursor() as cur:
            sql = """
                INSERT INTO ventas (
                    fecha, cliente, telefono, tipo_producto, nombre_fragancia,
                    cantidad, precio_unitario, costo_unitario, total_venta,
                    ganancia_neta, metodo_pago, estado_entrega, notas
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cur.execute(sql, (
                fecha_str, cliente, telefono, tipo, fragancia,
                cantidad, precio_unitario, costo_unitario, total_venta,
                ganancia_neta, medio_pago, estado_pago, notas
            ))
            nuevo_id = cur.lastrowid
        conn.close()

        nueva_venta = {
            'id': nuevo_id,
            'fecha': fecha_str,
            'cliente': cliente,
            'telefono': telefono,
            'tipo': tipo,
            'tipo_producto': tipo,
            'fragancia': fragancia,
            'nombre_fragancia': fragancia,
            'cantidad': cantidad,
            'precioVenta': precio_unitario,
            'precio_unitario': precio_unitario,
            'costoUnitario': costo_unitario,
            'costo_unitario': costo_unitario,
            'total_venta': total_venta,
            'ganancia_neta': ganancia_neta,
            'medioPago': medio_pago,
            'metodo_pago': medio_pago,
            'estadoPago': estado_pago,
            'estado_entrega': estado_pago,
            'notas': notas
        }

        return jsonify({'ok': True, 'venta': nueva_venta}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/ventas/<int:venta_id>', methods=['DELETE'])
@app.route('/ventas/<int:venta_id>', methods=['DELETE'])
def delete_venta(venta_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM ventas WHERE id = %s;", (venta_id,))
            afectadas = cur.rowcount
        conn.close()
        return jsonify({'ok': True, 'eliminadas': afectadas})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/ventas/migrar', methods=['POST'])
@app.route('/ventas/migrar', methods=['POST'])
def migrar_ventas():
    try:
        data = request.get_json(force=True)
        items = data.get('ventas', [])
        if not items:
            return jsonify({'ok': True, 'importadas': 0})

        conn = get_db_connection()
        importadas = 0
        with conn.cursor() as cur:
            for item in items:
                fecha_str = item.get('fecha') or datetime.now().strftime('%Y-%m-%d')
                cliente = (item.get('cliente') or 'Cliente').strip()
                tipo = item.get('tipo') or item.get('tipo_producto') or 'perfume'
                fragancia = item.get('fragancia') or item.get('nombre_fragancia') or 'Fragancia'
                cantidad = int(item.get('cantidad', 1))
                precio_unitario = float(item.get('precioVenta') or item.get('precio_unitario', 0))
                costo_unitario = float(item.get('costoUnitario') or item.get('costo_unitario', 0))
                medio_pago = item.get('medioPago') or item.get('metodo_pago') or 'Efectivo'
                estado_pago = item.get('estadoPago') or item.get('estado_entrega') or 'Cobrado'

                total_venta = precio_unitario * cantidad
                ganancia_neta = (precio_unitario - costo_unitario) * cantidad

                cur.execute("""
                    INSERT INTO ventas (
                        fecha, cliente, tipo_producto, nombre_fragancia,
                        cantidad, precio_unitario, costo_unitario, total_venta,
                        ganancia_neta, metodo_pago, estado_entrega
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    fecha_str, cliente, tipo, fragancia,
                    cantidad, precio_unitario, costo_unitario, total_venta,
                    ganancia_neta, medio_pago, estado_pago
                ))
                importadas += 1
        conn.close()
        return jsonify({'ok': True, 'importadas': importadas})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/compras', methods=['GET'])
@app.route('/compras', methods=['GET'])
def get_compras():
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM compras_mercaderia ORDER BY fecha DESC, id DESC;")
            filas = cur.fetchall()
        conn.close()
        
        compras = []
        for r in filas:
            fila_serial = serializar_fila(r)
            if 'fecha' in fila_serial and fila_serial['fecha']:
                if 'T' in str(fila_serial['fecha']):
                    fila_serial['fecha'] = str(fila_serial['fecha']).split('T')[0]
            compras.append(fila_serial)
            
        return jsonify({'ok': True, 'compras': compras})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/compras', methods=['POST'])
@app.route('/compras', methods=['POST'])
def add_compra():
    try:
        data = request.get_json(silent=True) or request.get_json(force=True, silent=True) or {}
        if not data:
            return jsonify({'ok': False, 'error': 'No se enviaron datos'}), 400

        fecha_str = data.get('fecha') or datetime.now().strftime('%Y-%m-%d')
        proveedor = (data.get('proveedor') or 'Proveedor General').strip()
        tipo_producto = data.get('tipo_producto') or data.get('tipo') or 'perfume'
        descripcion = (data.get('descripcion') or 'Compra de Mercadería').strip()
        cantidad = int(data.get('cantidad', 1))
        costo_unitario = float(data.get('costo_unitario', 0))
        costo_total = float(data.get('costo_total') or (costo_unitario * cantidad))
        metodo_pago = data.get('metodo_pago') or 'Efectivo'
        notas = data.get('notas', '')

        conn = get_db_connection()
        with conn.cursor() as cur:
            sql = """
                INSERT INTO compras_mercaderia (
                    fecha, proveedor, tipo_producto, descripcion,
                    cantidad, costo_unitario, costo_total, metodo_pago, notas
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cur.execute(sql, (
                fecha_str, proveedor, tipo_producto, descripcion,
                cantidad, costo_unitario, costo_total, metodo_pago, notas
            ))
            nuevo_id = cur.lastrowid
        conn.close()

        nueva_compra = {
            'id': nuevo_id,
            'fecha': fecha_str,
            'proveedor': proveedor,
            'tipo_producto': tipo_producto,
            'descripcion': descripcion,
            'cantidad': cantidad,
            'costo_unitario': costo_unitario,
            'costo_total': costo_total,
            'metodo_pago': metodo_pago,
            'notas': notas
        }
        return jsonify({'ok': True, 'compra': nueva_compra}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/compras/<int:compra_id>', methods=['DELETE'])
@app.route('/compras/<int:compra_id>', methods=['DELETE'])
def delete_compra(compra_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM compras_mercaderia WHERE id = %s;", (compra_id,))
            afectadas = cur.rowcount
        conn.close()
        return jsonify({'ok': True, 'eliminadas': afectadas})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/resumen-mes', methods=['GET'])
@app.route('/resumen-mes', methods=['GET'])
def get_resumen_mes():
    mes = request.args.get('mes') # ej: "2026-09"
    if not mes:
        mes = datetime.now().strftime('%Y-%m')
    try:
        conn = get_db_connection()
        patron_mes = f"{mes}%"
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    COUNT(*) as total_ventas_count,
                    COALESCE(SUM(total_venta), 0) as facturacion_total,
                    COALESCE(SUM(costo_unitario * cantidad), 0) as costo_mercaderia_vendida,
                    COALESCE(SUM(ganancia_neta), 0) as ganancia_neta,
                    COALESCE(SUM(cantidad), 0) as total_unidades_vendidas,
                    COALESCE(SUM(CASE WHEN tipo_producto = 'combo' THEN cantidad ELSE 0 END), 0) as unidades_combos,
                    COALESCE(SUM(CASE WHEN tipo_producto != 'combo' THEN cantidad ELSE 0 END), 0) as unidades_perfumes,
                    COALESCE(SUM(CASE WHEN metodo_pago = 'Efectivo' THEN total_venta ELSE 0 END), 0) as total_efectivo,
                    COALESCE(SUM(CASE WHEN metodo_pago != 'Efectivo' THEN total_venta ELSE 0 END), 0) as total_transferencia
                FROM ventas 
                WHERE fecha LIKE %s;
            """, (patron_mes,))
            kpi_ventas = cur.fetchone()

            cur.execute("""
                SELECT 
                    COUNT(*) as total_compras_count,
                    COALESCE(SUM(costo_total), 0) as total_invertido_compras,
                    COALESCE(SUM(cantidad), 0) as total_unidades_compradas
                FROM compras_mercaderia 
                WHERE fecha LIKE %s;
            """, (patron_mes,))
            kpi_compras = cur.fetchone()

            cur.execute("""
                SELECT nombre_fragancia, SUM(cantidad) as cant, SUM(total_venta) as total
                FROM ventas
                WHERE fecha LIKE %s
                GROUP BY nombre_fragancia
                ORDER BY cant DESC, total DESC
                LIMIT 5;
            """, (patron_mes,))
            top_fragancias = cur.fetchall()

        conn.close()

        res = {
            'mes': mes,
            'ventas': serializar_fila(kpi_ventas),
            'compras': serializar_fila(kpi_compras),
            'top_fragancias': [serializar_fila(f) for f in top_fragancias]
        }
        return jsonify({'ok': True, 'resumen': res})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

# ==================== CATÁLOGO & STOCK ====================
@app.route('/api/catalogo', methods=['GET'])
@app.route('/catalogo', methods=['GET'])
def get_catalogo():
    """Devuelve todo el catálogo de fragancias para búsqueda y autocompletado"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, tipo_producto, categoria, nombre_fragancia, marca,
                       cantidad as stock, costo_unitario, precio_venta
                FROM stock
                ORDER BY categoria ASC, nombre_fragancia ASC;
            """)
            filas = cur.fetchall()
        conn.close()
        items = [serializar_fila(r) for r in filas]
        for it in items:
            it['display'] = f"{it['nombre_fragancia']} ({it['marca']}) - {it['categoria']}"
        return jsonify({'ok': True, 'catalogo': items, 'total': len(items)})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/stock', methods=['GET'])
@app.route('/stock', methods=['GET'])
def get_stock():
    """Buscador y visor de stock"""
    q = (request.args.get('q') or '').strip().lower()
    cat = (request.args.get('categoria') or '').strip()
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            sql = "SELECT * FROM stock WHERE 1=1"
            params = []
            if q:
                sql += " AND (LOWER(nombre_fragancia) LIKE %s OR LOWER(marca) LIKE %s OR LOWER(categoria) LIKE %s)"
                term = f"%{q}%"
                params.extend([term, term, term])
            if cat and cat != 'todas':
                sql += " AND (categoria LIKE %s OR tipo_producto LIKE %s)"
                params.extend([f"%{cat}%", f"%{cat}%"])
            sql += " ORDER BY cantidad DESC, nombre_fragancia ASC;"
            cur.execute(sql, params)
            filas = cur.fetchall()
        conn.close()
        return jsonify({'ok': True, 'stock': [serializar_fila(r) for r in filas]})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/stock/ajustar', methods=['POST'])
@app.route('/stock/ajustar', methods=['POST'])
def ajustar_stock():
    """Ajustar cantidad de stock (+1, -1 o fijar valor)"""
    try:
        data = request.get_json(force=True)
        prod_id = int(data.get('id'))
        delta = data.get('delta')
        nueva_cant = data.get('cantidad')

        conn = get_db_connection()
        with conn.cursor() as cur:
            if delta is not None:
                cur.execute("UPDATE stock SET cantidad = GREATEST(0, cantidad + %s) WHERE id = %s;", (int(delta), prod_id))
            elif nueva_cant is not None:
                cur.execute("UPDATE stock SET cantidad = GREATEST(0, %s) WHERE id = %s;", (int(nueva_cant), prod_id))
            cur.execute("SELECT * FROM stock WHERE id = %s;", (prod_id,))
            prod = cur.fetchone()
        conn.close()
        return jsonify({'ok': True, 'producto': serializar_fila(prod)})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

# ==================== RESERVAS & ENCARGOS ====================
@app.route('/api/reservas', methods=['GET'])
@app.route('/reservas', methods=['GET'])
def get_reservas():
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM reservas_pedidos ORDER BY id DESC;")
            filas = cur.fetchall()
        conn.close()
        reservas = []
        for r in filas:
            fila_serial = serializar_fila(r)
            if 'fecha' in fila_serial and fila_serial['fecha']:
                if 'T' in str(fila_serial['fecha']):
                    fila_serial['fecha'] = str(fila_serial['fecha']).split('T')[0]
            reservas.append(fila_serial)
        return jsonify({'ok': True, 'reservas': reservas})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/reservas', methods=['POST'])
@app.route('/reservas', methods=['POST'])
def add_reserva():
    try:
        data = request.get_json(force=True)
        cliente = (data.get('cliente') or 'Cliente').strip()
        telefono = (data.get('telefono') or '').strip()
        tipo = data.get('tipo_producto') or data.get('tipo') or 'perfume'
        fragancia = (data.get('nombre_fragancia') or data.get('fragancia') or 'Fragancia').strip()
        cantidad = int(data.get('cantidad', 1))
        precio_estimado = float(data.get('precio_estimado') or data.get('precioVenta') or 0.0)
        tipo_op = data.get('tipo_operacion') or 'Reserva Cliente'
        estado = data.get('estado') or 'Pendiente'
        notas = (data.get('notas') or '').strip()

        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO reservas_pedidos (
                    cliente, telefono, tipo_producto, nombre_fragancia,
                    cantidad, precio_estimado, tipo_operacion, estado, notas
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (cliente, telefono, tipo, fragancia, cantidad, precio_estimado, tipo_op, estado, notas))
            nuevo_id = cur.lastrowid
        conn.close()

        nueva_res = {
            'id': nuevo_id,
            'cliente': cliente,
            'telefono': telefono,
            'tipo_producto': tipo,
            'nombre_fragancia': fragancia,
            'cantidad': cantidad,
            'precio_estimado': precio_estimado,
            'tipo_operacion': tipo_op,
            'estado': estado,
            'notas': notas
        }
        return jsonify({'ok': True, 'reserva': nueva_res}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/reservas/<int:reserva_id>', methods=['PUT'])
@app.route('/reservas/<int:reserva_id>', methods=['PUT'])
def update_reserva(reserva_id):
    try:
        data = request.get_json(force=True)
        conn = get_db_connection()
        campos = []
        valores = []
        for k in ['estado', 'notas', 'precio_estimado', 'cantidad', 'tipo_operacion']:
            if k in data:
                campos.append(f"{k} = %s")
                valores.append(data[k])
        if not campos:
            conn.close()
            return jsonify({'ok': False, 'error': 'Sin campos para actualizar'}), 400
        valores.append(reserva_id)
        with conn.cursor() as cur:
            cur.execute(f"UPDATE reservas_pedidos SET {', '.join(campos)} WHERE id = %s;", valores)
            cur.execute("SELECT * FROM reservas_pedidos WHERE id = %s;", (reserva_id,))
            reserva = cur.fetchone()
        conn.close()
        return jsonify({'ok': True, 'reserva': serializar_fila(reserva)})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/reservas/<int:reserva_id>', methods=['DELETE'])
@app.route('/reservas/<int:reserva_id>', methods=['DELETE'])
def delete_reserva(reserva_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM reservas_pedidos WHERE id = %s;", (reserva_id,))
            afectadas = cur.rowcount
        conn.close()
        return jsonify({'ok': True, 'eliminadas': afectadas})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/reservas/<int:reserva_id>/convertir', methods=['POST'])
@app.route('/reservas/<int:reserva_id>/convertir', methods=['POST'])
def convertir_reserva_a_venta(reserva_id):
    """Convierte una reserva directamente en venta registrada"""
    try:
        data = request.get_json(silent=True) or {}
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM reservas_pedidos WHERE id = %s;", (reserva_id,))
            r = cur.fetchone()
            if not r:
                conn.close()
                return jsonify({'ok': False, 'error': 'Reserva no encontrada'}), 404

            tipo = r['tipo_producto']
            costo = 6000.0 if tipo == 'combo' else 12000.0
            precio = float(data.get('precio_unitario') or r['precio_estimado'] or (11000.0 if tipo == 'combo' else 22000.0))
            cantidad = int(data.get('cantidad') or r['cantidad'] or 1)
            medio_pago = data.get('medioPago') or 'Efectivo'
            total_venta = precio * cantidad
            ganancia = (precio - costo) * cantidad
            fecha_hoy = datetime.now().strftime('%Y-%m-%d')

            cur.execute("""
                INSERT INTO ventas (
                    fecha, cliente, telefono, tipo_producto, nombre_fragancia,
                    cantidad, precio_unitario, costo_unitario, total_venta,
                    ganancia_neta, metodo_pago, estado_entrega, notas
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                fecha_hoy, r['cliente'], r['telefono'], tipo, r['nombre_fragancia'],
                cantidad, precio, costo, total_venta, ganancia, medio_pago, 'Cobrado',
                f"Convertido desde Reserva #{reserva_id}. {r['notas'] or ''}".strip()
            ))
            venta_id = cur.lastrowid

            # Actualizar estado de la reserva a Entregado
            cur.execute("UPDATE reservas_pedidos SET estado = 'Entregado' WHERE id = %s;", (reserva_id,))
        conn.close()
        return jsonify({'ok': True, 'venta_id': venta_id, 'reserva_id': reserva_id})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("==========================================================")
    print("  SERVIDOR BJ BEAUTY - BASE DE DATOS MYSQL")
    print("==========================================================")
    print(" Base de datos: MySQL localhost:3306 -> bj_beauty_db")
    print(" Panel web:     http://localhost:5000")
    print(" API Ventas:    http://localhost:5000/api/ventas")
    print(" Estado DB:     http://localhost:5000/api/estado")
    print("==========================================================")
    app.run(host='0.0.0.0', port=5000, debug=False)
