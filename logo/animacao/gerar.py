"""Animação da logo FaroFinder: 3840x2160, 30 fps, 10 s.

O visor procura (os cantos chegam e uma linha de busca passa), encontra (a estrela acende com um pulso),
trava o foco e o nome entra letra a letra. Os quadros saem com fundo transparente; o ffmpeg monta
MP4 (fundo grafite), MOV ProRes 4444 (transparente, para o Premiere) e WebM VP9 (transparente, para a web).

Uso: python gerar.py <pasta_saida>    (precisa de pymupdf; partes da logo em web/marca/partes.json)
"""
import json, math, os, subprocess, sys
from concurrent.futures import ProcessPoolExecutor

import pymupdf

AQUI = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(AQUI, '..', '..', 'web', 'marca', 'partes.json')))
W, H, FPS, DUR = 3840, 2160, 30, 10.0
PAPER, BLUE = '#F5F5F4', '#2D7EFC'
S = 2.2                                   # escala da logo (992 x 222 unidades -> 2182 x 488 px)
X0, Y0 = (W - 992 * S) / 2, (H - 222 * S) / 2
SHIFT = 385                               # deslocamento do símbolo quando está sozinho no centro
LETRAS = ['F', 'a', 'r', 'o', 'F2', 'i', 'n', 'd', 'e', 'r2']


def clamp(v): return max(0.0, min(1.0, v))
def prog(t, a, b): return clamp((t - a) / (b - a))
def out_cubic(p): return 1 - (1 - p) ** 3
def in_out(p): return 4 * p ** 3 if p < .5 else 1 - (-2 * p + 2) ** 3 / 2
def out_back(p, k=1.6): return 1 + (k + 1) * (p - 1) ** 3 + k * (p - 1) ** 2


def quadro(i):
    t = i / FPS
    g = []
    # 1. cantos chegam de fora (0,3 s a 1,3 s) e dão um "clique" de foco em 2,3 s
    chega = out_back(prog(t, .3, 1.3), 1.2)
    foco = 1 + .07 * math.sin(math.pi * prog(t, 2.25, 2.65))
    dist = (1 - chega) * 260
    for n, (sx, sy) in zip(['bTR', 'bTL', 'bBR', 'bBL'], [(1, -1), (-1, -1), (1, 1), (-1, 1)]):
        op = prog(t, .3, .8)
        g.append(f'<g transform="translate(111 111) scale({foco:.4f}) translate(-111 -111) translate({sx*dist:.2f} {sy*dist:.2f})">'
                 f'<path fill="{PAPER}" fill-opacity="{op:.3f}" d="{P[n]}"/></g>')
    # 2. linha de busca varre o visor (1,0 s a 1,7 s)
    v = prog(t, 1.0, 1.7)
    if 0 < v < 1:
        y = 20 + in_out(v) * 182
        op = math.sin(math.pi * v)
        g.append(f'<rect x="22" y="{y-2:.2f}" width="178" height="4" rx="2" fill="{BLUE}" fill-opacity="{.9*op:.3f}"/>')
        g.append(f'<rect x="22" y="{y-14:.2f}" width="178" height="28" rx="14" fill="{BLUE}" fill-opacity="{.12*op:.3f}"/>')
    # 3. estrela acende girando (1,55 s a 2,35 s) e solta um pulso em anel
    e = prog(t, 1.55, 2.35)
    if e > 0:
        k = out_back(e, 1.8) if e < 1 else 1
        rot = -135 * (1 - out_cubic(e)) + 6 * math.sin(2 * math.pi * prog(t, 4.2, 10))   # depois, um brilho leve
        g.append(f'<g transform="translate(111 111) rotate({rot:.2f}) scale({max(k, .001):.4f}) translate(-111 -111)">'
                 + "".join(f'<path fill="{BLUE}" fill-opacity="{prog(t, 1.55, 1.8):.3f}" d="{P[n]}"/>' for n in ['s1', 's2', 's3', 's4'])
                 + '</g>')
    a = prog(t, 2.05, 3.0)
    if 0 < a < 1:
        r = 30 + out_cubic(a) * 150
        g.append(f'<circle cx="111" cy="111" r="{r:.2f}" fill="none" stroke="{BLUE}" stroke-width="{6*(1-a)+1:.2f}" stroke-opacity="{.55*(1-a):.3f}"/>')
    simbolo = "".join(g)
    # 4. símbolo desliza para a esquerda (2,7 s a 3,4 s) e o nome entra letra a letra
    d = in_out(prog(t, 2.7, 3.4))
    nome = []
    for j, n in enumerate(LETRAS):
        p = out_cubic(prog(t, 3.3 + j * .06, 3.9 + j * .06))
        if p > 0:
            cor = PAPER if j < 4 else BLUE
            nome.append(f'<path transform="translate({(1-p)*-30:.2f} {(1-p)*24:.2f})" fill="{cor}" fill-opacity="{p:.3f}" d="{P[n]}"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<g transform="translate({X0:.2f} {Y0:.2f}) scale({S})">'
           f'<g transform="translate({SHIFT*(1-d):.2f} 0)">{simbolo}</g>{"".join(nome)}</g></svg>')
    pix = pymupdf.open(stream=svg.encode(), filetype='svg')[0].get_pixmap(alpha=True)
    pix.save(os.path.join(OUT, 'quadros', f'{i:04d}.png'))
    return i


def init(out):
    global OUT
    OUT = out


if __name__ == '__main__':
    OUT = os.path.abspath(sys.argv[1])
    os.makedirs(os.path.join(OUT, 'quadros'), exist_ok=True)
    n = int(DUR * FPS)
    with ProcessPoolExecutor(initializer=init, initargs=(OUT,)) as ex:
        for k in ex.map(quadro, range(n), chunksize=8):
            if k % 50 == 0:
                print('quadro', k, flush=True)
    q = os.path.join(OUT, 'quadros', '%04d.png')
    base = ['ffmpeg', '-y', '-v', 'error', '-framerate', str(FPS), '-i', q]
    # MP4 com o fundo grafite da marca (qualquer player, redes sociais)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i', f'color=c=0x1F2124:s={W}x{H}:r={FPS}:d={DUR}',
                    '-framerate', str(FPS), '-i', q, '-filter_complex', '[0][1]overlay=format=auto,format=yuv420p',
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-movflags', '+faststart',
                    os.path.join(OUT, 'FaroFinder-logo-4K.mp4')], check=True)
    # MOV ProRes 4444 com transparência (Premiere, After Effects, DaVinci)
    subprocess.run(base + ['-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', '-vendor', 'apl0',
                           os.path.join(OUT, 'FaroFinder-logo-4K-transparente.mov')], check=True)
    # WebM VP9 com transparência (navegador e a interface do FaroFinder)
    subprocess.run(base + ['-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-b:v', '0', '-crf', '24', '-row-mt', '1',
                           os.path.join(OUT, 'FaroFinder-logo-4K-transparente.webm')], check=True)
    print('pronto')
