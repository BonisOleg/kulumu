/**
 * np_select.js — вибір міста/складу Nova Poshta з dropdown
 * Кнопки: data-np-city-name / data-np-city-ref
 *         data-np-warehouse-address / data-np-warehouse-ref
 */

export const initNpSelect = () => {
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-np-city-name]");
    if (btn) {
      const nameInput = document.querySelector("[name='np_city_name']");
      const refInput  = document.querySelector("[name='np_city_ref']");
      if (nameInput) nameInput.value = btn.dataset.npCityName;
      if (refInput)  refInput.value  = btn.dataset.npCityRef ?? "";
      btn.closest(".np-dropdown")?.remove();
      return;
    }

    const warehouseBtn = e.target.closest("[data-np-warehouse-address]");
    if (warehouseBtn) {
      const addrInput = document.querySelector("[name='np_warehouse_address']");
      const refInput  = document.querySelector("[name='np_warehouse_ref']");
      if (addrInput) addrInput.value = warehouseBtn.dataset.npWarehouseAddress;
      if (refInput)  refInput.value  = warehouseBtn.dataset.npWarehouseRef ?? "";
      warehouseBtn.closest(".np-dropdown")?.remove();
    }
  });
};
