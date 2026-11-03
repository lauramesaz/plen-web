#!/usr/bin/env python3
"""Arma las páginas de Plen (header y footer compartidos). Uso: python3 build.py"""
import hashlib, re
from pathlib import Path

RAIZ = Path(__file__).parent
FLECHA = '<svg class="flecha" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M4 12h15M13 6l6 6-6 6"/></svg>'
MAS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 5v14M5 12h14"/></svg>'
# Render del frasco real (vidrio ámbar + etiqueta de PLEN MAGNESIUM CURVAS 2.ai). PENDIENTE: foto real de estudio.
FRASCO = 'assets/img/frasco.jpg'
# Sello de la etiqueta: aro + WELLNESS / HEALTHY + destello de rayos finos con 4 puntos
SELLO = ('<svg class="sello" viewBox="0 0 200 200" aria-hidden="true"><defs><path id="sello-arriba" d="M 36,100 A 64,64 0 0 1 164,100"/><path id="sello-abajo" d="M 22,100 A 78,78 0 0 0 178,100"/></defs>'
         '<circle class="aro" cx="100" cy="100" r="96"/><text><textPath href="#sello-arriba" startOffset="50%" text-anchor="middle">WELLNESS</textPath></text>'
         '<text><textPath href="#sello-abajo" startOffset="50%" text-anchor="middle">HEALTHY</textPath></text><circle class="punto" cx="22" cy="100" r="2.2"/><circle class="punto" cx="178" cy="100" r="2.2"/>'
         '<g class="destello"><line class="rayo" x1="100.00" y1="92.52" x2="100.00" y2="56.00"/><line class="rayo" x1="102.86" y1="93.09" x2="105.05" y2="87.80"/><line class="rayo" x1="105.29" y1="94.71" x2="113.07" y2="86.93"/><line class="rayo" x1="106.91" y1="97.14" x2="112.20" y2="94.95"/><line class="rayo" x1="107.48" y1="100.00" x2="127.28" y2="100.00"/><line class="rayo" x1="106.91" y1="102.86" x2="112.20" y2="105.05"/><line class="rayo" x1="105.29" y1="105.29" x2="113.07" y2="113.07"/><line class="rayo" x1="102.86" y1="106.91" x2="105.05" y2="112.20"/><line class="rayo" x1="100.00" y1="107.48" x2="100.00" y2="144.00"/><line class="rayo" x1="97.14" y1="106.91" x2="94.95" y2="112.20"/><line class="rayo" x1="94.71" y1="105.29" x2="86.93" y2="113.07"/><line class="rayo" x1="93.09" y1="102.86" x2="87.80" y2="105.05"/><line class="rayo" x1="92.52" y1="100.00" x2="72.72" y2="100.00"/><line class="rayo" x1="93.09" y1="97.14" x2="87.80" y2="94.95"/><line class="rayo" x1="94.71" y1="94.71" x2="86.93" y2="86.93"/><line class="rayo" x1="97.14" y1="93.09" x2="94.95" y2="87.80"/><circle class="punto" cx="118.67" cy="81.33" r="1.98"/><circle class="punto" cx="118.67" cy="118.67" r="1.98"/><circle class="punto" cx="81.33" cy="118.67" r="1.98"/><circle class="punto" cx="81.33" cy="81.33" r="1.98"/></g></svg>')


def versionar(texto):
    """Añade ?v=<huella> a fotos, CSS y JS para que ningún navegador muestre una copia vieja al cambiarlos."""
    def huella(m):
        ruta = RAIZ / m.group(0)
        return m.group(0) + '?v=' + hashlib.md5(ruta.read_bytes()).hexdigest()[:8] if ruta.exists() else m.group(0)
    return re.sub(r'(?:assets|marca)/[\w./-]+\.(?:jpg|png|webp|css|js)(?![?\w])', huella, texto)

def pagina(archivo, titulo, descripcion, cuerpo, pagina_id='', actual=''):
    def nav(href, txt):
        cur = ' aria-current="page"' if href == actual else ''
        return f'<a href="{href}"{cur}>{txt}</a>'
    html = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descripcion}">
