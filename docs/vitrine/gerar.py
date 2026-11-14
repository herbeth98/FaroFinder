# Gera as ilustrações da página do GitHub (README). Rode: python docs/vitrine/gerar.py
# São SVG animados com CSS: o GitHub mostra a animação; quem pediu "reduzir movimento" vê tudo parado.
import random
from pathlib import Path

AQUI = Path(__file__).parent
FONTE = "'Segoe UI Variable Display','Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"
AZUL, INDIGO, CIANO = "#0a84ff", "#5e5ce6", "#64d2ff"
TEXTO, CINZA = "#f5f5f7", "#a1a1aa"


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(nome, w, h, corpo, css="", parado=""):
    base = f"""
    text {{ font-family: {FONTE}; }}
    .a {{ transform-box: fill-box; transform-origin: center; }}
    @keyframes deriva1 {{ 50% {{ transform: translate(60px, -30px) scale(1.12); }} }}
    @keyframes deriva2 {{ 50% {{ transform: translate(-70px, 40px) scale(.92); }} }}
    @keyframes deriva3 {{ 50% {{ transform: translate(40px, 50px) scale(1.08); }} }}
    .b1 {{ animation: deriva1 18s ease-in-out infinite; }}
    .b2 {{ animation: deriva2 22s ease-in-out infinite; }}
    .b3 {{ animation: deriva3 26s ease-in-out infinite; }}
    """
    quieto = f"@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} {parado} }}"
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f"<style>{base}{css}{quieto}</style>{corpo}</svg>\n")
    (AQUI / f"{nome}.svg").write_text(doc, encoding="utf-8")


def fundo(w, h, cores=(AZUL, INDIGO, CIANO), forca=.45, raio=28):
    """Cartão escuro com manchas de cor que derivam devagar (o mesmo fundo aurora do app)."""
    id_ = f"f{w}x{h}"
    c1, c2, c3 = cores
    return f"""
    <defs>
      <linearGradient id="{id_}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#070a14"/><stop offset="1" stop-color="#0c1630"/></linearGradient>
      <filter id="nev{id_}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="70"/></filter>
      <clipPath id="c{id_}"><rect width="{w}" height="{h}" rx="{raio}"/></clipPath>
    </defs>
    <g clip-path="url(#c{id_})">
      <rect width="{w}" height="{h}" fill="url(#{id_})"/>
      <g filter="url(#nev{id_})" opacity="{forca}">
        <circle class="a b1" cx="{w*.15}" cy="{h*.2}" r="{min(w,h)*.42}" fill="{c1}"/>
        <circle class="a b2" cx="{w*.85}" cy="{h*.25}" r="{min(w,h)*.36}" fill="{c2}"/>
        <circle class="a b3" cx="{w*.6}" cy="{h*.95}" r="{min(w,h)*.4}" fill="{c3}" opacity=".7"/>
      </g>
      <rect width="{w}" height="{h}" rx="{raio}" fill="none" stroke="#ffffff" stroke-opacity=".08" stroke-width="2"/>
    </g>"""


