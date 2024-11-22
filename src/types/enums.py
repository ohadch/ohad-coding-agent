import enum


class FeatureRequestState(enum.Enum):
    BACKLOG = "BACKLOG"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    ERROR = "ERROR"
