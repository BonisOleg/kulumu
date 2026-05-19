/**
 * price_calculator.js — калькулятор ціни доріжок на відріз
 * ширина (radio) × довжина (input) = ціна в реальному часі
 */

export function initPriceCalc() {
  const calc = document.querySelector("#per-meter-calc");
  if (!calc) return;

  const widthInputs = calc.querySelectorAll("[name='width_cm']");
  const lengthInput = calc.querySelector("[name='length_m']");
  const priceDisplay = calc.querySelector("#calc-total-price");
  const addToCartBtn = document.querySelector("#add-to-cart-btn");

  function recalc() {
    const selectedWidth = [...widthInputs].find((i) => i.checked);
    if (!selectedWidth || !lengthInput) return;

    const pricePerM = parseFloat(selectedWidth.dataset.pricePerM || 0);
    const length = parseFloat(lengthInput.value) || 1;
    const total = Math.round(pricePerM * length);

    if (priceDisplay) {
      priceDisplay.textContent = `${total.toLocaleString("uk-UA")} ₴`;
    }

    // Оновлюємо поля форми для кошика
    if (addToCartBtn) {
      addToCartBtn.querySelector("[name='length_m']")?.setAttribute("value", length.toFixed(2));
    }
  }

  widthInputs.forEach((input) => {
    input.addEventListener("change", recalc);
  });

  lengthInput?.addEventListener("input", recalc);

  // Початковий розрахунок
  recalc();
}