<meta name="theme-color" content="#FAFAFA">
<link rel="icon" type="image/png" sizes="64x64" href="marca/favicon-64.png">
<link rel="icon" type="image/png" sizes="32x32" href="marca/favicon-32.png">
<link rel="apple-touch-icon" href="marca/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/plen.css">
<script src="assets/plen.js" defer></script>
</head>
<body data-pagina="{pagina_id}">
<div class="aurora" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><filter id="refraccion" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.008 0.012" numOctaves="2" seed="7" result="n"/><feGaussianBlur in="n" stdDeviation="2" result="b"/><feDisplacementMap in="SourceGraphic" in2="b" scale="38" xChannelSelector="R" yChannelSelector="G"/></filter><filter id="lente" x="0" y="0" width="44" height="44" filterUnits="userSpaceOnUse" primitiveUnits="userSpaceOnUse" color-interpolation-filters="sRGB"><feImage href="assets/lente-mapa.png" x="0" y="0" width="44" height="44" preserveAspectRatio="none" result="m"/><feDisplacementMap in="SourceGraphic" in2="m" scale="17" xChannelSelector="R" yChannelSelector="G"/></filter></svg>
<div class="lente" aria-hidden="true"><span class="lente__brillo"></span></div><div class="estela" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
<div class="anuncio">Envío gratis desde $150.000 a toda Colombia</div>
<header class="header"><div class="env header__in">
  <nav class="nav">{nav('tienda.html','Tienda')}{nav('magnesio.html','Magnesio')}{nav('index.html#filosofia','Nosotros')}</nav>
  <button class="icono-btn menu-btn" data-menu aria-label="Menú"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M4 8h16M4 16h11"/></svg></button>
  <a class="logo" href="index.html" aria-label="Plen Wellness, inicio"><img src="marca/logo-plen.png" alt="Plen Wellness"></a>
  <div class="acciones">
    <button class="icono-btn" data-abrir-carrito aria-label="Abrir bolsa"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M5 8h14l-1.2 12H6.2z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/></svg><span class="burbuja" data-contador>0</span></button>
  </div>
</div></header>
<div class="menu-movil">
  <button class="icono-btn cerrar" data-menu aria-label="Cerrar"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
  <a href="index.html">Inicio</a><a href="tienda.html">Tienda</a><a href="magnesio.html"><em>Magnesio</em></a><a href="index.html#filosofia">Nosotros</a>
</div>
<main>
{cuerpo}
</main>
<footer class="boletin"><div class="env">
  <div class="boletin__grid">
    <h2 class="display">Bienestar, <em>sin ruido.</em></h2>
    <div><p style="margin-bottom:18px;opacity:.8">Lanzamientos, rituales y 10% en tu primera compra.</p>
      <form class="form-linea" data-boletin><input type="email" required placeholder="Tu correo" aria-label="Tu correo"><button>Suscribirme</button></form>
      <p class="nota-legal">Al suscribirte aceptas nuestra política de datos.</p></div>
  </div>
  <div class="footer__grid">
    <div><img class="footer__logo" src="marca/logo-plen-claro.png" alt="Plen Wellness"><p style="opacity:.6;max-width:280px;font-size:14px">Bienestar esencial, formulado con intención. Hecho en Colombia.</p></div>
    <div><h4>Tienda</h4><a href="magnesio.html">Magnesio</a><a href="tienda.html">Todos los productos</a><a href="tienda.html#pronto">Próximamente</a></div>
    <div><h4>Ayuda</h4><a href="#">Envíos y entregas</a><a href="#">Cambios y devoluciones</a><a href="#">Preguntas frecuentes</a><a href="#">Contacto</a></div>
    <div><h4>Plen</h4><a href="index.html#filosofia">Nosotros</a><a href="#">Instagram</a><a href="#">TikTok</a><a href="#">Términos y condiciones</a></div>
  </div>
  <div class="footer__base"><span>© 2026 Plen Wellness · Magnesio + Zinc: registro sanitario NSA-4231-2026</span>
    <div class="pagos"><span>Visa</span><span>Mastercard</span><span>PSE</span><span>Nequi</span></div></div>
