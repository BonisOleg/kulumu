/**
 * variant_swatch.js — перемикач кольорів/розмірів на картці серії
 * Клік → HTMX GET → перерендер блоку ціни/фото
 */

const applySwatchColors = (root = document) => {
  root.querySelectorAll("[data-color-id][data-color]").forEach((el) => {
    el.style.background = el.dataset.color;
  });
};

export function initVariantSwatch() {
  applySwatchColors();

  document.body.addEventListener("htmx:afterSwap", (e) => {
    applySwatchColors(e.detail?.target ?? document);
  });

  // Swatches кольорів
  document.addEventListener("click", (e) => {
    const swatch = e.target.closest("[data-color-id]");
    if (!swatch) return;

    document.querySelectorAll("[data-color-id]").forEach((el) => {
      el.classList.remove("active");
      el.setAttribute("aria-pressed", "false");
    });
    swatch.classList.add("active");
    swatch.setAttribute("aria-pressed", "true");

    updateVariantParam("color", swatch.dataset.colorId);
  });

  // Перемикач розмірів
  document.addEventListener("click", (e) => {
    const sizeBtn = e.target.closest("[data-size-variant-id]");
    if (!sizeBtn) return;

    document.querySelectorAll("[data-size-variant-id]").forEach((el) => {
      el.classList.remove("active", "btn-primary");
      el.setAttribute("aria-pressed", "false");
    });
    sizeBtn.classList.add("active", "btn-primary");
    sizeBtn.setAttribute("aria-pressed", "true");

    updateVariantParam("variant", sizeBtn.dataset.sizeVariantId);
  });
}

function updateVariantParam(key, value) {
  const variantBlock = document.querySelector("#variant-block");
  if (!variantBlock) return;

  const url = variantBlock.dataset.htmxUrl;
  if (!url) return;

  const urlObj = new URL(url, window.location.origin);
  urlObj.searchParams.set(key, value);
  const finalUrl = urlObj.pathname + urlObj.search;
  variantBlock.setAttribute("hx-get", finalUrl);

  if (typeof htmx === "undefined") return;

  // htmx.ajax надійніший за trigger після зміни URL (див. htmx.org/api/#ajax)
  htmx.ajax("GET", finalUrl, {
    source: variantBlock,
    target: variantBlock,
    swap: "outerHTML",
  });
}

/** Після підвантаження блоку варіанту — оновити текст мобільної CTA (ціна). */
function syncStickyCartLabelFromVariantBlock(variantBlock) {
  if (!variantBlock || variantBlock.id !== "variant-block") return;
  const label = variantBlock.getAttribute("data-cta-price-label");
  const cta = document.getElementById("cta-bar-add-label");
  if (label && cta) {
    cta.textContent = label;
  }
}

document.body.addEventListener("htmx:afterSwap", (e) => {
  syncStickyCartLabelFromVariantBlock(e.detail?.target);
});
