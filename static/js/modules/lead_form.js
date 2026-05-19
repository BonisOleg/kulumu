/**
 * lead_form.js — модалка "Замовити дзвінок"
 * Використовує event delegation — коректно працює після HTMX outerHTML swap.
 */

export function initLeadForms() {
  function getModal() {
    return document.querySelector("#callback-modal");
  }

  function openModal() {
    const modal = getModal();
    if (!modal) return;
    modal.style.display = "flex";
    document.body.classList.add("modal-open");

    const pageUrlInput = modal.querySelector("[name='page_url']");
    if (pageUrlInput) pageUrlInput.value = window.location.href;

    modal.querySelector("input:not([type='hidden'])")?.focus();
  }

  function closeModal() {
    const modal = getModal();
    if (!modal) return;
    modal.style.display = "none";
    document.body.classList.remove("modal-open");
  }

  // Event delegation — спрацьовує навіть після HTMX outerHTML swap
  document.addEventListener("click", (e) => {
    if (e.target.closest("[data-modal='callback']")) {
      openModal();
      return;
    }
    if (e.target.closest("[data-modal-close]")) {
      closeModal();
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      const modal = getModal();
      if (modal && modal.style.display !== "none") closeModal();
    }
  });
}
