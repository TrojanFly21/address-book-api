from app.utils.haversine import haversine_distance


class GeoService:

    @staticmethod
    def distance_in_km(
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
    ) -> float:
        return haversine_distance(
            lat1,
            lon1,
            lat2,
            lon2,
        )