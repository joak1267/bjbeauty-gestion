# -*- coding: utf-8 -*-
import urllib.request
import json

def test_url(endpoint):
    url = f"http://127.0.0.1:5000{endpoint}"
    try:
        with urllib.request.urlopen(url, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"[OK] {endpoint} -> HTTP {resp.status}")
            return data
    except Exception as e:
        print(f"[ERROR] {endpoint} -> {e}")
        return None

print("=== PROBANDO ENDPOINTS BJ BEAUTY ===")
estado = test_url("/api/estado")
print("Estado DB:", estado)

ventas = test_url("/api/ventas")
print("Total Ventas:", len(ventas.get('ventas', [])) if ventas else 0)
if ventas and ventas.get('ventas'):
    for v in ventas['ventas'][:3]:
        print(f"  Venta #{v['id']}: {v['cliente']} - {v['fragancia']} (${v['precioVenta']} x {v['cantidad']}) | Notas: {v.get('notas')}")

reservas = test_url("/api/reservas")
print("Total Reservas & Encargos:", len(reservas.get('reservas', [])) if reservas else 0)
if reservas and reservas.get('reservas'):
    for r in reservas['reservas']:
        print(f"  Reserva #{r['id']}: {r['cliente']} -> {r['nombre_fragancia']} | Op: {r['tipo_operacion']} | Estado: {r['estado']}")

catalogo = test_url("/api/catalogo")
print("Total Perfumes en Catálogo:", catalogo.get('total') if catalogo else 0)
if catalogo and catalogo.get('catalogo'):
    print("  Muestra de perfumes cargados:", [c['nombre_fragancia'] + " (" + c['marca'] + ")" for c in catalogo['catalogo'][:4]])

stock = test_url("/api/stock?q=Scandal")
print("Búsqueda en Stock 'Scandal':", len(stock.get('stock', [])) if stock else 0)
if stock and stock.get('stock'):
    for s in stock['stock']:
        print(f"  Stock: {s['nombre_fragancia']} ({s['marca']}) - {s['categoria']} | Stock actual: {s['cantidad']}")
