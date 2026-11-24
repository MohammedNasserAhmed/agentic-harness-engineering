from types import SimpleNamespace
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ui_helpers import friendly_tool_steps


def test_friendly_tool_steps_maps_known_tools_once():
    messages = [
        SimpleNamespace(
            tool_calls=[
                {"id": "one", "name": "get_user_purchase_history", "args": {}},
                {"id": "one", "name": "get_user_purchase_history", "args": {}},
                {"id": "two", "name": "issue_refund_ticket", "args": {}},
            ]
        )
    ]

    assert friendly_tool_steps(messages) == [
        "Checking purchase history",
        "Creating the refund ticket",
    ]


def test_friendly_tool_steps_ignores_unknown_tools():
    messages = [SimpleNamespace(tool_calls=[{"id": "one", "name": "unknown", "args": {}}])]

    assert friendly_tool_steps(messages) == []
