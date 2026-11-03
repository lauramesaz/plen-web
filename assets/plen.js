/* ============ PLEN — carrito y detalles ============ */
const PLEN = {
  whatsapp: '573000000000',          // PENDIENTE: número real de Plen
  envioGratisDesde: 150000,
  costoEnvio: 12000,
  productos: {
    magnesio: {
      nombre: 'Magnesio + Zinc', sub: 'Bisglicinato · 100 unidades',
      precio: 89000, img: 'assets/img/frasco.jpg', url: 'magnesio.html'
    }
  }
};
const SUSCRIPCION_DESCUENTO = 0.15;

const pesos = n => '$' + Math.round(n).toLocaleString('es-CO');
const leer = () => { try { return JSON.parse(localStorage.getItem('plen-carrito')) || []; } catch (e) { return []; } };
const guardar = c => { try { localStorage.setItem('plen-carrito', JSON.stringify(c)); } catch (e) {} };
let carrito = leer();

function precioItem(it) {
  const p = PLEN.productos[it.id].precio;
  return it.plan === 'suscripcion' ? p * (1 - SUSCRIPCION_DESCUENTO) : p;
}
function subtotal() { return carrito.reduce((s, it) => s + precioItem(it) * it.cant, 0); }
function unidades() { return carrito.reduce((s, it) => s + it.cant, 0); }
function envio() { const s = subtotal(); return s === 0 || s >= PLEN.envioGratisDesde ? 0 : PLEN.costoEnvio; }

function agregar(id, cant = 1, plan = 'unica') {
  const ya = carrito.find(it => it.id === id && it.plan === plan);
  if (ya) ya.cant += cant; else carrito.push({ id, cant, plan });
  guardar(carrito); pintar(); abrirCarrito();
}
function cambiar(i, d) {
  carrito[i].cant += d;
  if (carrito[i].cant < 1) carrito.splice(i, 1);
  guardar(carrito); pintar();
}

/* ---------- panel del carrito ---------- */
function montarCarrito() {
  document.body.insertAdjacentHTML('beforeend', `
  <div class="velo" data-cerrar></div>
  <aside class="carrito" aria-label="Tu bolsa">
    <div class="carrito__cab"><h3>Tu bolsa</h3>
      <button class="icono-btn" data-cerrar aria-label="Cerrar"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>
    <div class="envio-barra"><span data-envio-txt></span><div class="riel"><i data-envio-riel></i></div></div>
    <div class="carrito__items" data-items></div>
    <div class="carrito__pie" data-pie></div>
  </aside>
  <div class="toast" data-toast></div>`);
  document.querySelectorAll('[data-cerrar]').forEach(b => b.addEventListener('click', cerrarCarrito));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') cerrarCarrito(); });
}
function abrirCarrito() { document.querySelector('.carrito').classList.add('si'); document.querySelector('.velo').classList.add('si'); }
function cerrarCarrito() { document.querySelector('.carrito')?.classList.remove('si'); document.querySelector('.velo')?.classList.remove('si'); }

function pintar() {
  const n = unidades();
  document.querySelectorAll('[data-contador]').forEach(b => { b.textContent = n; b.classList.toggle('si', n > 0); });
  const items = document.querySelector('[data-items]'); if (!items) return;
  const falta = PLEN.envioGratisDesde - subtotal();
  document.querySelector('[data-envio-txt]').innerHTML = falta > 0
    ? `Te faltan <b>${pesos(falta)}</b> para el envío gratis` : 'Tu envío es <b>gratis</b> ✦';
  document.querySelector('[data-envio-riel]').style.width = Math.min(100, subtotal() / PLEN.envioGratisDesde * 100) + '%';

  if (!carrito.length) {
    items.innerHTML = `<div class="carrito__vacio"><b>Tu bolsa está vacía</b>Empieza tu ritual con nuestro magnesio.<br><br><a class="btn" href="magnesio.html">Ver magnesio</a></div>`;
    document.querySelector('[data-pie]').innerHTML = '';
    return;
  }
  items.innerHTML = carrito.map((it, i) => {
    const p = PLEN.productos[it.id];
    return `<div class="item"><img src="${p.img}" alt="">
      <div><h4>${p.nombre}</h4><small>${it.plan === 'suscripcion' ? 'Suscripción · −15%' : 'Compra única'}</small>
        <div class="cant"><button data-menos="${i}" aria-label="Quitar uno">−</button><span>${it.cant}</span><button data-mas="${i}" aria-label="Agregar uno">+</button></div></div>
      <div class="item__der">${pesos(precioItem(it) * it.cant)}<button data-quitar="${i}">Quitar</button></div></div>`;
  }).join('');
  items.querySelectorAll('[data-menos]').forEach(b => b.onclick = () => cambiar(+b.dataset.menos, -1));
  items.querySelectorAll('[data-mas]').forEach(b => b.onclick = () => cambiar(+b.dataset.mas, 1));
  items.querySelectorAll('[data-quitar]').forEach(b => b.onclick = () => cambiar(+b.dataset.quitar, -999));
  document.querySelector('[data-pie]').innerHTML = `
    <div class="fila"><span>Subtotal</span><span>${pesos(subtotal())}</span></div>
    <div class="fila"><span>Envío</span><span>${envio() ? pesos(envio()) : 'Gratis'}</span></div>
    <div class="fila fila--total"><span>Total</span><span>${pesos(subtotal() + envio())}</span></div>
    <a class="btn btn--ancho" href="pedido.html">Finalizar compra <svg class="flecha" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M4 12h15M13 6l6 6-6 6"/></svg></a>
    <p class="seguro">Pago seguro · Tarjeta, PSE y Nequi</p>`;
}

