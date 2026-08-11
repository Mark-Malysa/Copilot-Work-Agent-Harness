from __future__ import annotations

import json
import re
from dataclasses import dataclass

from pydantic import ValidationError

from cwah.protocol.models import Response

START, END = "CWAH_RESPONSE_V1_START", "CWAH_RESPONSE_V1_END"


class ProtocolError(ValueError):
    pass


@dataclass
class ParsedResponse:
    control: Response
    payloads: dict[str, str]


def parse_response(text: str) -> ParsedResponse:
    start, end = text.find(START), text.rfind(END)
    if start < 0 or end < 0 or end <= start:
        raise ProtocolError("Missing or invalid response markers")
    body = text[start + len(START) : end]
    payloads: dict[str, str] = {}
    pattern = re.compile(r"CWAH_PAYLOAD_START\s+([^\s]+)\s*\n(.*?)\nCWAH_PAYLOAD_END\s+\1", re.S)
    for match in pattern.finditer(body):
        pid = match.group(1)
        if pid in payloads:
            raise ProtocolError(f"Duplicate payload: {pid}")
        payloads[pid] = match.group(2)
    control_area = pattern.sub("", body).strip()
    control_area = re.sub(r"^```(?:json)?\s*|\s*```$", "", control_area, flags=re.I | re.S).strip()
    try:
        obj = json.loads(control_area)
        control = Response.model_validate(obj)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise ProtocolError(str(exc)) from exc
    missing = [
        a.payload_id for a in control.actions if a.payload_id and a.payload_id not in payloads
    ]
    if missing:
        raise ProtocolError(f"Missing payload(s): {', '.join(missing)}")
    return ParsedResponse(control, payloads)


def repair_prompt(error: Exception) -> str:
    return f"Your previous reply could not be parsed ({error}). Return the SAME intended actions only in valid {START}/CWAH_RESPONSE_V1_END format. Keep JSON small and payloads outside JSON."