</div></footer>
</body>
</html>
'''
    html = versionar(html)
    (RAIZ / archivo).write_text(html, encoding='utf-8')
    print('✓', archivo)


def tarjeta_magnesio(extra=''):
    return f'''<article class="prod rev {extra}">
      <a class="prod__img" href="magnesio.html"><img src="{FRASCO}" alt="Magnesio + Zinc Plen Wellness" loading="lazy"><span class="prod__tag glass">Nuevo</span></a>
      <button class="prod__add" data-agregar="magnesio" aria-label="Agregar magnesio a la bolsa">{MAS}</button>
      <div class="prod__info"><div><h3>Magnesio + Zinc</h3><p>Bisglicinato · 100 unidades</p></div><span class="p">$89.000</span></div>
    </article>'''


def tarjeta_pronto(nombre, desc, extra=''):
    return f'''<article class="prod prod--pronto rev {extra}">
      <a class="prod__img" href="#" data-pronto><div class="frasco-sil"><span>{nombre.split()[0]}</span></div><span class="prod__tag glass">Muy pronto</span></a>
      <div class="prod__info"><div><h3>{nombre}</h3><p>{desc}</p></div><span class="p suave">—</span></div>
    </article>'''


PRONTO = [('Omega 3', 'Aceite de pescado'), ('Colágeno', 'Hidrolizado'), ('Vitamina D3 + K2', 'Gotas'),
          ('Ashwagandha', 'Adaptógeno'), ('Creatina', 'Monohidrato'), ('Probiótico', '10 cepas')]

ICONOS = {
    'musculo': '<svg viewBox="0 0 40 40"><path d="M8 26c4-10 10-14 16-14 4 0 7 2 8 5"/><path d="M8 26c6 3 14 3 20-2"/><circle cx="20" cy="20" r="17"/></svg>',
    'calma': '<svg viewBox="0 0 40 40"><path d="M26 8a13 13 0 1 0 6 18A11 11 0 0 1 26 8z"/></svg>',
    'absorcion': '<svg viewBox="0 0 40 40"><path d="M20 5c6 8 10 13 10 19a10 10 0 0 1-20 0c0-6 4-11 10-19z"/><path d="M15 25a5 5 0 0 0 5 5"/></svg>',
    'energia': '<svg viewBox="0 0 40 40"><path d="M20 4v10M20 26v10M4 20h10M26 20h10M9 9l6 6M25 25l6 6M31 9l-6 6M15 25l-6 6"/></svg>',
    'defensas': '<svg viewBox="0 0 40 40"><path d="M20 5l12 5v9c0 8-5 13-12 16C13 32 8 27 8 19v-9z"/><path d="M15 20l4 4 7-8"/></svg>',
    'dia': '<svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="15"/><path d="M20 11v9l6 4"/></svg>',
    'registro': '<svg viewBox="0 0 40 40"><rect x="9" y="6" width="22" height="28" rx="3"/><path d="M14 14h12M14 20h12M14 26h7"/></svg>',
}

# ------------------------------------------------------------------ INICIO
inicio = f'''
<section class="hero"><div class="env hero__grid">
  <div class="hero__txt">
    <p class="eyebrow rev">Nuevo · Magnesio + zinc</p>
    <h1 class="display rev d1">El ritual<span class="fina"><em>que tu cuerpo</em></span>te pedía</h1>
    <p class="rev d2">Bienestar esencial, formulado con intención. Empezamos por dos minerales que tu cuerpo usa todos los días: magnesio y zinc.</p>
    <div class="hero__cta rev d3"><a class="btn" href="magnesio.html">Comprar ahora {FLECHA}</a><a class="btn btn--glass" href="#filosofia">Conocer Plen</a></div>
  </div>
  <div class="hero__foto rev d1">
    <div class="arco"><img src="{FRASCO}" alt="Frasco de magnesio Plen Wellness"></div>
    {SELLO}
    <div class="gota gota--capsula" aria-hidden="true"></div><div class="gota gota--esfera" aria-hidden="true"></div>
    <div class="chip-flota glass"><b>100 unidades</b>Una al día, con un vaso de agua o tu bebida preferida.</div>
  </div>
</div><span class="scroll-v">Desliza</span></section>

<div class="cinta" aria-hidden="true"><div class="cinta__pista">
  {''.join('<span>Nuevo</span><span><i>magnesio + zinc</i></span><span>Bisglicinato</span><span>Una al día</span><span>Hecho en Colombia</span><span><i>bienestar, sin ruido</i></span>' for _ in range(4))}