function toast(t) {
  const el = document.querySelector('[data-toast]'); el.textContent = t; el.classList.add('si');
  clearTimeout(toast.t); toast.t = setTimeout(() => el.classList.remove('si'), 2200);
}

/* ---------- general ---------- */
document.addEventListener('DOMContentLoaded', () => {
  montarCarrito(); pintar();
  document.querySelectorAll('[data-abrir-carrito]').forEach(b => b.addEventListener('click', abrirCarrito));
  document.querySelectorAll('[data-agregar]').forEach(b => b.addEventListener('click', e => {
    e.preventDefault(); agregar(b.dataset.agregar);
  }));
  document.querySelectorAll('[data-pronto]').forEach(b => b.addEventListener('click', e => {
    e.preventDefault(); toast('Muy pronto ✦ Déjanos tu correo y te avisamos');
  }));

  // brillo del vidrio que sigue el cursor
  document.addEventListener('pointermove', e => {
    const g = e.target.closest && e.target.closest('.glass'); if (!g) return;
    const r = g.getBoundingClientRect();
    g.style.setProperty('--mx', (e.clientX - r.left) + 'px'); g.style.setProperty('--my', (e.clientY - r.top) + 'px');
  }, { passive: true });

  // lente de vidrio líquido que sigue el mouse
  lenteLiquida();

  // header con borde al bajar
  const h = document.querySelector('.header');
  const onScroll = () => h && h.classList.toggle('con-borde', scrollY > 10);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // menú móvil
  const mm = document.querySelector('.menu-movil');
  document.querySelectorAll('[data-menu]').forEach(b => b.addEventListener('click', () => mm.classList.toggle('si')));
  mm?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => mm.classList.remove('si')));

  // entradas al hacer scroll
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('si'); io.unobserve(e.target); } }), { threshold: .12 });
  document.querySelectorAll('.rev').forEach(el => io.observe(el));

  // parallax suave en la foto editorial
  const ed = document.querySelector('.editorial img');
  if (ed && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    addEventListener('scroll', () => {
      const r = ed.parentElement.getBoundingClientRect();
      ed.style.transform = `translateY(${(r.top / innerHeight) * -60}px)`;
    }, { passive: true });
  }

  // boletín
  document.querySelectorAll('[data-boletin]').forEach(f => f.addEventListener('submit', e => {
    e.preventDefault(); f.innerHTML = '<p style="font-family:var(--serif);font-size:24px">Gracias. Ya eres parte de Plen ✦</p>';
  }));

  if (document.body.dataset.pagina === 'producto') paginaProducto();
  if (document.body.dataset.pagina === 'pedido') paginaPedido();
});

/* ---------- página de producto ---------- */
function paginaProducto() {
  const grande = document.querySelector('.foto-grande img');
  document.querySelectorAll('.miniaturas button').forEach(b => b.addEventListener('click', () => {
    document.querySelectorAll('.miniaturas button').forEach(x => x.classList.remove('si'));
    b.classList.add('si'); grande.style.opacity = 0;
    setTimeout(() => { grande.src = b.dataset.src; grande.style.opacity = 1; }, 180);
  }));
  let cant = 1;
  const num = document.querySelector('[data-cant]');
  document.querySelector('[data-cmenos]').onclick = () => { cant = Math.max(1, cant - 1); num.textContent = cant; };
  document.querySelector('[data-cmas]').onclick = () => { cant++; num.textContent = cant; };
  const plan = () => document.querySelector('input[name=plan]:checked').value;
  const precioBtn = document.querySelectorAll('[data-precio-btn]');
  const actualizar = () => {
    const p = PLEN.productos.magnesio.precio * (plan() === 'suscripcion' ? 1 - SUSCRIPCION_DESCUENTO : 1);
    precioBtn.forEach(el => el.textContent = pesos(p));
  };
  document.querySelectorAll('input[name=plan]').forEach(r => r.addEventListener('change', actualizar)); actualizar();
  document.querySelectorAll('[data-comprar]').forEach(b => b.addEventListener('click', () => agregar('magnesio', cant, plan())));

  // barra fija en celular
  const bf = document.querySelector('.barra-fija'), ref = document.querySelector('.comprar');
  if (bf && ref) new IntersectionObserver(([e]) => bf.classList.toggle('si', !e.isIntersecting && e.boundingClientRect.top < 0)).observe(ref);
}

