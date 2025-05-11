from datetime import datetime
from decimal import Decimal
from typing import Iterable

from pydantic import BaseModel, Field, AliasPath
from pydantic_extra_types.currency_code import Currency

from flights_service.models.offer import Offer
from flights_service.models.segment import Segment
from flights_service.models.slice import Slice
from flights_service.repositories.airline.abc import AirlineRepository


class SegmentSchema(BaseModel):
    marketing_airline_iata_code: str = Field(
        validation_alias=AliasPath("marketing_airline", "iata_code")
    )
    operating_airline_iata_code: str = Field(
        validation_alias=AliasPath("operating_airline", "iata_code")
    )
    flight_number: str
    departure_time: datetime
    arrival_time: datetime

    @property
    def airline_iata_codes(self) -> Iterable[str]:
        yield self.marketing_airline_iata_code
        yield self.operating_airline_iata_code

    def to_domain(self, airline_repo: AirlineRepository) -> Segment:
        return Segment(
            marketing_airline=airline_repo.get_airline_by_iata_code(
                self.marketing_airline_iata_code
            ),
            operating_airline=airline_repo.get_airline_by_iata_code(
                self.operating_airline_iata_code
            ),
            flight_number=self.flight_number,
            departure_time=self.departure_time,
            arrival_time=self.arrival_time,
        )


class SliceSchema(BaseModel):
    segments: list[SegmentSchema]
    fare_brand_name: str

    @property
    def airline_iata_codes(self) -> Iterable[str]:
        for segment in self.segments:
            yield from segment.airline_iata_codes

    def to_domain(self, airline_repo: AirlineRepository) -> Slice:
        return Slice(
            segments=[seg.to_domain(airline_repo) for seg in self.segments],
            fare_brand_name=self.fare_brand_name,
        )


class OfferSchema(BaseModel):
    id: str
    remote_id: str
    slices: list[SliceSchema]
    currency: Currency
    total_amount: Decimal

    @property
    def airline_iata_codes(self) -> Iterable[str]:
        for slice in self.slices:
            yield from slice.airline_iata_codes

    def to_domain(self, airline_repo: AirlineRepository) -> Offer:
        return Offer(
            id=self.id,
            remote_id=self.remote_id,
            slices=[slice.to_domain(airline_repo) for slice in self.slices],
            currency=self.currency,
            total_amount=self.total_amount,
        )

    @classmethod
    def from_domain(cls, offer: Offer) -> "OfferSchema":
        return cls.model_validate(offer, from_attributes=True)
