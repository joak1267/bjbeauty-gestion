# -*- coding: utf-8 -*-
"""
Inyecta la lógica JavaScript completa para el catálogo, autocompletado y reservas en sistema_ventas_y_ganancias.html.
"""

import os

FILE_PATH = r"C:\Users\soyto.JOAQUIN2206\OneDrive\Desktop\Proyectos\perfumes-gestion\sistema_ventas_y_ganancias.html"
SCRATCH_PATH = r"C:\Users\soyto.JOAQUIN2206\.gemini\antigravity\scratch\perfumes-gestion\sistema_ventas_y_ganancias.html"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Variables de estado al inicio de <script>
old_vars = "        let modoMySQL = false;"
new_vars = """        let modoMySQL = false;
        let catalogo = [];
        let reservas = [];
        let categoriaCatalogoActiva = 'todas';"""

content = content.replace(old_vars, new_vars)

# 2. Reemplazar cambiarPestana
old_pestana = """        function cambiarPestana(pestana) {
            const btnVentas = document.getElementById('tab-btn-ventas');
            const btnCompras = document.getElementById('tab-btn-compras');
            const secVentas = document.getElementById('seccion-ventas');
            const secCompras = document.getElementById('seccion-compras');

            if (pestana === 'ventas') {
                btnVentas.classList.add('active');
                btnCompras.classList.remove('active');
                secVentas.style.display = 'block';
                secCompras.style.display = 'none';
            } else {
                btnCompras.classList.add('active');
                btnVentas.classList.remove('active');
                secVentas.style.display = 'none';
                secCompras.style.display = 'block';
            }
        }"""

new_pestana = """        function cambiarPestana(pestana) {
            const tabs = ['ventas', 'compras', 'reservas', 'catalogo'];
            tabs.forEach(t => {
                const btn = document.getElementById(`tab-btn-${t}`);
                const sec = document.getElementById(`seccion-${t}`);
                if (btn) {
                    if (t === pestana) btn.classList.add('active');
                    else btn.classList.remove('active');
                }
                if (sec) {
                    sec.style.display = (t === pestana) ? 'block' : 'none';
                }
            });
            if (pestana === 'catalogo') renderizarTablaCatalogo();
            if (pestana === 'reservas') renderizarTablaReservas();
        }"""

content = content.replace(old_pestana, new_pestana)

# 3. Actualizar verificarConexionMySQL para llamar a cargarCatalogo y cargarReservas
old_verif = """                    await cargarVentasDesdeMySQL();
                    await cargarComprasDesdeMySQL();"""

new_verif = """                    await cargarVentasDesdeMySQL();
                    await cargarComprasDesdeMySQL();
                    await cargarCatalogo();
                    await cargarStock();
                    await cargarReservas();"""

content = content.replace(old_verif, new_verif)

# 4. Actualizar guardado de ventas para tomar venta-notas
old_notas_venta = "notas: ''"
new_notas_venta = "notas: (document.getElementById('venta-notas') ? document.getElementById('venta-notas').value : '').trim()"
content = content.replace(old_notas_venta, new_notas_venta)

