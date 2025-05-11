from decimal import Decimal

from pydantic_extra_types.currency_code import Currency

from flights_service.models.slice import Slice


class Offer:
    def __init__(
        self,
        *,
        id: str | None = None,
        remote_id: str,
        slices: list[Slice],
        currency: Currency,
        total_amount: Decimal,
    ) -> None:
        self.id = id
        self.remote_id = remote_id
        self.slices = slices
        self.currency = Currency(currency)
        self.total_amount = total_amount
