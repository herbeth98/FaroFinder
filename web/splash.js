// Tela de abertura do FaroFinder: a logo se monta (cantos fecham o foco, a estrela acende, o nome entra)
// e a tela sai quando a página terminou de carregar. Com "reduzir movimento", aparece parada e sai logo.
(() => {
  const el = document.getElementById("splash");
  if (!el) return;
  const reduzido = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const minimo = reduzido ? 300 : 1900;   // tempo para a animação terminar
  const t0 = performance.now();
  let saindo = false;
  const sai = () => {
    if (saindo) return;
    saindo = true;
    const falta = Math.max(0, minimo - (performance.now() - t0));
    setTimeout(() => {
      el.classList.add("sp-out");
      setTimeout(() => el.remove(), 450);
    }, falta);
  };
  if (document.readyState === "complete") sai();
  else addEventListener("load", sai, { once: true });
  setTimeout(sai, 8000);   // nunca prende a tela, mesmo se algum recurso demorar
})();
