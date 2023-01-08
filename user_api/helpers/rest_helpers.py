from typing import Any, Dict, NamedTuple


class ApiResponse(NamedTuple):
    ok: bool
    description: str
    result: Any | None = None

    def to_dict(self) -> Dict:
        return {
            "ok": self.ok,
            "message": self.description,
            "result": self.result,
        }
