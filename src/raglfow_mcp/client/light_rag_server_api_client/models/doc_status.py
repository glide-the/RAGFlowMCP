from enum import Enum


class DocStatus(str, Enum):
    FAILED = "failed"
    PENDING = "pending"
    PROCESSED = "processed"
    PROCESSING = "processing"

    def __str__(self) -> str:
        return str(self.value)