</div></div>

<section class="sec"><div class="insignia rev"><div class="insignia__grid">
  <div class="capsula"><img src="assets/img/mano.jpg" alt="Mano sosteniendo una unidad de Plen Magnesio + Zinc" loading="lazy"></div>
  <div>
    <p class="eyebrow">Fórmula insignia · 01</p>
    <h2 class="display">Magnesio <em>+&nbsp;zinc</em></h2>
    <p>Bisglicinato de zinc y bisglicinato de magnesio: minerales unidos a glicina, un aminoácido. En una pequeña unidad de gelatina con centro líquido, una al día.</p>
    <ul class="lista-check"><li>Magnesio y zinc en forma bisglicinato</li><li>Contribuye al funcionamiento normal de los músculos</li><li>Una unidad al día</li><li>Registro sanitario NSA-4231-2026</li></ul>
    <div class="precio">$89.000 <small>100 unidades · 60 g</small></div>
    <div class="hero__cta"><button class="btn" data-agregar="magnesio">Agregar a la bolsa</button><a class="btn btn--glass" href="magnesio.html">Ver detalles</a></div>
  </div>
</div></div></section>

<section class="sec" style="padding-top:0"><div class="env">
  <div class="sec__cab"><h2 class="display rev">Por qué <em>magnesio</em></h2><p class="suave rev" style="max-width:360px">Participa en más de 300 procesos del cuerpo, y no siempre lo obtenemos de la comida.</p></div>
  <div class="beneficios">
    <div class="beneficio glass rev">{ICONOS['musculo']}<h3>Músculo</h3><p>El magnesio contribuye al funcionamiento normal de los músculos.</p></div>
    <div class="beneficio glass rev d1">{ICONOS['calma']}<h3>Calma</h3><p>El magnesio contribuye al funcionamiento normal del sistema nervioso.</p></div>
    <div class="beneficio glass rev d2">{ICONOS['energia']}<h3>Energía</h3><p>El magnesio contribuye a disminuir el cansancio y la fatiga.</p></div>
    <div class="beneficio glass rev d3">{ICONOS['defensas']}<h3>Defensas</h3><p>El zinc contribuye al funcionamiento normal del sistema inmunitario.</p></div>
  </div>
</div></section>

<section class="sec" id="filosofia" style="padding-top:0"><div class="env filo">
  <div class="filo__fotos rev"><div class="f1"><img src="assets/img/polvo.jpg" alt="Unidades de gelatina con centro líquido junto a magnesio en polvo" loading="lazy"></div><div class="f2"><img src="assets/img/mano.jpg" alt="" loading="lazy"></div></div>
  <div>
    <p class="eyebrow rev">Nuestra filosofía</p>
    <h2 class="display rev d1">Menos, <em>pero mejor</em></h2>
    <p class="rev d2">Plen nace de una idea sencilla: tu bienestar no necesita más ruido, necesita lo esencial bien hecho. Pocos ingredientes, las mejores formas, dosis honestas.</p>
    <p class="rev d2">Sin promesas milagrosas. Solo un ritual diario que se siente bien.</p>
    <div class="cifras rev d3"><div><b>02</b><span>Minerales clave</span></div><div><b>100</b><span>Unidades</span></div><div><b>01</b><span>Al día</span></div></div>
  </div>
</div></section>

<section class="editorial rev"><img src="assets/img/mar.jpg" alt="Mujer frente al mar" loading="lazy">
  <div class="editorial__txt"><div class="panel-glass glass"><p class="eyebrow">Plen Wellness</p><h2 class="display">el bienestar<br><em>es libertad</em></h2></div><a class="btn btn--glass" href="magnesio.html">Empieza tu ritual {FLECHA}</a></div>
</section>

<section class="sec"><div class="env">
  <div class="sec__cab"><h2 class="display rev">La <em>colección</em></h2><a class="aviso-link rev" href="tienda.html">Ver todo</a></div>
  <div class="productos">
    {tarjeta_magnesio()}
    {tarjeta_pronto(*PRONTO[0], 'd1')}
    {tarjeta_pronto(*PRONTO[1], 'd2')}
    {tarjeta_pronto(*PRONTO[2], 'd3')}
  </div>
