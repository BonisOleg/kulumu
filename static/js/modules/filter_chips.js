/**
 * filter_chips.js — Active filter chips з видаленням
 * Після видалення — тригер HTMX submit форми фільтра
 */

export function initFilterChips() {
  document.addEventListener("click", (e) => {
    const chip = e.target.closest("[data-remove-filter]");
    if (!chip) return;

    const filterName = chip.dataset.removeFilter;
    const filterValue = chip.dataset.removeValue;
    const form = document.querySelector("#filter-form");

    if (!form) return;

    // Знімаємо відповідний checkbox або очищаємо number-поле
    const inputs = form.querySelectorAll(`[name="${filterName}"]`);
    inputs.forEach((input) => {
      if (input.value === filterValue || !filterValue) {
        input.checked = false;
        if (input.type === "text" || input.type === "number") {
          input.value = "";
        }
      }
    });

    // Тригеримо HTMX через submit — найнадійніший спосіб
    if (typeof htmx !== "undefined") {
      htmx.trigger(form, "submit");
    } else {
      const fallback = form.querySelector("input[type='checkbox']:checked") || form.querySelector("input");
      if (fallback) {
        fallback.dispatchEvent(new Event("change", { bubbles: true }));
      }
    }
  });
}
