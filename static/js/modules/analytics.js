/**
 * analytics.js — GA4 purchase event для сторінки успіху
 * Читає data-атрибути з .order-confirmation, якщо вони є на сторінці.
 */

export const initAnalytics = () => {
  const el = document.querySelector(".order-confirmation[data-order-id]");
  if (!el) return;
  if (typeof gtag === "undefined") return;

  gtag("event", "purchase", {
    transaction_id: el.dataset.orderId,
    value: parseFloat(el.dataset.orderValue ?? "0"),
    currency: "UAH",
  });
};
