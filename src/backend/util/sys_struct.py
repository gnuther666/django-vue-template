from dataclasses import dataclass


@dataclass
class BoolMsgResult:
    is_success: bool
    msg: str