# 5. Inyectar todas las funciones de autocompletado, reservas y catálogo antes de '// Init'
js_funcs = """
        // ==========================================
        // PROMOS RÁPIDAS EN VENTAS
        // ==========================================
        function aplicarPromoVenta(tipo) {
            if (tipo === '2x40') {
                document.getElementById('tipo-producto').value = 'perfume';
                document.getElementById('cantidad').value = 2;
                document.getElementById('precio-venta').value = 20000;
                document.getElementById('costo-unitario').value = 12000;
                calcularEnVivo();
            } else if (tipo === '2x20auto') {
                document.getElementById('tipo-producto').value = 'combo';
                document.getElementById('cantidad').value = 2;
                document.getElementById('precio-venta').value = 10000;
                document.getElementById('costo-unitario').value = 6000;
                calcularEnVivo();
            }
        }

        // ==========================================
        // AUTOCOMPLETADO Y SELECCIÓN DEL CATÁLOGO
        // ==========================================
        function buscarEnCatalogo(query, contexto = 'venta') {
            const container = document.getElementById(`autocomplete-catalogo-${contexto}`);
            if (!container) return;
            const q = (query || '').trim().toLowerCase();
            if (!q) {
                container.style.display = 'none';
                return;
            }
            const filtrados = catalogo.filter(p => 
                (p.nombre_fragancia && p.nombre_fragancia.toLowerCase().includes(q)) ||
                (p.marca && p.marca.toLowerCase().includes(q)) ||
                (p.categoria && p.categoria.toLowerCase().includes(q))
            ).slice(0, 15);

            if (filtrados.length === 0) {
                container.innerHTML = `<div style="padding: 10px; color: var(--text-muted); font-size: 0.8rem; text-align: center;">No se encontraron perfumes con "${query}"</div>`;
                container.style.display = 'block';
                return;
            }

            container.innerHTML = filtrados.map(p => {
                let tagClass = 'tag-fem';
                if (p.categoria && p.categoria.includes('Masc')) tagClass = 'tag-masc';
                else if (p.categoria && p.categoria.includes('Árabe')) tagClass = 'tag-arabe';
                else if (p.categoria && p.categoria.includes('Auto')) tagClass = 'tag-auto';
                else if (p.categoria && (p.categoria.includes('Unisex') || p.categoria.includes('Cápsula'))) tagClass = 'tag-unisex';

                return `
                    <div class="autocomplete-item" onclick="seleccionarDelCatalogo(${p.id}, '${contexto}')">
                        <div>
                            <div class="auto-name">${p.nombre_fragancia}</div>
                            <div class="auto-meta">${p.marca || ''} • <span class="auto-tag ${tagClass}">${p.categoria || ''}</span></div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-weight: 700; color: var(--primary); font-size: 0.85rem;">$${p.precio_venta.toLocaleString('es-AR')}</div>
                            <div style="font-size: 0.72rem; color: var(--text-muted);">Stock: ${p.stock || 0}</div>
                        </div>
                    </div>
                `;
            }).join('');
            container.style.display = 'block';
        }

        function seleccionarDelCatalogo(id, contexto = 'venta') {
            const p = catalogo.find(item => item.id === id);
            if (!p) return;

            if (contexto === 'venta') {
                document.getElementById('fragancia').value = `${p.nombre_fragancia} (${p.marca})`;
                const tipoSelect = document.getElementById('tipo-producto');
                if (tipoSelect) {
                    if (p.categoria && (p.categoria.includes('Árabe') || p.categoria.includes('Cápsula'))) {
                        tipoSelect.value = 'fusion';
                    } else if (p.categoria && p.categoria.includes('Auto')) {
                        tipoSelect.value = 'combo';
                    } else {
                        tipoSelect.value = 'perfume';
                    }
                }
                document.getElementById('precio-venta').value = p.precio_venta;
                document.getElementById('costo-unitario').value = p.costo_unitario;
                calcularEnVivo();
                const drop = document.getElementById('autocomplete-catalogo-venta');
                if (drop) drop.style.display = 'none';
            } else if (contexto === 'reserva') {
                document.getElementById('reserva-fragancia').value = `${p.nombre_fragancia} (${p.marca})`;
                document.getElementById('reserva-precio').value = p.precio_venta;
                document.getElementById('reserva-tipo-prod').value = p.tipo_producto;
                const drop = document.getElementById('autocomplete-catalogo-reserva');
                if (drop) drop.style.display = 'none';
            }
        }

        document.addEventListener('click', function(e) {
            if (!e.target.closest('#fragancia') && !e.target.closest('#autocomplete-catalogo-venta')) {
                const d = document.getElementById('autocomplete-catalogo-venta');
                if (d) d.style.display = 'none';
            }
            if (!e.target.closest('#reserva-fragancia') && !e.target.closest('#autocomplete-catalogo-reserva')) {
                const d = document.getElementById('autocomplete-catalogo-reserva');
                if (d) d.style.display = 'none';
            }
        });

        // ==========================================
        // RESERVAS, ENCARGOS & PENDIENTES
        // ==========================================
        async function cargarReservas() {
            if (modoMySQL) {
                try {
                    const resp = await fetch(`${API_BASE}/reservas`, { cache: 'no-cache' });
                    if (resp.ok) {
                        const data = await resp.json();
                        reservas = data.reservas || [];
                        localStorage.setItem('perfumes_reservas_db', JSON.stringify(reservas));
                    }
                } catch (e) {
                    reservas = JSON.parse(localStorage.getItem('perfumes_reservas_db')) || [];
                }
            } else {
                reservas = JSON.parse(localStorage.getItem('perfumes_reservas_db')) || [];
            }
            actualizarBadgeReservas();
            renderizarTablaReservas();
        }

        function actualizarBadgeReservas() {
            const activas = reservas.filter(r => r.estado !== 'Entregado' && r.estado !== 'Cancelado').length;
            const badge = document.getElementById('badge-count-reservas');
            if (badge) {
                badge.innerText = activas;
                badge.style.display = activas > 0 ? 'inline-block' : 'none';
            }
        }

        function autoAjustarTipoOperacion() {
            const op = document.getElementById('reserva-tipo-op').value;
            const estadoSelect = document.getElementById('reserva-estado');
            if (op === 'A Confirmar') {
                estadoSelect.value = 'Pendiente de Confirmación';
            } else if (op === 'Encargo Proveedor') {
                estadoSelect.value = 'Por Encargar';
                document.getElementById('reserva-cliente').value = 'Distribuidor / Fábrica';
            } else {
                estadoSelect.value = 'Reservado';
            }
        }

        function renderizarTablaReservas(filtradas = null) {
            const lista = filtradas || reservas;
            const tbody = document.getElementById('tabla-reservas-cuerpo');
            if (!tbody) return;
            tbody.innerHTML = '';

            const sinDatos = document.getElementById('sin-reservas');
            if (lista.length === 0) {
                if (sinDatos) sinDatos.style.display = 'block';
                return;
            } else {
                if (sinDatos) sinDatos.style.display = 'none';
            }

            lista.forEach(r => {
                const tr = document.createElement('tr');
                let badgeOpClass = 'badge-op-reserva';
                if (r.tipo_operacion === 'A Confirmar') badgeOpClass = 'badge-op-confirmar';
                else if (r.tipo_operacion === 'Encargo Proveedor') badgeOpClass = 'badge-op-encargo';

                let badgeEstadoColor = '#facc15';
                let badgeEstadoBg = 'rgba(234, 179, 8, 0.2)';
                if (r.estado === 'Entregado') {
                    badgeEstadoColor = '#34d399';
                    badgeEstadoBg = 'rgba(16, 185, 129, 0.2)';
                } else if (r.estado === 'Por Encargar') {
                    badgeEstadoColor = '#c084fc';
                    badgeEstadoBg = 'rgba(168, 85, 247, 0.2)';
                }

                tr.innerHTML = `
                    <td>${r.fecha ? r.fecha.split('T')[0] : '-'}</td>
                    <td><strong>${r.cliente}</strong></td>
                    <td><span class="badge-op ${badgeOpClass}">${r.tipo_operacion}</span></td>
                    <td>${r.nombre_fragancia}</td>
                    <td>${r.cantidad}</td>
                    <td>$${(r.precio_estimado ? Number(r.precio_estimado) : 0).toLocaleString('es-AR')}</td>
                    <td><span style="display:inline-block; padding: 2px 8px; border-radius: 10px; font-size: 0.72rem; font-weight: 700; background: ${badgeEstadoBg}; color: ${badgeEstadoColor};">${r.estado}</span></td>
                    <td><small style="color: #cbd5e1;">${r.notas || '-'}</small></td>
                    <td style="text-align: right; white-space: nowrap;">
                        ${r.estado !== 'Entregado' ? `
                            <button class="btn-sm-action btn-sm-success" title="Pasar a Venta Directa" onclick="convertirReservaAVenta(${r.id})">🛒 Vender</button>
                            <button class="btn-sm-action" title="Marcar como Entregado" onclick="marcarReservaEntregada(${r.id})">✅</button>
                        ` : '<span style="color:var(--success);font-size:0.75rem;font-weight:700;">Entregado</span>'}
                        <button class="action-icon" title="Eliminar" onclick="eliminarReserva(${r.id})">🗑️</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        async function guardarReservaForm(e) {
            e.preventDefault();
            const nuevaRes = {
                cliente: document.getElementById('reserva-cliente').value,
                telefono: '',
                tipo_producto: document.getElementById('reserva-tipo-prod').value || 'perfume',
                nombre_fragancia: document.getElementById('reserva-fragancia').value,
                cantidad: Number(document.getElementById('reserva-cantidad').value) || 1,
                precio_estimado: Number(document.getElementById('reserva-precio').value) || 0,
                tipo_operacion: document.getElementById('reserva-tipo-op').value,
                estado: document.getElementById('reserva-estado').value,
                notas: document.getElementById('reserva-notas').value
            };

            if (modoMySQL) {
                try {
                    const resp = await fetch(`${API_BASE}/reservas`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(nuevaRes)
                    });
                    const res = await resp.json();
                    if (res.ok && res.reserva) {
                        reservas.unshift(res.reserva);
                    }
                } catch (err) {
                    nuevaRes.id = Date.now();
                    nuevaRes.fecha = new Date().toISOString().split('T')[0];
                    reservas.unshift(nuevaRes);
                }
            } else {
                nuevaRes.id = Date.now();
                nuevaRes.fecha = new Date().toISOString().split('T')[0];
                reservas.unshift(nuevaRes);
            }

            localStorage.setItem('perfumes_reservas_db', JSON.stringify(reservas));
            actualizarBadgeReservas();
            renderizarTablaReservas();
            alert('✅ ¡Reserva registrada con éxito!');
            document.getElementById('reserva-form').reset();
        }

        async function convertirReservaAVenta(id) {
            if (!confirm('¿Deseas pasar esta reserva directamente a las Ventas Registradas?')) return;
            if (modoMySQL) {
                try {
                    const resp = await fetch(`${API_BASE}/reservas/${id}/convertir`, { method: 'POST' });
                    const res = await resp.json();
                    if (res.ok) {
                        alert('🎉 ¡Venta registrada y reserva completada!');
                        await cargarVentasDesdeMySQL();
                        await cargarReservas();
                        cambiarPestana('ventas');
                        return;
                    }
                } catch (err) {
                    console.error(err);
                }
            }
            const r = reservas.find(item => item.id === id);
            if (r) {
                r.estado = 'Entregado';
                const tipo = r.tipo_producto || 'perfume';
                const nuevaV = {
                    id: Date.now(),
                    fecha: new Date().toISOString().split('T')[0],
                    cliente: r.cliente,
                    tipo: tipo,
                    fragancia: r.nombre_fragancia,
                    cantidad: r.cantidad || 1,
                    precioVenta: r.precio_estimado || (tipo === 'combo' ? 11000 : 22000),
                    costoUnitario: (tipo === 'combo' ? 6000 : 12000),
                    medioPago: 'Efectivo',
                    estadoPago: 'Cobrado',
                    notas: `Convertido de Reserva #${id}. ${r.notas || ''}`
                };
                ventas.unshift(nuevaV);
                localStorage.setItem('perfumes_ventas_db', JSON.stringify(ventas));
                localStorage.setItem('perfumes_reservas_db', JSON.stringify(reservas));
                actualizarDashboardGeneral();
                actualizarBadgeReservas();
                renderizarTablaReservas();
                alert('🎉 ¡Venta registrada!');
                cambiarPestana('ventas');
            }
        }

        async function marcarReservaEntregada(id) {
            if (modoMySQL) {
                try {
                    await fetch(`${API_BASE}/reservas/${id}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ estado: 'Entregado' })
                    });
                } catch (e) { console.warn(e); }
            }
            const r = reservas.find(item => item.id === id);
            if (r) r.estado = 'Entregado';
            localStorage.setItem('perfumes_reservas_db', JSON.stringify(reservas));
            actualizarBadgeReservas();
            renderizarTablaReservas();
        }

        async function eliminarReserva(id) {
            if (!confirm('¿Eliminar esta reserva o encargo?')) return;
            if (modoMySQL) {
                try {
                    await fetch(`${API_BASE}/reservas/${id}`, { method: 'DELETE' });
                } catch (e) { console.warn(e); }
            }
            reservas = reservas.filter(r => r.id !== id);
            localStorage.setItem('perfumes_reservas_db', JSON.stringify(reservas));
            actualizarBadgeReservas();
            renderizarTablaReservas();
        }

        function filtrarReservas() {
            const q = (document.getElementById('filtro-reservas').value || '').toLowerCase();
            const filtradas = reservas.filter(r => 
                (r.cliente && r.cliente.toLowerCase().includes(q)) ||
                (r.nombre_fragancia && r.nombre_fragancia.toLowerCase().includes(q)) ||
                (r.notas && r.notas.toLowerCase().includes(q)) ||
                (r.tipo_operacion && r.tipo_operacion.toLowerCase().includes(q)) ||
                (r.estado && r.estado.toLowerCase().includes(q))
            );
            renderizarTablaReservas(filtradas);
        }

        // ==========================================
        // CATÁLOGO OFICIAL & CONTROL DE STOCK
        // ==========================================
        async function cargarCatalogo() {
            if (modoMySQL) {
                try {
                    const resp = await fetch(`${API_BASE}/catalogo`, { cache: 'no-cache' });
                    if (resp.ok) {
                        const data = await resp.json();
                        catalogo = data.catalogo || [];
                        localStorage.setItem('perfumes_catalogo_cache', JSON.stringify(catalogo));
                        return;
                    }
                } catch (e) { console.warn(e); }
            }
            catalogo = JSON.parse(localStorage.getItem('perfumes_catalogo_cache')) || [];
        }

        async function cargarStock() {
            if (modoMySQL) {
                try {
                    const resp = await fetch(`${API_BASE}/stock`, { cache: 'no-cache' });
                    if (resp.ok) {
                        const data = await resp.json();
                        const stockItems = data.stock || [];
                        stockItems.forEach(s => {
                            const found = catalogo.find(c => c.id === s.id);
                            if (found) found.stock = s.cantidad;
                        });
                    }
                } catch (e) { console.warn(e); }
            }
        }

        function renderizarTablaCatalogo(filtradas = null) {
            const lista = filtradas || catalogo;
            const tbody = document.getElementById('tabla-catalogo-cuerpo');
            if (!tbody) return;
            tbody.innerHTML = '';

            lista.forEach(p => {
                const tr = document.createElement('tr');
                let tagClass = 'tag-fem';
                if (p.categoria && p.categoria.includes('Masc')) tagClass = 'tag-masc';
                else if (p.categoria && p.categoria.includes('Árabe')) tagClass = 'tag-arabe';
                else if (p.categoria && p.categoria.includes('Auto')) tagClass = 'tag-auto';
                else if (p.categoria && (p.categoria.includes('Unisex') || p.categoria.includes('Cápsula'))) tagClass = 'tag-unisex';

                tr.innerHTML = `
                    <td><strong>${p.nombre_fragancia}</strong></td>
                    <td><span style="color:#cbd5e1;">${p.marca || '-'}</span></td>
                    <td><span class="auto-tag ${tagClass}">${p.categoria || 'Perfume'}</span></td>
                    <td style="font-weight:700;color:var(--primary);">$${p.precio_venta.toLocaleString('es-AR')}</td>
                    <td>$${p.costo_unitario.toLocaleString('es-AR')}</td>
                    <td style="text-align:center;">
                        <div class="stock-control">
                            <button class="btn-stock" onclick="ajustarStock(${p.id}, -1)">-</button>
                            <span style="font-weight:bold; min-width: 25px; display: inline-block;">${p.stock || 0}</span>
                            <button class="btn-stock" onclick="ajustarStock(${p.id}, 1)">+</button>
                        </div>
                    </td>
                    <td style="text-align: right; white-space: nowrap;">
                        <button class="btn-sm-action" title="Cargar venta de este producto" onclick="prepararVentaDesdeCatalogo(${p.id})">🛒 Vender</button>
                        <button class="btn-sm-action" title="Reservar para cliente" onclick="prepararReservaDesdeCatalogo(${p.id})">🔖 Reservar</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        function filtrarCatalogo() {
            const q = (document.getElementById('filtro-catalogo-input').value || '').toLowerCase();
            let lista = catalogo;
            if (categoriaCatalogoActiva !== 'todas') {
                lista = lista.filter(p => p.categoria && p.categoria.includes(categoriaCatalogoActiva));
            }
            if (q) {
                lista = lista.filter(p => 
                    (p.nombre_fragancia && p.nombre_fragancia.toLowerCase().includes(q)) || 
                    (p.marca && p.marca.toLowerCase().includes(q)) || 
                    (p.categoria && p.categoria.toLowerCase().includes(q))
                );
            }
            renderizarTablaCatalogo(lista);
        }

        function filtrarCatalogoCat(cat, btn) {
            categoriaCatalogoActiva = cat;
            const chips = document.querySelectorAll('#chips-catalogo .filter-chip');
            chips.forEach(c => c.classList.remove('active'));
            if (btn) btn.classList.add('active');
            filtrarCatalogo();
        }

        async function ajustarStock(id, delta) {
            const p = catalogo.find(item => item.id === id);
            if (!p) return;
            p.stock = Math.max(0, (p.stock || 0) + delta);
            renderizarTablaCatalogo();

            if (modoMySQL) {
                try {
                    await fetch(`${API_BASE}/stock/ajustar`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ id: id, delta: delta })
                    });
                } catch (e) { console.warn(e); }
            }
        }

        function prepararVentaDesdeCatalogo(id) {
            seleccionarDelCatalogo(id, 'venta');
            cambiarPestana('ventas');
            document.getElementById('cliente').focus();
        }

        function prepararReservaDesdeCatalogo(id) {
            seleccionarDelCatalogo(id, 'reserva');
            cambiarPestana('reservas');
            document.getElementById('reserva-cliente').focus();
        }
"""

content = content.replace("        // Inicialización\n        calcularEnVivo();", js_funcs + "\n        // Inicialización\n        calcularEnVivo();")

# 6. Guardar ambos archivos
with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(content)

with open(SCRATCH_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("JavaScript y lógica de catálogo/reservas inyectadas con éxito.")