</div></section>

<section class="sec" style="padding-top:0"><div class="env">
  <div class="sec__cab"><h2 class="display rev">Tu <em>ritual</em></h2></div>
  <div class="pasos">
    <div class="paso rev"><h3>Pide</h3><p>Elige compra única o suscríbete y ahorra 15% en cada envío.</p></div>
    <div class="paso rev d1"><h3>Recibe</h3><p>Te llega a casa en 2 a 5 días hábiles, en cualquier ciudad de Colombia.</p></div>
    <div class="paso rev d2"><h3>Disfruta</h3><p>Una unidad al día con un vaso de agua o tu bebida preferida. La constancia es la clave.</p></div>
  </div>
</div></section>
'''
pagina('index.html', 'Plen Wellness · Bienestar esencial', 'Plen Wellness, hecho en Colombia. Compra Magnesio + Zinc bisglicinato: 100 unidades de gelatina con centro líquido, una al día, con envío a todo el país.', inicio, 'inicio')

# ------------------------------------------------------------------ TIENDA
tienda = f'''
<section class="sec" style="padding-top:clamp(40px,6vw,80px)"><div class="env">
  <p class="eyebrow rev">Tienda</p>
  <div class="sec__cab"><h1 class="display rev d1" style="font-size:clamp(56px,8vw,120px)">Todo <em>Plen</em></h1><p class="suave rev" style="max-width:340px">Empezamos con lo esencial. Cada mes sumamos una nueva fórmula.</p></div>
  <div class="productos">{tarjeta_magnesio()}</div>
  <div class="sec__cab" id="pronto" style="margin-top:clamp(70px,9vw,120px)"><h2 class="display rev">Muy <em>pronto</em></h2></div>
  <div class="productos">{''.join(tarjeta_pronto(n, d, f'd{i % 4}') for i, (n, d) in enumerate(PRONTO))}</div>
