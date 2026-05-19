/**
 * toast.js — обробка mini-cart toast після HTMX swap
 * Toast-елемент рендериться сервером у #toast-container.
 * Читаємо data-cart-count щоб оновити лічильник у header.
 * Авто-приховування через 3с.
 */

const TOAST_SELECTOR = "[data-toast-cart]";
const COUNTER_ID     = "cart-count";
const AUTO_HIDE_MS   = 3000;

const updateCartCounter = (count) => {
  const counter = document.getElementById(COUNTER_ID);
  if (counter) {
    counter.textContent = count;
    return;
  }
  const btn = document.querySelector(".header__cart-btn");
  if (!btn) return;
  const el = document.createElement("span");
  el.className = "header__cart-count";
  el.id = COUNTER_ID;
  el.textContent = count;
  btn.appendChild(el);
};

export const initToast = () => {
  document.body.addEventListener("htmx:afterSwap", (e) => {
    if (e.detail.target?.id !== "toast-container") return;
    const toast = e.detail.target.querySelector(TOAST_SELECTOR);
    if (!toast) return;

    const count = toast.dataset.toastCart;
    if (count !== undefined) updateCartCounter(count);

    setTimeout(() => {
      const container = document.getElementById("toast-container");
      if (container) container.innerHTML = "";
    }, AUTO_HIDE_MS);
  });
};
