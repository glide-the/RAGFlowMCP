from enum import Enum


class QueryRequestMode(str, Enum):
    GLOBAL = "global"
    HYBRID = "hybrid"
    LOCAL = "local"
    MIX = "mix"
    NAIVE = "naive"

    def __str__(self) -> str:
        return str(self.value)
