import math


def calculate_pages(total_items, items_per_page=10):
    return math.ceil(total_items / items_per_page)