/* ---------- pedido ---------- */
function paginaPedido() {
  const box = document.querySelector('[data-resumen]');
  const pintarResumen = () => {
    if (!carrito.length) { box.innerHTML = '<p class="suave">Tu bolsa está vacía. <a href="magnesio.html" style="text-decoration:underline">Ver magnesio</a></p>'; return; }
    box.innerHTML = carrito.map(it => {
      const p = PLEN.productos[it.id];
      return `<div class="item" style="grid-template-columns:64px 1fr auto"><img src="${p.img}" alt="" style="width:64px;height:76px">
        <div><h4>${p.nombre} × ${it.cant}</h4><small>${it.plan === 'suscripcion' ? 'Suscripción −15%' : 'Compra única'}</small></div>
        <div class="item__der">${pesos(precioItem(it) * it.cant)}</div></div>`;
    }).join('') + `
      <div style="margin-top:18px"><div class="fila"><span>Subtotal</span><span>${pesos(subtotal())}</span></div>
      <div class="fila"><span>Envío</span><span>${envio() ? pesos(envio()) : 'Gratis'}</span></div>
      <div class="fila fila--total"><span>Total</span><span>${pesos(subtotal() + envio())}</span></div></div>`;
  };
  pintarResumen();
  document.querySelector('[data-form-pedido]').addEventListener('submit', e => {
    e.preventDefault();
    if (!carrito.length) return toast('Tu bolsa está vacía');
    const d = Object.fromEntries(new FormData(e.target));
    const lineas = carrito.map(it => `• ${PLEN.productos[it.id].nombre} x${it.cant} (${it.plan === 'suscripcion' ? 'suscripción' : 'compra única'}) — ${pesos(precioItem(it) * it.cant)}`).join('\n');
    const msg = `Hola Plen ✦ Quiero hacer este pedido:\n${lineas}\nTotal: ${pesos(subtotal() + envio())}\n\nNombre: ${d.nombre}\nCelular: ${d.celular}\nCiudad: ${d.ciudad}\nDirección: ${d.direccion}\nPago: ${d.pago}`;
    // DEMO: mientras se conecta la pasarela (Wompi / Shopify) el pedido se confirma por WhatsApp
    document.querySelector('.pedido').innerHTML = `<div class="gracias" style="grid-column:1/-1">
      <p class="eyebrow">Pedido recibido</p><h1 class="display">Gracias, <em>${(d.nombre || '').split(' ')[0]}</em></h1>
      <p class="suave" style="max-width:460px;margin:0 auto 30px">En la versión final aquí se abre la pasarela de pago. Por ahora te llevamos a WhatsApp para confirmar tu pedido.</p>
      <a class="btn" target="_blank" rel="noopener" href="https://wa.me/${PLEN.whatsapp}?text=${encodeURIComponent(msg)}">Confirmar por WhatsApp</a></div>`;
    carrito = []; guardar(carrito); pintar();
  });
}

/* ---------- lente de vidrio líquido ---------- */
function lenteLiquida() {
  if (!matchMedia('(hover:hover) and (pointer:fine)').matches || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const lente = document.querySelector('.lente'); if (!lente) return;
  const gotas = [...document.querySelectorAll('.estela i')];
  let mx = innerWidth / 2, my = innerHeight / 2, x = mx, y = my, vx = 0, vy = 0, esc = 1, escMeta = 1;
  const pos = gotas.map(() => ({ x: mx, y: my }));
  addEventListener('pointermove', e => {
    mx = e.clientX; my = e.clientY; document.body.classList.add('con-lente');
    escMeta = e.target.closest('a,button,label,summary,input') ? 1.45 : 1;
  }, { passive: true });
  document.addEventListener('pointerleave', () => document.body.classList.remove('con-lente'));
  addEventListener('blur', () => document.body.classList.remove('con-lente'));
  addEventListener('pointerdown', () => { esc = .78; });
  (function paso() {
    // resorte: sigue al cursor con un poco de inercia, como un líquido
    vx += (mx - x) * .16; vy += (my - y) * .16; vx *= .62; vy *= .62; x += vx; y += vy;
    esc += (escMeta - esc) * .14;
    const vel = Math.min(Math.hypot(vx, vy), 60), ang = Math.atan2(vy, vx) * 180 / Math.PI;
    const estira = 1 + vel / 110, aplana = 1 - vel / 260;
    lente.style.transform = `translate3d(${x}px,${y}px,0) rotate(${ang}deg) scale(${esc * estira},${esc * aplana})`;
    let px = x, py = y;
    pos.forEach((p, i) => {
      p.x += (px - p.x) * (.34 - i * .05); p.y += (py - p.y) * (.34 - i * .05);
      const s = (1 - i * .18) * Math.min(1, .35 + vel / 30);
      gotas[i].style.transform = `translate3d(${p.x}px,${p.y}px,0) scale(${s})`;
      px = p.x; py = p.y;
    });
    requestAnimationFrame(paso);
  })();
}