</div></section>
'''
pagina('tienda.html', 'Tienda · Plen Wellness', 'Todos los productos Plen Wellness.', tienda, 'tienda', 'tienda.html')

# ------------------------------------------------------------------ PRODUCTO
CHIPS = [('musculo', 'Músculo y nervios'), ('absorcion', 'Bisglicinato'), ('dia', 'Una al día'), ('registro', 'NSA-4231-2026')]
producto = f'''
<div class="env"><nav class="migas"><a href="index.html">Inicio</a> / <a href="tienda.html">Tienda</a> / Magnesio + Zinc</nav>
<section class="pdp">
  <div class="galeria">
    <div class="miniaturas">
      <button class="si" data-src="{FRASCO}"><img src="{FRASCO}" alt="Frasco"></button>
      <button data-src="assets/img/frasco-luz.jpg"><img src="assets/img/frasco-luz.jpg" alt="Frasco con luz de ventana"></button>
      <button data-src="assets/img/polvo.jpg"><img src="assets/img/polvo.jpg" alt="Unidades de gelatina con centro líquido"></button>
      <button data-src="assets/img/mano.jpg"><img src="assets/img/mano.jpg" alt="Una unidad en la mano"></button>
    </div>
    <div class="foto-grande"><img src="{FRASCO}" alt="Frasco de Magnesio + Zinc bisglicinato Plen Wellness"></div>
  </div>
  <div class="pdp__info">
    <p class="eyebrow">Alimento de gelatina con centro líquido</p>
    <h1 class="display">Magnesio <em>+&nbsp;zinc</em></h1>
    <p class="pdp__sub">Bisglicinato de zinc | bisglicinato de magnesio. 100 unidades de gelatina con centro líquido, una al día.</p>
    <div class="chips">{''.join(f'<div>{ICONOS[i]}{t}</div>' for i, t in CHIPS)}</div>
    <div class="opciones">
      <label class="opcion glass"><input type="radio" name="plan" value="suscripcion" checked>
        <div><b>Suscríbete y ahorra</b><small>Llega antes de que se acabe el tuyo · Pausa o cancela cuando quieras</small><span class="ahorro" style="display:inline-block;margin-top:10px">Ahorra 15%</span></div>
        <div class="val"><s>$89.000</s>$75.650</div></label>
      <label class="opcion glass"><input type="radio" name="plan" value="unica">
        <div><b>Compra única</b><small>Un frasco, sin compromiso</small></div>
        <div class="val">$89.000</div></label>
    </div>
    <div class="comprar">
      <div class="cant"><button data-cmenos aria-label="Menos">−</button><span data-cant>1</span><button data-cmas aria-label="Más">+</button></div>
      <button class="btn" data-comprar>Agregar · <span data-precio-btn>$75.650</span></button>
    </div>
    <p class="garantias">Envío gratis desde $150.000 · Pago seguro · Tarjeta, PSE y Nequi</p>
    <div class="acordeon">
      <details open><summary>Qué incluye <span class="mas"></span></summary><div class="resp">1 frasco de vidrio ámbar con 100 unidades de gelatina con centro líquido (60 g), con bisglicinato de zinc y bisglicinato de magnesio. Rinde 100 días, a una unidad al día.</div></details>
      <details><summary>Beneficios <span class="mas"></span></summary><div class="resp"><ul><li>El magnesio contribuye al funcionamiento normal de los músculos.</li><li>El magnesio contribuye al funcionamiento normal del sistema nervioso.</li><li>El magnesio contribuye a disminuir el cansancio y la fatiga.</li><li>El zinc contribuye al funcionamiento normal del sistema inmunitario.</li><li>Minerales en forma bisglicinato (unidos a glicina).</li></ul><p style="margin-top:10px;font-size:13px">Como parte de una alimentación variada y equilibrada y un estilo de vida saludable.</p></div></details>
      <details><summary>Cómo tomarlo <span class="mas"></span></summary><div class="resp">Toma 1 unidad al día con un vaso de agua o tu bebida preferida. Guárdalo en un lugar fresco y seco, protegido de la luz solar directa.</div></details>
      <details><summary>Ingredientes <span class="mas"></span></summary><div class="resp">
        <p>Gelatina con centro líquido, agua purificada, humectante glicerina, color (E 150a), bisglicinato de zinc, bisglicinato de magnesio.</p>
        <table class="tabla-nut" style="margin-top:12px"><tr><td>Presentación</td><td>Alimento de gelatina con centro líquido</td></tr><tr><td>Contenido neto</td><td>100 unidades · 60 g</td></tr><tr><td>Porciones por envase</td><td>100</td></tr><tr><td>Modo de uso</td><td>1 unidad al día</td></tr></table>
        <p style="margin-top:12px;font-size:13px">Registro sanitario NSA-4231-2026 · Elaborado por PRAME S.A.S. para OSANA NUTRACEUTICA, Sabaneta (Colombia).</p></div></details>
      <details><summary>Advertencias <span class="mas"></span></summary><div class="resp">Este producto es un alimento y debe comercializarse como tal. No usar si el sello de seguridad está roto o no lo tiene. Consulta a tu médico si estás en embarazo, lactancia o tomas medicamentos. Mantener fuera del alcance de los niños.</div></details>
    </div>
  </div>
</section></div>

<div class="cinta" aria-hidden="true" style="margin-top:60px"><div class="cinta__pista">
  {''.join('<span>Músculo</span><span><i>calma</i></span><span>Energía</span><span>Bisglicinato</span><span><i>una al día</i></span>' for _ in range(4))}
</div></div>

<section class="sec"><div class="env">
  <div class="sec__cab"><h2 class="display rev">Preguntas <em>frecuentes</em></h2></div>
  <div class="faq">
    <details class="rev"><summary>¿Cuándo es mejor tomarlo? <span class="mas"></span></summary><p class="resp">Muchas personas lo prefieren en la noche, como parte de su rutina antes de dormir. Lo importante es tomarlo todos los días.</p></details>
    <details class="rev"><summary>¿Qué es un alimento de gelatina con centro líquido? <span class="mas"></span></summary><p class="resp">Es la presentación de Plen: una pequeña unidad de gelatina con el centro líquido, que tomas con un vaso de agua o tu bebida preferida. Es un alimento, con registro sanitario NSA-4231-2026.</p></details>
    <details class="rev"><summary>¿Por qué bisglicinato? <span class="mas"></span></summary><p class="resp">El bisglicinato es el mineral unido a glicina, un aminoácido. Es una de las formas de magnesio y zinc más usadas hoy, y suele sentarle bien al estómago.</p></details>
    <details class="rev"><summary>¿Cómo funciona la suscripción? <span class="mas"></span></summary><p class="resp">Cada frasco rinde 100 días. Te llega uno nuevo antes de que se acabe el tuyo, con 15% de descuento. Puedes pausar, cambiar la fecha o cancelar cuando quieras, sin costo.</p></details>
    <details class="rev"><summary>¿Cuánto se demora el envío? <span class="mas"></span></summary><p class="resp">De 2 a 5 días hábiles a cualquier ciudad de Colombia. Envío gratis en compras desde $150.000.</p></details>
  </div>
