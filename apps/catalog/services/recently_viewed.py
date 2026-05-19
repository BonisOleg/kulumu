RECENTLY_VIEWED_KEY = "recently_viewed"
MAX_ITEMS = 10


def add_to_recently_viewed(request, series_pk: int):
    """Додає ID серії до cookie-списку нещодавно переглянутих."""
    viewed = request.session.get(RECENTLY_VIEWED_KEY, [])
    pk = int(series_pk)
    if pk in viewed:
        viewed.remove(pk)
    viewed.insert(0, pk)
    request.session[RECENTLY_VIEWED_KEY] = viewed[:MAX_ITEMS]


def get_recently_viewed(request, exclude_pk=None):
    """Повертає список ID нещодавно переглянутих (без поточного)."""
    viewed = request.session.get(RECENTLY_VIEWED_KEY, [])
    if exclude_pk:
        viewed = [pk for pk in viewed if pk != int(exclude_pk)]
    return viewed[:MAX_ITEMS]
