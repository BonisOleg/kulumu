"""Інтеграція з API Нової Пошти."""
import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

NP_API_URL = "https://api.novaposhta.ua/v2.0/json/"


def _np_request(model: str, method: str, props: dict = None) -> list:
    payload = {
        "apiKey": settings.NOVA_POSHTA_API_KEY,
        "modelName": model,
        "calledMethod": method,
        "methodProperties": props or {},
    }
    try:
        response = requests.post(NP_API_URL, json=payload, timeout=10)
        data = response.json()
        if data.get("success"):
            return data.get("data", [])
    except Exception as exc:
        logger.warning("Nova Poshta API error: %s", exc)
    return []


def search_cities(query: str) -> list:
    results = _np_request(
        "Address", "getCities",
        {"FindByString": query, "Limit": 10}
    )
    return [
        {"ref": r["Ref"], "name": r["Description"]}
        for r in results
    ]


def search_warehouses(city_ref: str, query: str = "") -> list:
    props = {"CityRef": city_ref, "Limit": 20}
    if query:
        props["FindByString"] = query
    results = _np_request("AddressGeneral", "getWarehouses", props)
    return [
        {"ref": r["Ref"], "address": r["Description"]}
        for r in results
    ]
