"""Small, framework-independent helpers for the refund chat UI."""

from collections.abc import Iterable
from typing import Any


TOOL_ACTIVITY = {
    "get_user_purchase_history": "Checking purchase history",
    "get_today_date": "Checking the purchase date",
    "calculate_right_refund": "Calculating the refund amount",
    "issue_refund_ticket": "Creating the refund ticket",
}


def friendly_tool_steps(messages: Iterable[Any]) -> list[str]:
    """Return each known tool call once, in the order the agent made it."""
    steps: list[str] = []
    seen_call_ids: set[str] = set()

    for message in messages:
        for tool_call in getattr(message, "tool_calls", []) or []:
            name = tool_call.get("name")
            call_id = tool_call.get("id") or f"{name}:{tool_call.get('args', {})}"
            if name in TOOL_ACTIVITY and call_id not in seen_call_ids:
                seen_call_ids.add(call_id)
                steps.append(TOOL_ACTIVITY[name])

    return steps
