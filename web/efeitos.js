// Efeitos visuais inspirados no React Bits (reactbits.dev, licença MIT + Commons Clause):
// AnimatedList, BorderGlow, ClickSpark e CountUp, reescritos em JavaScript puro, porque o app não usa React.
// Só mexem no visual: nenhum comportamento do app muda. Com "reduzir movimento" no sistema, ficam parados.
(() => {
  const reduzido = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---------------------------------------------------------------- BorderGlow
  // Brilho na borda que acompanha o ponteiro quando ele chega perto da beirada.
  function borderGlow(el) {
    if (!el || el.dataset.glow) return;
    el.dataset.glow = "1";
    el.classList.add("bglow");
    const luz = document.createElement("span");
    luz.className = "edge-light";
    luz.setAttribute("aria-hidden", "true");
    el.prepend(luz);
    el.addEventListener("pointermove", (e) => {
      const r = el.getBoundingClientRect();
      const cx = r.width / 2, cy = r.height / 2;
      const dx = e.clientX - r.left - cx, dy = e.clientY - r.top - cy;
      const kx = dx ? cx / Math.abs(dx) : Infinity, ky = dy ? cy / Math.abs(dy) : Infinity;
      const borda = Math.min(Math.max(1 / Math.min(kx, ky), 0), 1);
      let ang = Math.atan2(dy, dx) * 180 / Math.PI + 90;
      if (ang < 0) ang += 360;
      el.style.setProperty("--edge-proximity", (borda * 100).toFixed(2));
      el.style.setProperty("--cursor-angle", `${ang.toFixed(2)}deg`);
    });
  }

  // ---------------------------------------------------------------- AnimatedList
  // Itens entram em cascata ("pop") e um destaque desliza com mola até o item sob o ponteiro.
  function listaAnimada(box, seletor) {
    if (!box || box.dataset.al) return;
    box.dataset.al = "1";
    box.classList.add("al-box");
    const ind = document.createElement("span");
    ind.className = "al-ind";
    ind.setAttribute("aria-hidden", "true");
    box.append(ind);

    const m = { y: 0, h: 0, vy: 0, vh: 0, ty: 0, th: 0, pronto: false };
    let raf = 0, t0 = 0;
    const escreve = () => {
      ind.style.transform = `translate3d(0, ${m.y.toFixed(2)}px, 0)`;
      ind.style.height = `${m.h.toFixed(2)}px`;
    };
    const quadro = (agora) => {   // mola amortecida (a mesma física do AnimatedList)
      raf = 0;
      const dt = Math.min(0.05, (agora - t0) / 1000 || 0);
      t0 = agora;
      const w = 30, z = 0.78, n = Math.max(1, Math.ceil(dt * 240)), h = dt / n;
      for (let i = 0; i < n; i++) {
        m.vy += (w * w * (m.ty - m.y) - 2 * z * w * m.vy) * h;
        m.vh += (w * w * (m.th - m.h) - 2 * z * w * m.vh) * h;
        m.y += m.vy * h;
        m.h += m.vh * h;
      }
      const movendo = Math.abs(m.ty - m.y) > 0.05 || Math.abs(m.th - m.h) > 0.05 || Math.abs(m.vy) + Math.abs(m.vh) > 0.5;
      if (!movendo) { m.y = m.ty; m.h = m.th; m.vy = m.vh = 0; }
      escreve();
      if (movendo) raf = requestAnimationFrame(quadro);
    };
    const vai = (item) => {
      if (!item || !item.offsetParent) { ind.style.opacity = "0"; m.pronto = false; return; }
      const br = box.getBoundingClientRect(), ir = item.getBoundingClientRect();
      m.ty = ir.top - br.top + box.scrollTop;
      m.th = ir.height;
      ind.style.left = `${ir.left - br.left}px`;
      ind.style.width = `${ir.width}px`;
      ind.style.opacity = "1";
      if (reduzido || !m.pronto) { m.y = m.ty; m.h = m.th; m.vy = m.vh = 0; m.pronto = true; escreve(); return; }
      if (!raf) { t0 = performance.now(); raf = requestAnimationFrame(quadro); }
    };
    const marcados = () => box.querySelector(`${seletor}.on`);
    const entra = (itens) => itens.forEach((it, i) => {
      it.classList.add("al-item");
      if (reduzido) return;
      it.style.setProperty("--al-i", Math.min(i, 12));
      it.classList.remove("al-in");
      void it.offsetWidth;
      it.classList.add("al-in");
    });

    box.addEventListener("pointerover", (e) => {
      const it = e.target.closest(seletor);
      if (it && box.contains(it)) vai(it);
    });
    box.addEventListener("pointerleave", () => vai(marcados()));
    new MutationObserver((muts) => {
      if (!box.contains(ind)) box.append(ind);   // o app reescreve a lista com innerHTML e leva o destaque junto
      const novos = [];
      for (const mu of muts) for (const n of mu.addedNodes) {
        if (n.nodeType !== 1 || n === ind) continue;
        if (n.matches(seletor)) novos.push(n);
        novos.push(...n.querySelectorAll(seletor));
      }
      if (novos.length) { entra(novos); requestAnimationFrame(() => vai(marcados())); }
    }).observe(box, { childList: true, subtree: true });
    entra([...box.querySelectorAll(seletor)]);
    requestAnimationFrame(() => vai(marcados()));
  }

  // ---------------------------------------------------------------- ClickSpark
  // Faíscas curtas saindo do ponto do clique nos botões (fora da grade de fotos, que é usada o tempo todo).
  document.addEventListener("pointerdown", (e) => {
    if (reduzido || e.button !== 0) return;
    const b = e.target.closest("button, .btn");
    if (!b || b.disabled || b.closest(".tile, .tl-bar, .seg, .chip, .cloud, .bottomnav, .speech, .vol")) return;
    const f = document.createElement("span");
    f.className = "spark";
    f.style.left = `${e.clientX}px`;
    f.style.top = `${e.clientY}px`;
    for (let i = 0; i < 8; i++) {
      const r = document.createElement("i");
      r.style.setProperty("--a", `${i * 45}deg`);
      f.append(r);
    }
    document.body.append(f);
    setTimeout(() => f.remove(), 450);
  });

  // ---------------------------------------------------------------- CountUp
  // O total de resultados conta do número anterior até o novo.
  const total = document.getElementById("count");
  let anterior = 0, rodada = 0, escrevendo = false;
  if (total) new MutationObserver(() => {
    if (escrevendo) return;
    const t = total.textContent, achado = t.match(/^([\d.]+)(\D.*)$/);
    if (!achado) return;
    const alvo = Number(achado[1].replace(/\./g, "")), de = anterior, resto = achado[2], id = ++rodada;
    anterior = alvo;
    if (reduzido || !de || de === alvo) return;
    const inicio = performance.now(), dur = 300;
    const tique = (agora) => {
      if (id !== rodada) return;
      const p = Math.min(1, (agora - inicio) / dur), e = 1 - Math.pow(1 - p, 3);
      escrevendo = true;
      total.textContent = Math.round(de + (alvo - de) * e).toLocaleString("pt-BR") + resto;
      escrevendo = false;
      if (p < 1) requestAnimationFrame(tique);
    };
    requestAnimationFrame(tique);
  }).observe(total, { childList: true, characterData: true, subtree: true });

  // ---------------------------------------------------------------- onde cada efeito entra
  ["#searchForm", ".timeline", ".mapbox", ".collhead", ".selbar", ".sharebox"].forEach((s) => borderGlow(document.querySelector(s)));
  listaAnimada(document.querySelector(".side .marks"), ".vol");
  listaAnimada(document.getElementById("volumes"), ".vol");
})();
