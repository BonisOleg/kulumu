/**
 * drawer.js — мобільне меню-drawer
 * Блокує scroll body при відкритті (iOS-safe)
 */

export function initDrawer() {
  const overlay = document.querySelector(".drawer-overlay");
  const drawer = document.querySelector(".drawer");
  const openBtns = document.querySelectorAll("[data-drawer-open]");
  const closeBtns = document.querySelectorAll("[data-drawer-close]");

  if (!drawer) return;

  function open() {
    overlay?.classList.add("open");
    drawer.classList.add("open");
    document.body.classList.add("drawer-open");
    drawer.querySelector("a, button")?.focus();
  }

  function close() {
    overlay?.classList.remove("open");
    drawer.classList.remove("open");
    document.body.classList.remove("drawer-open");
  }

  openBtns.forEach((btn) => btn.addEventListener("click", open));
  closeBtns.forEach((btn) => btn.addEventListener("click", close));
  overlay?.addEventListener("click", close);

  // Закрити по Escape
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && drawer.classList.contains("open")) {
      close();
    }
  });
}