</div></section>

<section class="sec" style="padding-top:0"><div class="env">
  <div class="sec__cab"><h2 class="display rev">También <em>te va a gustar</em></h2><a class="aviso-link" href="tienda.html#pronto">Ver próximos</a></div>
  <div class="productos">{''.join(tarjeta_pronto(n, d, f'd{i}') for i, (n, d) in enumerate(PRONTO[:4]))}</div>
</div></section>

<div class="barra-fija glass"><span>Magnesio + Zinc · <span data-precio-btn>$75.650</span></span><button class="btn" data-comprar>Agregar</button></div>
'''
pagina('magnesio.html', 'Magnesio + Zinc bisglicinato · Plen Wellness', 'Magnesio + Zinc bisglicinato Plen Wellness: 100 unidades de gelatina con centro líquido, una al día. Compra en línea con envío a toda Colombia.', producto, 'producto', 'magnesio.html')

# ------------------------------------------------------------------ PEDIDO
pedido = '''
<div class="env"><nav class="migas"><a href="index.html">Inicio</a> / Finalizar compra</nav>
<section class="pedido">
  <form data-form-pedido>
    <h1 class="display">Finalizar <em>compra</em></h1>
    <div class="bloque glass"><h2>Contacto <span>01</span></h2><div class="campos">
      <div class="campo campo--ancho"><label for="nombre">Nombre completo</label><input id="nombre" name="nombre" required autocomplete="name"></div>
      <div class="campo"><label for="correo">Correo</label><input id="correo" name="correo" type="email" required autocomplete="email"></div>
      <div class="campo"><label for="celular">Celular</label><input id="celular" name="celular" type="tel" required autocomplete="tel"></div>
    </div></div>
    <div class="bloque glass"><h2>Envío <span>02</span></h2><div class="campos">
      <div class="campo"><label for="ciudad">Ciudad</label><input id="ciudad" name="ciudad" required autocomplete="address-level2"></div>
      <div class="campo"><label for="depto">Departamento</label><input id="depto" name="depto" required autocomplete="address-level1"></div>
      <div class="campo campo--ancho"><label for="direccion">Dirección</label><input id="direccion" name="direccion" required autocomplete="street-address" placeholder="Calle, número, apto o casa"></div>
    </div></div>
    <div class="bloque glass"><h2>Pago <span>03</span></h2><div class="metodos">
      <label class="metodo glass"><input type="radio" name="pago" value="Tarjeta" checked><svg viewBox="0 0 28 28"><rect x="3" y="6" width="22" height="16" rx="3"/><path d="M3 11h22"/></svg>Tarjeta</label>
      <label class="metodo glass"><input type="radio" name="pago" value="PSE"><svg viewBox="0 0 28 28"><path d="M4 11l10-6 10 6M6 11v9M11 11v9M17 11v9M22 11v9M4 23h20"/></svg>PSE</label>
      <label class="metodo glass"><input type="radio" name="pago" value="Nequi"><svg viewBox="0 0 28 28"><rect x="8" y="3" width="12" height="22" rx="3"/><path d="M12 21h4"/></svg>Nequi</label>
    </div></div>
    <button class="btn btn--ancho" style="height:60px">Pagar pedido</button>
    <p class="nota-demo">Vista de diseño: la pasarela de pago se conecta en el siguiente paso.</p>
  </form>
  <aside class="resumen glass"><h2>Tu pedido</h2><div data-resumen></div></aside>
</section></div>
'''
pagina('pedido.html', 'Finalizar compra · Plen Wellness', 'Finaliza tu pedido Plen Wellness.', pedido, 'pedido')
