from sqlalchemy.orm import Session

from flights_service.models.airline import Airline
from flights_service.repositories.airline.abc import AirlineRepository


class SQLAlchemyAirlineRepository(AirlineRepository):
    def __init__(self, session: Session) -> None:
        self._session = session
        self._initialite_airlines()

    def get_airline_by_iata_code(self, iata_code: str) -> Airline:
        return self._session.get_one(Airline, iata_code)  # type:ignore

    def _initialite_airlines(self):
        airlines = [
            Airline("AA", "American Airlines"),
            Airline("UA", "United Airlines"),
            Airline("DL", "Delta Air Lines"),
            Airline("WN", "Southwest Airlines"),
            Airline("AC", "Air Canada"),
            Airline("WS", "WestJet"),
            Airline("BA", "British Airways"),
            Airline("LH", "Lufthansa"),
            Airline("AF", "Air France"),
            Airline("KL", "KLM Royal Dutch Airlines"),
            Airline("IB", "Iberia"),
            Airline("AZ", "Alitalia"),
            Airline("SN", "Brussels Airlines"),
            Airline("CX", "Cathay Pacific"),
            Airline("SQ", "Singapore Airlines"),
            Airline("JL", "Japan Airlines"),
            Airline("NH", "All Nippon Airways"),
            Airline("KE", "Korean Air"),
            Airline("CZ", "China Southern Airlines"),
            Airline("MU", "China Eastern Airlines"),
            Airline("EK", "Emirates"),
            Airline("QR", "Qatar Airways"),
            Airline("EY", "Etihad Airways"),
        ]
        for airline in airlines:
            self._session.merge(airline)
        self._session.flush()
