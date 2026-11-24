from dataclasses import dataclass


@dataclass
class PlaneCreate:
    registration: str
    model: str
    airline: str


@dataclass
class Plane:
    id: int
    registration: str
    model: str
    airline: str
