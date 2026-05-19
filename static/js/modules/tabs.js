/**
 * tabs.js — tab switcher для [role="tablist"] з data-tab атрибутами
 * Використання: <button data-tab="id" role="tab">
 *               <div id="tab-{id}" role="tabpanel">
 */

export const initTabs = () => {
  document.querySelectorAll("[role='tablist']").forEach((tablist) => {
    tablist.addEventListener("click", (e) => {
      const btn = e.target.closest("[role='tab'][data-tab]");
      if (!btn) return;

      const targetId = btn.dataset.tab;
      const root = tablist.closest("[data-tabs-root]") ?? document;

      root.querySelectorAll("[role='tabpanel']").forEach((panel) => {
        panel.setAttribute("aria-selected", "false");
      });
      root.querySelectorAll("[role='tab']").forEach((tab) => {
        tab.setAttribute("aria-selected", "false");
      });

      const panel = root.querySelector(`#tab-${targetId}`);
      if (panel) panel.setAttribute("aria-selected", "true");
      btn.setAttribute("aria-selected", "true");
    });
  });
};
