import uuid
from datetime import timedelta, datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

from pydantic_extra_types.currency_code import Currency

from flights_service.adapters.abc import SearchAdapter, UpstreamSession
from flights_service.models.offer import Offer
from flights_service.models.segment import Segment
from flights_service.models.slice import Slice
from flights_service.repositories.airline.abc import AirlineRepository


class TestUpstreamSession(UpstreamSession):
    def __init__(self, offers: list[Offer]) -> None:
        self.offers = offers
        self.call_count = 0

    def get_offers(self) -> list[Offer]:
        if self.call_count == 0:
            self.call_count += 1
            return self.offers
        return []


class TestSearchAdapter(SearchAdapter):
    def __init__(self, airline_repo: AirlineRepository) -> None:
        self.airline_repo = airline_repo

    def create_session(self) -> UpstreamSession:
        # Generate a few common airport pairs
        city_pairs = [
            # Origin, Destination
            ("JFK", "LHR"),  # New York to London
            ("LAX", "NRT"),  # Los Angeles to Tokyo
            ("SFO", "HKG"),  # San Francisco to Hong Kong
            ("ORD", "CDG"),  # Chicago to Paris
            ("MIA", "MAD"),  # Miami to Madrid
        ]

        # Create fake offers
        offers = []

        utc = ZoneInfo("UTC")
        now = datetime.now(utc)

        for i, (_origin, _destination) in enumerate(city_pairs):
            # Generate different airline combinations for variety
            if i == 0:
                airline_codes = ["AA", "BA"]  # American, British Airways
            elif i == 1:
                airline_codes = ["UA", "NH"]  # United, ANA
            elif i == 2:
                airline_codes = ["UA", "CX"]  # United, Cathay Pacific
            elif i == 3:
                airline_codes = ["AA", "AF"]  # American, Air France
            else:
                airline_codes = ["AA", "IB"]  # American, Iberia

            marketing_airline = self.airline_repo.get_airline_by_iata_code(
                airline_codes[0]
            )
            operating_airline = self.airline_repo.get_airline_by_iata_code(
                airline_codes[1]
            )

            # Create outbound segment
            outbound_departure = now + timedelta(days=30, hours=i * 3)
            outbound_arrival = outbound_departure + timedelta(hours=8 + i)

            outbound_segment = Segment(
                marketing_airline=marketing_airline,
                operating_airline=operating_airline,
                flight_number=f"{marketing_airline.iata_code}123",
                departure_time=outbound_departure,
                arrival_time=outbound_arrival,
            )

            # Create return segment
            return_departure = outbound_arrival + timedelta(days=7)
            return_arrival = return_departure + timedelta(hours=9 + i)

            return_segment = Segment(
                marketing_airline=marketing_airline,
                operating_airline=operating_airline,
                flight_number=f"{marketing_airline.iata_code}456",
                departure_time=return_departure,
                arrival_time=return_arrival,
            )

            # Create outbound and return slices
            outbound_slice = Slice(
                segments=[outbound_segment],
                fare_brand_name=f"Economy {'Basic' if i % 2 == 0 else 'Flex'}",
            )

            return_slice = Slice(
                segments=[return_segment],
                fare_brand_name=f"Economy {'Basic' if i % 2 == 0 else 'Flex'}",
            )

            # Create offer with both slices
            offer = Offer(
                remote_id=f"TEST-{uuid.uuid4()}",
                slices=[outbound_slice, return_slice],
                currency=Currency("USD"),
                total_amount=Decimal(f"{500 + (i * 100):.2f}"),
            )

            offers.append(offer)

        return TestUpstreamSession(offers)
