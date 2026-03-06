from typing import List, Dict

def search_flights(departure: str, destination: str) -> List[Dict]:
    """
    Return mock flight options between two cities.
    """
    return [
        {"airline": "Air France", "price": 120},
        {"airline": "Ryanair", "price": 70},
        {"airline": "ITA Airways", "price": 110}
    ]


def search_hotels(destination: str) -> List[Dict]:
    """
    Return mock hotel options.
    """
    return [
        {"hotel": "Hotel Roma", "price": 90},
        {"hotel": "City Hostel", "price": 45},
        {"hotel": "Luxury Suites", "price": 180}
    ]


def search_restaurants(destination: str) -> List[Dict]:
    """
    Return mock restaurant options.
    """
    return [
       {"restaurant": "Trattoria Roma", "avg_price": 25},
        {"restaurant": "Street Pizza", "avg_price": 10},
        {"restaurant": "La Pasta House", "avg_price": 18},
        {"restaurant": "Roma Bistro", "avg_price": 22},
        {"restaurant": "Vino & Pasta", "avg_price": 30},
        {"restaurant": "Local Market Eatery", "avg_price": 12},
        {"restaurant": "Tiber Riverside Cafe", "avg_price": 16}
    ]


def search_activities(destination: str) -> List[Dict]:
    """
    Return mock activities.
    """
    return [
        {"activity": "Colosseum", "price": 20},
        {"activity": "Vatican Museum", "price": 25}
    ]