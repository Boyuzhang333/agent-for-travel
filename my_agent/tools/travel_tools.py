from typing import List, Dict

def search_flights(departure: str, destination: str) -> List[Dict]:
    """
    Return mock flight options between two cities.
    """
    try:
        return [
            {"airline": "Air France", "price": 120},
            {"airline": "Ryanair", "price": 70},
            {"airline": "ITA Airways", "price": 110}
        ]
    except Exception as e:
        return [{"error": str(e)}]


def search_hotels(destination: str) -> List[Dict]:
    """
    Return mock hotel options.
    """
    try:
        return [
            {"hotel": "Hotel Roma", "price": 90},
            {"hotel": "City Hostel", "price": 45},
            {"hotel": "Luxury Suites", "price": 180}
        ]
    except Exception as e:
        return [{"error": str(e)}]


def search_restaurants(destination: str) -> List[Dict]:
    """
    Return mock restaurants.
    """
    try:
        return [
            {"restaurant": "Trattoria Roma", "avg_price": 25},
            {"restaurant": "Street Pizza", "avg_price": 10}
        ]
    except Exception as e:
        return [{"error": str(e)}]


def search_activities(destination: str) -> List[Dict]:
    """
    Return mock activities.
    """
    try:
        return [
            {"activity": "Colosseum", "price": 20},
            {"activity": "Vatican Museum", "price": 25}
        ]
    except Exception as e:
        return [{"error": str(e)}]