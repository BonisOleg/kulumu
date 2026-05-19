/**
 * main.js — точка входу. Ініціалізація всіх JS-модулів.
 * Без бандлера (нативні ES modules з <script type="module">)
 */

import { initSafariFix }   from "./modules/safari_fix.js";
import { initDrawer }       from "./modules/drawer.js";
import { initFilterChips }  from "./modules/filter_chips.js";
import { initVariantSwatch }from "./modules/variant_swatch.js";
import { initPriceCalc }    from "./modules/price_calculator.js";
import { initLazy }         from "./modules/lazy_images.js";
import { initLeadForms }    from "./modules/lead_form.js";
import { initTabs }         from "./modules/tabs.js";
import { initNpSelect }     from "./modules/np_select.js";
import { initToast }        from "./modules/toast.js";
import { initAnalytics }    from "./modules/analytics.js";

const getCookie = (name) => {
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : null;
};

document.body.addEventListener("htmx:configRequest", (evt) => {
  evt.detail.headers["X-CSRFToken"] = getCookie("csrftoken") ?? "";
});

document.addEventListener("DOMContentLoaded", () => {
  initSafariFix();   // обов'язково першим
  initDrawer();
  initFilterChips();
  initVariantSwatch();
  initPriceCalc();
  initLazy();
  initLeadForms();
  initTabs();
  initNpSelect();
  initToast();
  initAnalytics();
});
