from sqlalchemy import Table, Column, Text, DateTime, Integer, ForeignKey, Numeric
from sqlalchemy.orm import registry, relationship

from flights_service.models.airline import Airline
from flights_service.models.airport import Airport
from flights_service.models.quote import Quote
from flights_service.models.segment import Segment
from flights_service.models.slice import Slice

mapper_registry = registry()

airline_table = Table(
    "airline",
    mapper_registry.metadata,
    Column("iata_code", Text, primary_key=True),
    Column("name", Text, nullable=False),
)

airport_table = Table(
    "airport",
    mapper_registry.metadata,
    Column("iata_code", Text, primary_key=True),
    Column("name", Text, nullable=False),
)

segment_table = Table(
    "segment",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("slice_id", Integer, ForeignKey("slice.id"), nullable=False),
    Column("flight_number", Text, nullable=False),
    Column("departure_time", DateTime(timezone=True), nullable=False),
    Column("arrival_time", DateTime(timezone=True), nullable=False),
    Column(
        "marketing_airline_iata_code",
        Text,
        ForeignKey("airline.iata_code"),
        nullable=False,
    ),
    Column(
        "operating_airline_iata_code",
        Text,
        ForeignKey("airline.iata_code"),
        nullable=False,
    ),
)

slice_table = Table(
    "slice",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("fare_brand_name", Text, nullable=False),
    Column("departure_time", DateTime(timezone=True), nullable=False),
)

quote_table = Table(
    "quote",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("remote_id", Text, nullable=False),
    Column("currency", Text, nullable=False),
    Column("total_amount", Numeric, nullable=False),
)

slice_quote_association = Table(
    "slice_quote_association",
    mapper_registry.metadata,
    Column("slice_id", Integer, ForeignKey("slice.id"), primary_key=True),
    Column("quote_id", Integer, ForeignKey("quote.id"), primary_key=True),
)


mapper_registry.map_imperatively(Airline, airline_table)
mapper_registry.map_imperatively(Airport, airport_table)
mapper_registry.map_imperatively(
    Segment,
    segment_table,
    properties={
        "marketing_airline": relationship(
            Airline, foreign_keys=segment_table.c.marketing_airline_iata_code
        ),
        "operating_airline": relationship(
            Airline, foreign_keys=segment_table.c.operating_airline_iata_code
        ),
    },
)
mapper_registry.map_imperatively(
    Slice,
    slice_table,
    properties={
        "segments": relationship(Segment, order_by=segment_table.c.departure_time),
    },
)
mapper_registry.map_imperatively(
    Quote,
    quote_table,
    properties={
        "slices": relationship(
            Slice,
            secondary=slice_quote_association,
            order_by=slice_table.c.departure_time,
        ),
    },
)
