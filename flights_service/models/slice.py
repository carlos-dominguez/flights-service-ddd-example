from flights_service.models.segment import Segment


class Slice:
    def __init__(self, segments: list[Segment], fare_brand_name: str):
        self.segments = segments
        self.fare_brand_name = fare_brand_name
        self.departure_time = min(segment.departure_time for segment in segments)
