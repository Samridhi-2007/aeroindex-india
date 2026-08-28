from dataclasses import dataclass, field


@dataclass(frozen=True)
class WeightMetadata:
    source: str
    status: str
    reference: str = ""


@dataclass(frozen=True)
class Observation:
    observation_id: str
    period: str
    route: str
    origin: str
    destination: str
    booking_window_days: int
    total_consumer_fare: float | None
    source_id: str
    carrier: str | None
    fare_class: str | None
    observation_date: str
    is_duplicate: bool
    raw_fare: str | None = None
    collection_timestamp: str | None = None
    extraction_status: str = "normalized"
    stops: int | None = None
    source_url: str | None = None


@dataclass(frozen=True)
class RawFareObservation:
    observation_id: str
    period: str
    route: str
    origin: str
    destination: str
    booking_window_days: int
    raw_fare: str | None
    source_id: str
    carrier: str | None
    fare_class: str | None
    observation_date: str
    collection_timestamp: str
    extraction_status: str = "extracted"
    stops: int | None = None
    source_url: str | None = None


@dataclass(frozen=True)
class Weights:
    route_weights: dict[str, float] = field(default_factory=dict)
    window_weights: dict[int, float] = field(default_factory=dict)
    airfare_weight: float | None = None
    route_weight_metadata: dict[str, WeightMetadata] = field(default_factory=dict)
    window_weight_metadata: dict[int, WeightMetadata] = field(default_factory=dict)
    airfare_weight_metadata: WeightMetadata | None = None