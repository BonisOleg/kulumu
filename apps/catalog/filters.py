from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CatalogFilter:
    """Нормалізовані параметри фільтра каталогу з query string."""

    facet_slugs: list = field(default_factory=list)
    price_min: Optional[int] = None
    price_max: Optional[int] = None
    sort: str = "default"
    page: int = 1
    per_page: int = 24

    @classmethod
    def from_request(cls, request) -> "CatalogFilter":
        params = request.GET
        facets = params.getlist("f")  # ?f=vysokovorsni&f=dlya-spalni
        price_min = params.get("price_min")
        price_max = params.get("price_max")
        sort = params.get("sort", "default")

        try:
            page = max(1, int(params.get("page", 1) or 1))
        except (ValueError, TypeError):
            page = 1

        try:
            if price_min is not None and str(price_min).strip() != "":
                price_min = int(price_min)
            else:
                price_min = None
        except (ValueError, TypeError):
            price_min = None
        try:
            if price_max is not None and str(price_max).strip() != "":
                price_max = int(price_max)
            else:
                price_max = None
        except (ValueError, TypeError):
            price_max = None

        if price_min is not None and price_min < 0:
            price_min = None
        if price_max is not None and price_max < 0:
            price_max = None
        if price_min is not None and price_max is not None and price_min > price_max:
            price_min, price_max = price_max, price_min

        valid_sorts = {"default", "price_asc", "price_desc", "new", "top"}
        if sort not in valid_sorts:
            sort = "default"

        return cls(
            facet_slugs=facets,
            price_min=price_min,
            price_max=price_max,
            sort=sort,
            page=page,
        )

    def as_query_dict(self):
        """Для формування URL параметрів."""
        params = {}
        if self.facet_slugs:
            params["f"] = self.facet_slugs
        if self.price_min is not None:
            params["price_min"] = self.price_min
        if self.price_max is not None:
            params["price_max"] = self.price_max
        if self.sort != "default":
            params["sort"] = self.sort
        return params