# ------------------------------------------------------------------ cenas das miniaturas
def cena(tipo, x, y, w, h, r=10, sem=0):
    rnd = random.Random(sem)
    cid = f"t{tipo}{x}{y}{sem}"
    p = [f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath><g clip-path="url(#{cid})">']
    j = rnd.uniform(-.12, .12)
    if tipo == "praia":
        p += [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#8fd3ff"/>',
              f'<rect x="{x}" y="{y}" width="{w}" height="{h*.35}" fill="#c9ecff"/>',
              f'<circle cx="{x+w*(.72+j)}" cy="{y+h*.28}" r="{h*.13}" fill="#ffd54f"/>',
              f'<rect x="{x}" y="{y+h*.55}" width="{w}" height="{h*.2}" fill="#1e88e5"/>',
              f'<path d="M{x} {y+h*.72} Q{x+w*.5} {y+h*.62} {x+w} {y+h*.74} V{y+h} H{x}Z" fill="#f3d9a4"/>',
              f'<circle cx="{x+w*(.35+j)}" cy="{y+h*.7}" r="{h*.05}" fill="#6d4c41"/>',
              f'<rect x="{x+w*(.35+j)-h*.04}" y="{y+h*.74}" width="{h*.08}" height="{h*.13}" rx="{h*.03}" fill="#ef5350"/>']
    elif tipo == "bolo":
        cor = rnd.choice(["#f48fb1", "#ce93d8", "#ffab91"])
        p += [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ffe3ec"/>',
              f'<circle cx="{x+w*.15}" cy="{y+h*.2}" r="{h*.07}" fill="#fff59d"/><circle cx="{x+w*.85}" cy="{y+h*.25}" r="{h*.05}" fill="#b3e5fc"/>',
              f'<rect x="{x+w*.25}" y="{y+h*.5}" width="{w*.5}" height="{h*.32}" rx="6" fill="{cor}"/>',
              f'<rect x="{x+w*.25}" y="{y+h*.5}" width="{w*.5}" height="{h*.08}" rx="4" fill="#fff"/>',
              f'<rect x="{x+w*.2}" y="{y+h*.8}" width="{w*.6}" height="{h*.05}" rx="3" fill="#bcaaa4"/>']
        for k in range(3):
            cx = x + w * (.38 + k * .12)
            p += [f'<rect x="{cx-2}" y="{y+h*.36}" width="4" height="{h*.14}" fill="#64b5f6"/>',
                  f'<ellipse cx="{cx}" cy="{y+h*.32}" rx="3" ry="6" fill="#ffb300"/>']
    elif tipo == "palco":
        p += [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#140b2e"/>']
        for k, c in enumerate(["#ff4fd8", "#64d2ff", "#ffd54f"]):
            cx = x + w * (.25 + k * .25 + j / 2)
            p += [f'<path d="M{cx} {y} L{cx-w*.16} {y+h*.75} L{cx+w*.16} {y+h*.75}Z" fill="{c}" opacity=".28"/>']
        p += [f'<rect x="{x}" y="{y+h*.72}" width="{w}" height="{h*.06}" fill="#3a2a6e"/>']
        for k in range(9):
            p += [f'<circle cx="{x+w*(k+.5)/9}" cy="{y+h*(.92+rnd.uniform(-.03,.03))}" r="{h*.07}" fill="#05030d"/>']
    elif tipo == "sol":
        p += [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ff8a65"/>',
              f'<rect x="{x}" y="{y}" width="{w}" height="{h*.4}" fill="#7e57c2" opacity=".55"/>',
              f'<circle cx="{x+w*(.5+j)}" cy="{y+h*.66}" r="{h*.2}" fill="#ffe082"/>',
              f'<path d="M{x} {y+h*.7} Q{x+w*.3} {y+h*.55} {x+w*.6} {y+h*.72} T{x+w} {y+h*.66} V{y+h} H{x}Z" fill="#3e2723"/>']
    elif tipo == "montanha":
        p += [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#b3e5fc"/>',
              f'<path d="M{x-10} {y+h} L{x+w*(.3+j)} {y+h*.3} L{x+w*.62} {y+h}Z" fill="#546e7a"/>',
              f'<path d="M{x+w*.35} {y+h} L{x+w*(.7+j)} {y+h*.42} L{x+w+10} {y+h}Z" fill="#78909c"/>',
              f'<path d="M{x+w*(.3+j)} {y+h*.3} l{-w*.07} {h*.13} l{w*.14} 0Z" fill="#fff"/>']
    elif tipo == "festa":
        p += [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#311b92"/>']
        for k in range(22):
            p += [f'<rect x="{x+rnd.uniform(0,w)}" y="{y+rnd.uniform(0,h)}" width="6" height="3" rx="1.5" fill="{rnd.choice(["#ffd54f","#ff4fd8","#64d2ff","#69f0ae"])}" transform="rotate({rnd.randint(0,180)} {x+w/2} {y+h/2})"/>']
    elif tipo == "faixa":
        p += [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#9ccc65"/>',
              f'<rect x="{x}" y="{y}" width="{w}" height="{h*.45}" fill="#b3e5fc"/>',
              f'<rect x="{x+w*.08}" y="{y+h*.22}" width="{w*.84}" height="{h*.3}" rx="4" fill="#fff"/>',
              f'<rect x="{x+w*.16}" y="{y+h*.31}" width="{w*.68}" height="{h*.05}" rx="2" fill="#1565c0"/>',
              f'<rect x="{x+w*.24}" y="{y+h*.4}" width="{w*.52}" height="{h*.04}" rx="2" fill="#ef5350"/>']
        for k in range(6):
            p += [f'<circle cx="{x+w*(k+.5)/6}" cy="{y+h*.85}" r="{h*.09}" fill="#33691e"/>']
    p.append("</g>")
    return "".join(p)


# ------------------------------------------------------------------ peças de texto
def bloco(x, y, sobre, titulo, texto, largura_titulo=None, cor=AZUL):
    s = [f'<text x="{x}" y="{y}" font-size="17" font-weight="700" letter-spacing="2.2" fill="{cor}">{esc(sobre)}</text>']
    for i, linha in enumerate(titulo):
        s.append(f'<text x="{x}" y="{y+56+i*52}" font-size="44" font-weight="700" letter-spacing="-1.2" fill="{TEXTO}">{esc(linha)}</text>')
    y2 = y + 56 + len(titulo) * 52 + 18
    for i, linha in enumerate(texto):
        s.append(f'<text x="{x}" y="{y2+i*33}" font-size="22" fill="{CINZA}">{esc(linha)}</text>')
    return "".join(s)


def pilula(x, y, w, texto, h=48, tam=19):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="#1c1c22" stroke="#ffffff" stroke-opacity=".14"/>'
            f'<circle cx="{x+26}" cy="{y+h/2-2}" r="8" fill="none" stroke="{CINZA}" stroke-width="2.4"/>'
            f'<path d="M{x+32} {y+h/2+4} l6 6" stroke="{CINZA}" stroke-width="2.6" stroke-linecap="round"/>'
            f'<text x="{x+50}" y="{y+h/2+7}" font-size="{tam}" fill="{TEXTO}">{esc(texto)}</text>')


def silhueta(cx, cy, r, cor):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{cor}"/>'
            f'<path d="M{cx-r*1.7} {cy+r*3.2} Q{cx-r*1.7} {cy+r*1.2} {cx} {cy+r*1.2} Q{cx+r*1.7} {cy+r*1.2} {cx+r*1.7} {cy+r*3.2}Z" fill="{cor}"/>')


# ================================================================== 1. abertura
def abertura():
    W, H = 1200, 700
    frases = [("criança na praia", "praia", "1.284"), ("bolo de aniversário", "bolo", "362"),
              ("palco com público", "palco", "917"), ("pôr do sol", "sol", "2.051")]
    P = 4 * len(frases)
    css = f"""
    @keyframes vez {{ 0% {{ opacity: 0; }} 2% {{ opacity: 1; }} 23% {{ opacity: 1; }} 25%, 100% {{ opacity: 0; }} }}
    @keyframes digita {{ 0% {{ transform: scaleX(0); }} 7%, 100% {{ transform: scaleX(1); }} }}
    @keyframes chega {{ 0%, 6% {{ opacity: 0; transform: translateY(14px) scale(.94); }}
                       10% {{ opacity: 1; transform: none; }} 23% {{ opacity: 1; transform: none; }} 25%, 100% {{ opacity: 0; }} }}
    @keyframes pisca {{ 50% {{ opacity: 0; }} }}
    .vez {{ animation: vez {P}s linear infinite both; }}
    .dig {{ transform-box: fill-box; transform-origin: left center; animation: digita {P}s linear infinite both; }}
    .tile {{ animation: chega {P}s cubic-bezier(.2,.8,.2,1) infinite both; }}
    .cursor {{ animation: pisca 1s steps(1) infinite; }}
    """
    parado = ".outra { display: none; }"
    c = [fundo(W, H, forca=.5)]
    c.append(f'<text x="{W/2}" y="92" text-anchor="middle" font-size="18" font-weight="700" letter-spacing="2.4" fill="{CIANO}">BUSCADORFAST · PARA WINDOWS</text>')
    c.append(f'<text x="{W/2}" y="158" text-anchor="middle" font-size="58" font-weight="700" letter-spacing="-1.8" fill="{TEXTO}">Toda foto que você já tirou,</text>')
    c.append('<defs><linearGradient id="tit" x1="0" x2="1"><stop offset="0" stop-color="#64d2ff"/><stop offset=".5" stop-color="#0a84ff"/><stop offset="1" stop-color="#a78bfa"/></linearGradient></defs>')
    c.append(f'<text x="{W/2}" y="222" text-anchor="middle" font-size="58" font-weight="700" letter-spacing="-1.8" fill="url(#tit)">a uma frase de distância.</text>')
    # janela do app
    wx, wy, ww, wh = 110, 270, 980, 390
    c.append(f'<rect x="{wx}" y="{wy+10}" width="{ww}" height="{wh}" rx="22" fill="#000" opacity=".35"/>')
    c.append(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="22" fill="#111117" stroke="#ffffff" stroke-opacity=".12"/>')
    for k, cor in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        c.append(f'<circle cx="{wx+26+k*20}" cy="{wy+24}" r="6" fill="{cor}"/>')
    sx, sy, sw = wx + 210, wy + 46, 560
    c.append(f'<rect x="{sx-3}" y="{sy-3}" width="{sw+6}" height="56" rx="28" fill="none" stroke="url(#tit)" stroke-width="2" opacity=".9"/>')
    c.append(pilula(sx, sy, sw, "", h=50))
    gx, gy, tw, th, gap = wx + 26, wy + 150, 176, 106, 12
    for i, (frase, tipo, total) in reversed(list(enumerate(frases))):
        atraso = f"animation-delay: {i*4 - 1.8:.2f}s"   # a primeira busca já aparece pronta
        outra = " outra" if i else ""
        cid = f"dg{i}"
        c.append(f'<g class="vez{outra}" style="{atraso}">')
        c.append(f'<clipPath id="{cid}"><rect class="dig" style="{atraso}" x="{sx+48}" y="{sy+8}" width="{len(frase)*11.5+6}" height="34"/></clipPath>')
        c.append(f'<g clip-path="url(#{cid})"><text x="{sx+50}" y="{sy+32}" font-size="20" fill="{TEXTO}">{esc(frase)}</text></g>')
        c.append(f'<text x="{gx}" y="{gy-16}" font-size="15" fill="{CINZA}">{total} resultados · em todos os discos</text>')
        c.append("</g>")
        for k in range(10):
            col, lin = k % 5, k // 5
            c.append(f'<g class="tile{outra}" style="animation-delay: {i*4 + k*.07 - 1.8:.2f}s">'
                     + cena(tipo, gx + col * (tw + gap), gy + lin * (th + gap), tw, th, sem=i * 20 + k) + "</g>")
    svg("abertura", W, H, "".join(c), css, parado)


# ================================================================== faixas de recurso
def faixa(nome, sobre, titulo, texto, arte, css="", lado="esq", cores=(AZUL, INDIGO, CIANO)):
    W, H = 1200, 470
    tx = 70 if lado == "esq" else 650
    c = [fundo(W, H, cores, forca=.32), bloco(tx, 120, sobre, titulo, texto), arte(640 if lado == "esq" else 60)]
    svg(nome, W, H, "".join(c), css)


def arte_pessoas(x0):
    px, py, pw, ph = x0 + 30, 60, 470, 300
    s = [cena("montanha", px, py, pw, ph, r=18, sem=3)]
    pessoas = [(px + 110, py + 150, "#ffcc80", "Ana"), (px + 235, py + 135, "#a1887f", "Pedro"), (px + 360, py + 155, "#f8bbd0", "Lúcia")]
    for k, (cx, cy, cor, nome) in enumerate(pessoas):
        s.append(silhueta(cx, cy, 30, cor))
        s.append(f'<g class="a quadro" style="animation-delay: {k*.6}s">'
                 f'<rect x="{cx-44}" y="{cy-44}" width="88" height="88" rx="14" fill="none" stroke="{CIANO}" stroke-width="3"/>'
                 f'<rect x="{cx-38}" y="{cy-82}" width="76" height="30" rx="15" fill="{AZUL}"/>'
                 f'<text x="{cx}" y="{cy-61}" text-anchor="middle" font-size="16" font-weight="600" fill="#fff">{nome}</text></g>')
    for k, (_, _, cor, nome) in enumerate(pessoas):
        ax = px + 40 + k * 150
        s.append(f'<g class="a sobe" style="animation-delay: {1.8 + k*.15}s"><rect x="{ax}" y="{py+ph+22}" width="136" height="48" rx="24" fill="#1c1c22" stroke="#fff" stroke-opacity=".12"/>'
                 f'<circle cx="{ax+24}" cy="{py+ph+46}" r="15" fill="{cor}"/>'
                 f'<text x="{ax+48}" y="{py+ph+52}" font-size="17" fill="{TEXTO}">{nome}</text></g>')
    return "".join(s)


CSS_PESSOAS = """
@keyframes quadro { 0%, 8% { opacity: 0; transform: scale(1.25); } 16%, 88% { opacity: 1; transform: none; } 100% { opacity: 0; } }
@keyframes sobe { 0%, 30% { opacity: 0; transform: translateY(10px); } 40%, 90% { opacity: 1; transform: none; } 100% { opacity: 0; } }
.quadro { animation: quadro 6s cubic-bezier(.2,.8,.2,1) infinite both; }
.sobe { animation: sobe 6s cubic-bezier(.2,.8,.2,1) infinite both; }
"""


def arte_texto(x0):
    px, py, pw, ph = x0 + 30, 110, 470, 300
    s = [pilula(px + 60, 40, 350, "formatura 2019", h=46, tam=18)]
    s.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="18" fill="#9ccc65"/>')
    s.append(f'<clipPath id="ft"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="18"/></clipPath><g clip-path="url(#ft)">')
    s.append(f'<rect x="{px}" y="{py}" width="{pw}" height="130" fill="#b3e5fc"/>')
    s.append(f'<rect x="{px+40}" y="{py+70}" width="{pw-80}" height="110" rx="8" fill="#fff" transform="rotate(-2 {px+pw/2} {py+125})"/>')
    s.append(f'<text x="{px+pw/2}" y="{py+128}" text-anchor="middle" font-size="40" font-weight="800" fill="#1565c0" transform="rotate(-2 {px+pw/2} {py+125})">FORMATURA 2019</text>')
    s.append(f'<text x="{px+pw/2}" y="{py+162}" text-anchor="middle" font-size="18" font-weight="700" fill="#ef5350" transform="rotate(-2 {px+pw/2} {py+125})">PARABÉNS, TURMA!</text>')
    for k in range(7):
        s.append(silhueta(px + 35 + k * 67, py + 240, 20, ["#ffcc80", "#a1887f", "#f8bbd0", "#8d6e63", "#ffe0b2", "#bcaaa4", "#d7ccc8"][k]))
    s.append(f'<rect class="a varre" x="{px}" y="{py}" width="{pw}" height="5" fill="{CIANO}" opacity=".9"/>')
    s.append("</g>")
    s.append(f'<rect class="a acha" x="{px+52}" y="{py+88}" width="{pw-104}" height="54" rx="8" fill="{CIANO}" fill-opacity=".14" stroke="{CIANO}" stroke-width="3" transform="rotate(-2 {px+pw/2} {py+125})"/>')
    return "".join(s)


CSS_TEXTO = """
@keyframes varre { 0% { transform: translateY(0); opacity: 0; } 5% { opacity: .9; } 45% { transform: translateY(295px); opacity: .9; } 50%, 100% { transform: translateY(295px); opacity: 0; } }
@keyframes acha { 0%, 42% { opacity: 0; } 50%, 92% { opacity: 1; } 100% { opacity: 0; } }
.varre { transform-box: view-box; animation: varre 5s ease-in-out infinite; }
.acha { transform-box: view-box; animation: acha 5s ease-in-out infinite; }
"""


def arte_fala(x0):
    px, py = x0 + 20, 60
    s = [f'<rect x="{px}" y="{py}" width="290" height="330" rx="18" fill="#0f0f14" stroke="#fff" stroke-opacity=".12"/>']
    s.append(cena("festa", px + 14, py + 14, 262, 180, r=12, sem=7))
    s.append(f'<circle cx="{px+145}" cy="{py+104}" r="28" fill="#000" opacity=".45"/><path d="M{px+136} {py+90} l24 14 l-24 14Z" fill="#fff"/>')
    for k in range(26):
        h = 10 + (k * 37 % 50)
        s.append(f'<rect class="onda" style="animation-delay: {k*.06:.2f}s" x="{px+20+k*9.6}" y="{py+262-h/2}" width="5" height="{h}" rx="2.5" fill="{AZUL if k < 13 else "#3a3a44"}"/>')
    s.append(f'<rect x="{px+20}" y="{py+302}" width="250" height="4" rx="2" fill="#3a3a44"/><rect x="{px+20}" y="{py+302}" width="125" height="4" rx="2" fill="{AZUL}"/>')
    s.append(f'<circle cx="{px+145}" cy="{py+304}" r="7" fill="#fff"/>')
    tx = px + 310
    linhas = [("01:52", "e agora a gente vai cantar", False), ("02:14", "parabéns pra você, nesta", True),
              ("02:19", "data querida, muitas…", False), ("02:31", "assopra, assopra!", False)]
    for k, (t, frase, alvo) in enumerate(linhas):
        y = py + 30 + k * 76
        if alvo:
            s.append(f'<rect class="a marca" x="{tx-10}" y="{y-6}" width="250" height="66" rx="12" fill="{AZUL}" fill-opacity=".18" stroke="{AZUL}" stroke-width="2"/>')
        s.append(f'<text x="{tx}" y="{y+18}" font-size="15" font-weight="700" fill="{CIANO if alvo else CINZA}">{t}</text>')
        s.append(f'<text x="{tx}" y="{y+44}" font-size="18" fill="{TEXTO if alvo else CINZA}">{esc(frase)}</text>')
    return "".join(s)


CSS_FALA = """
@keyframes onda { 50% { transform: scaleY(.35); } }
@keyframes marca { 0%, 100% { opacity: .55; } 50% { opacity: 1; } }
.onda { transform-box: fill-box; transform-origin: center; animation: onda 1.1s ease-in-out infinite; }
.marca { animation: marca 2.4s ease-in-out infinite; }
"""


def arte_sons(x0):
    px, py = x0 + 20, 230
    s = []
    rnd = random.Random(5)
    picos = {9: ("aplausos", "#ffd54f"), 24: ("música", "#ff4fd8"), 39: ("fogos", CIANO), 52: ("latido", "#69f0ae")}
    for k in range(60):
        h = 16 + rnd.random() * 50 + (110 if any(abs(k - p) < 3 for p in picos) else 0)
        cor = next((c for p, (_, c) in picos.items() if abs(k - p) < 3), "#3a3a50")
        s.append(f'<rect class="onda" style="animation-delay: {k*.045:.2f}s" x="{px+k*8.5}" y="{py-h/2}" width="5" height="{h}" rx="2.5" fill="{cor}"/>')
    for n, (p, (nome, cor)) in enumerate(picos.items()):
        x = px + p * 8.5
        y = py - 150 if n % 2 == 0 else py + 110
        s.append(f'<g class="a tag" style="animation-delay: {n*.5}s"><rect x="{x-62}" y="{y}" width="124" height="42" rx="21" fill="#1c1c22" stroke="{cor}" stroke-width="2"/>'
                 f'<circle cx="{x-38}" cy="{y+21}" r="6" fill="{cor}"/><text x="{x-24}" y="{y+27}" font-size="17" fill="{TEXTO}">{nome}</text></g>')
    return "".join(s)


CSS_SONS = CSS_FALA.split("@keyframes marca")[0] + """
@keyframes tag { 0%, 5% { opacity: 0; transform: translateY(8px) scale(.9); } 15%, 85% { opacity: 1; transform: none; } 100% { opacity: 0; } }
.onda { transform-box: fill-box; transform-origin: center; animation: onda 1.3s ease-in-out infinite; }
.tag { animation: tag 5s cubic-bezier(.2,.8,.2,1) infinite both; }
"""


def disco(x, y, nome, info, ligado):
    cor = "#30d158" if ligado else "#8e8e93"
    return (f'<rect x="{x}" y="{y}" width="230" height="74" rx="16" fill="#1c1c22" stroke="#fff" stroke-opacity=".12"/>'
            f'<rect x="{x+18}" y="{y+22}" width="44" height="30" rx="7" fill="none" stroke="{CINZA}" stroke-width="2.4"/>'
            f'<circle cx="{x+52}" cy="{y+37}" r="3" fill="{CINZA}"/>'
            f'<text x="{x+76}" y="{y+33}" font-size="17" font-weight="600" fill="{TEXTO}">{esc(nome)}</text>'
            f'<circle class="{"a pulsa" if ligado else ""}" cx="{x+82}" cy="{y+51}" r="5" fill="{cor}"/>'
            f'<text x="{x+94}" y="{y+56}" font-size="14" fill="{CINZA}">{esc(info)}</text>')


def arte_discos(x0):
    s = [disco(x0 + 20, 50, "Fotos 2015–2020", "conectado", True),
         disco(x0 + 270, 50, "Backup viagens", "na gaveta", False)]
    tipos = ["montanha", "praia", "sol", "festa", "bolo", "palco", "montanha", "praia"]
    for k in range(8):
        col, lin = k % 4, k // 4
        x, y = x0 + 20 + col * 122, 150 + lin * 92
        apagado = col >= 2
        s.append(f'<g opacity="{.42 if apagado else 1}">' + cena(tipos[k], x, y, 112, 82, sem=40 + k) + "</g>")
    s.append(f'<g class="a aviso"><rect x="{x0+270}" y="350" width="230" height="58" rx="14" fill="{AZUL}"/>'
             f'<text x="{x0+385}" y="376" text-anchor="middle" font-size="16" font-weight="600" fill="#fff">Ligue “Backup viagens”</text>'
             f'<text x="{x0+385}" y="397" text-anchor="middle" font-size="14" fill="#fff" fill-opacity=".85">para abrir o original</text></g>')
    s.append(f'<path d="M{x0+385} 350 l-10 -12 h20Z" fill="{AZUL}" class="a aviso"/>')
    return "".join(s)


CSS_DISCOS = """
@keyframes pulsa { 50% { transform: scale(1.6); opacity: .5; } }
@keyframes aviso { 0%, 20% { opacity: 0; transform: translateY(8px); } 30%, 85% { opacity: 1; transform: none; } 100% { opacity: 0; } }
.pulsa { animation: pulsa 1.6s ease-in-out infinite; }
.aviso { animation: aviso 6s cubic-bezier(.2,.8,.2,1) infinite both; }
"""


def arte_organiza(x0):
    s = [f'<rect x="{x0+20}" y="50" width="250" height="360" rx="18" fill="#1c1c22" stroke="#fff" stroke-opacity=".12"/>',
         f'<text x="{x0+40}" y="86" font-size="17" font-weight="600" fill="{TEXTO}">Linha do tempo</text>']
    alturas = [60, 90, 130, 80, 170, 210, 150, 240]
    for k, h in enumerate(alturas):
        s.append(f'<rect class="cresce" style="animation-delay: {k*.08:.2f}s" x="{x0+40+k*27}" y="{370-h}" width="18" height="{h}" rx="5" fill="{AZUL if k == 7 else "#3a3a50"}"/>')
    s.append(f'<text x="{x0+40}" y="395" font-size="13" fill="{CINZA}">2017</text><text x="{x0+250}" y="395" text-anchor="end" font-size="13" fill="{CINZA}">2025</text>')
    mx = x0 + 290
    s.append(f'<rect x="{mx}" y="50" width="230" height="360" rx="18" fill="#132a1f"/>')
    s.append(f'<clipPath id="mapa"><rect x="{mx}" y="50" width="230" height="360" rx="18"/></clipPath><g clip-path="url(#mapa)">'
             f'<path d="M{mx-20} 170 Q{mx+80} 120 {mx+130} 200 T{mx+260} 230" stroke="#1e88e5" stroke-width="18" fill="none" opacity=".6"/>'
             f'<path d="M{mx} 300 L{mx+230} 260 M{mx+60} 50 L{mx+120} 410 M{mx+170} 50 L{mx+190} 410" stroke="#2e4d3c" stroke-width="5"/>'
             f'<path d="M{mx+30} 330 Q{mx+90} 300 {mx+140} 360 T{mx+240} 340 V420 H{mx}Z" fill="#1b3a2a"/></g>')
    for k, (dx, dy) in enumerate([(60, 120), (150, 170), (95, 260), (175, 320)]):
        s.append(f'<g class="pino" style="animation-delay: {.3 + k*.25:.2f}s"><path d="M{mx+dx} {dy+30} c-18 -20 -18 -44 0 -44 s18 24 0 44Z" fill="{["#ff453a", AZUL, "#ffd60a", "#30d158"][k]}"/>'
                 f'<circle cx="{mx+dx}" cy="{dy}" r="5" fill="#fff"/></g>')
    return "".join(s)


CSS_ORGANIZA = """
@keyframes cresce { 0%, 75% { transform: scaleY(1); } 82% { transform: scaleY(0); } 100% { transform: scaleY(1); } }
@keyframes pino { 0%, 72% { opacity: 1; transform: none; } 80% { opacity: 0; transform: translateY(-40px); } 92%, 100% { opacity: 1; transform: none; } }
.cresce { transform-box: fill-box; transform-origin: bottom; animation: cresce 6s cubic-bezier(.2,.8,.2,1) infinite both; }
.pino { animation: pino 6s cubic-bezier(.3,1.4,.5,1) infinite both; }
"""


def arte_celular(x0):
    fx, fy, fw, fh = x0 + 170, 30, 220, 420
    s = [f'<rect x="{fx-8}" y="{fy-8}" width="{fw+16}" height="{fh+16}" rx="46" fill="#2c2c30"/>',
         f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="38" fill="#0b0b0f"/>',
         f'<clipPath id="tela"><rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="38"/></clipPath><g clip-path="url(#tela)">',
         '<g class="rola">']
    tipos = ["praia", "bolo", "montanha", "sol", "palco", "festa", "faixa", "praia", "sol", "montanha", "bolo", "palco"]
    for rep in range(2):
        for k, t in enumerate(tipos):
            col, lin = k % 3, k // 3 + rep * 4
            s.append(cena(t, fx + 6 + col * 70, fy + 96 + lin * 70, 66, 66, r=6, sem=60 + k))
    s.append("</g>")
    s.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="90" fill="#0b0b0f"/>')
    s.append(f'<rect x="{fx+76}" y="{fy+12}" width="68" height="20" rx="10" fill="#000"/>')
    s.append(pilula(fx + 12, fy + 44, fw - 24, "viagem 2023", h=36, tam=15))
    s.append("</g>")
    s.append(f'<g class="a sinal"><circle cx="{x0+60}" cy="200" r="22" fill="none" stroke="{CIANO}" stroke-width="3"/>'
             f'<circle cx="{x0+60}" cy="200" r="44" fill="none" stroke="{CIANO}" stroke-width="3" opacity=".5"/></g>'
             f'<circle cx="{x0+60}" cy="200" r="8" fill="{CIANO}"/>')
    s.append(f'<rect x="{x0-40}" y="250" width="200" height="40" rx="20" fill="#1c1c22" stroke="#fff" stroke-opacity=".12"/>'
             f'<text x="{x0+60}" y="276" text-anchor="middle" font-size="15" fill="{TEXTO}">mesma rede Wi-Fi</text>')
    return "".join(s)


CSS_CELULAR = """
@keyframes rola { to { transform: translateY(-280px); } }
@keyframes sinal { 0% { transform: scale(.6); opacity: 1; } 100% { transform: scale(1.4); opacity: 0; } }
.rola { animation: rola 12s linear infinite; }
.sinal { animation: sinal 2.2s ease-out infinite; }
"""


# ================================================================== privacidade
def privacidade():
    W, H = 1200, 440
    css = """
    @keyframes anel { 0% { transform: scale(.7); opacity: .9; } 100% { transform: scale(1.6); opacity: 0; } }
    .anel { transform-box: fill-box; transform-origin: center; animation: anel 3.6s ease-out infinite; }
    """
    cx, cy = W / 2, 130
    c = [fundo(W, H, ("#30d158", AZUL, CIANO), forca=.3)]
    for k in range(3):
        c.append(f'<circle class="anel" style="animation-delay: {k*1.2}s" cx="{cx}" cy="{cy}" r="56" fill="none" stroke="#30d158" stroke-width="2"/>')
    c.append(f'<circle cx="{cx}" cy="{cy}" r="56" fill="#30d158" fill-opacity=".14" stroke="#30d158" stroke-width="2"/>')
    c.append(f'<rect x="{cx-22}" y="{cy-6}" width="44" height="36" rx="8" fill="#30d158"/>')
    c.append(f'<path d="M{cx-13} {cy-6} v-10 a13 13 0 0 1 26 0 v10" fill="none" stroke="#30d158" stroke-width="6"/>')
    c.append(f'<text x="{cx}" y="{cy+138}" text-anchor="middle" font-size="46" font-weight="700" letter-spacing="-1.2" fill="{TEXTO}">Nada sai do seu computador.</text>')
    c.append(f'<text x="{cx}" y="{cy+186}" text-anchor="middle" font-size="22" fill="{CINZA}">A inteligência artificial roda na sua máquina. Sem conta, sem assinatura</text>')
    c.append(f'<text x="{cx}" y="{cy+218}" text-anchor="middle" font-size="22" fill="{CINZA}">e sem mandar nenhuma foto para a nuvem.</text>')
    svg("privacidade", W, H, "".join(c), css)


# ================================================================== três passos
def passos():
    W, H = 1200, 330
    css = """
    @keyframes vai { 0% { stroke-dashoffset: 40; } 100% { stroke-dashoffset: 0; } }
    .liga { stroke-dasharray: 6 14; animation: vai 1.2s linear infinite; }
    """
    itens = [("1", "Baixe o instalador", ["Um arquivo só, de 3 MB,", "na página de versões."]),
             ("2", "Instale e espere", ["Ele prepara a IA sozinho:", "de 10 a 40 minutos."]),
             ("3", "Indexe e busque", ["Escolha os discos e", "escreva o que procura."])]
    c = [fundo(W, H, forca=.25)]
    for k, (n, tit, txt) in enumerate(itens):
        x = 200 + k * 400
        if k:
            c.append(f'<path class="liga" d="M{x-330} 110 H{x-70}" stroke="{AZUL}" stroke-width="3" stroke-linecap="round" fill="none"/>')
        c.append(f'<circle cx="{x}" cy="110" r="44" fill="{AZUL}" fill-opacity=".16" stroke="{AZUL}" stroke-width="2.5"/>')
        c.append(f'<text x="{x}" y="125" text-anchor="middle" font-size="40" font-weight="700" fill="{TEXTO}">{n}</text>')
        c.append(f'<text x="{x}" y="200" text-anchor="middle" font-size="26" font-weight="700" fill="{TEXTO}">{tit}</text>')
        for i, l in enumerate(txt):
            c.append(f'<text x="{x}" y="{238+i*28}" text-anchor="middle" font-size="19" fill="{CINZA}">{l}</text>')
    svg("passos", W, H, "".join(c), css)


# ================================================================== botão de baixar
def botao():
    W, H = 420, 84
    c = ['<defs><linearGradient id="bt" x1="0" x2="1"><stop offset="0" stop-color="#2997ff"/><stop offset="1" stop-color="#0a6cff"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" rx="{H/2}" fill="url(#bt)"/>',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{H/2-1}" fill="none" stroke="#fff" stroke-opacity=".25"/>',
         '<g transform="translate(46 42)" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">'
         '<path d="M0 -15 V9 M-10 -1 L0 9 L10 -1 M-14 17 H14"/></g>',
         '<text x="84" y="40" font-size="25" font-weight="700" fill="#fff">Baixar para Windows</text>',
         '<text x="84" y="64" font-size="16" fill="#fff" fill-opacity=".85">Windows 10 e 11 · 64 bits</text>']
    svg("baixar", W, H, "".join(c))


abertura()
faixa("pessoas", "PESSOAS", ["Ele reconhece", "quem aparece."],
      ["Junta os rostos da mesma pessoa.", "Você dá o nome uma vez e pronto.", "Acha até as fotos em que duas", "pessoas aparecem juntas."],
      arte_pessoas, CSS_PESSOAS, "esq")
faixa("texto", "ESCRITO NA FOTO", ["Lê faixas, placas", "e documentos."],
      ["Procure “formatura 2019” e ele", "traz a foto da faixa. Serve também", "para aquele documento fotografado", "que sumiu no meio das outras."],
      arte_texto, CSS_TEXTO, "dir")
faixa("fala", "FALADO NOS VÍDEOS", ["O momento exato", "em que alguém disse."],
      ["Os vídeos são transcritos. Ao abrir", "um resultado, o vídeo começa no", "trecho certo, com a fala ao lado."],
      arte_fala, CSS_FALA, "esq")
faixa("sons", "SONS", ["Aplausos, música,", "fogos, latido."],
      ["Procure pelo som e ele mostra", "os vídeos em que ele aparece."],
      arte_sons, CSS_SONS, "dir", (INDIGO, "#ff4fd8", CIANO))
faixa("discos", "TODOS OS DISCOS", ["Até os HDs que", "estão na gaveta."],
      ["O catálogo guarda as miniaturas.", "Você vê tudo com o disco desligado,", "e ele avisa qual ligar para abrir", "o arquivo original."],
      arte_discos, CSS_DISCOS, "esq")
faixa("organiza", "ORGANIZAÇÃO", ["Linha do tempo, mapa", "e álbuns prontos."],
      ["Os álbuns se montam sozinhos por", "dia e lugar. E ainda tem duplicados", "para liberar espaço e as fotos", "borradas separadas para revisar."],
      arte_organiza, CSS_ORGANIZA, "dir", ("#30d158", AZUL, CIANO))
faixa("celular", "NO CELULAR", ["Suas fotos no bolso,", "sem nuvem."],
      ["Abra pelo celular na mesma rede", "Wi-Fi, ou de qualquer lugar com", "o Tailscale. Tudo protegido por", "uma chave que só o seu PC gera."],
      arte_celular, CSS_CELULAR, "esq")
privacidade()
passos()
botao()
print("ok:", ", ".join(sorted(p.stem for p in AQUI.glob("*.svg"))))
