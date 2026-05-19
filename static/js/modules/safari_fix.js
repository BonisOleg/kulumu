/**
 * safari_fix.js — iOS Safari quirks:
 * - 100dvh фолбек
 * - Blur при scroll (address bar)
 * - Safe-area оновлення при rotate
 */

export function initSafariFix() {
  const root = document.documentElement;

  // --vh оновлюємо при resize/orientation (фолбек для старих iOS що не знають 100dvh)
  function updateVh() {
    root.style.setProperty("--vh", `${window.innerHeight}px`);
  }

  updateVh();
  window.addEventListener("resize", updateVh, { passive: true });
  window.addEventListener("orientationchange", () => {
    // Невелика затримка бо iOS оновлює window.innerHeight з запізненням
    setTimeout(updateVh, 200);
  }, { passive: true });

  root.classList.add("ios-ready");
}
