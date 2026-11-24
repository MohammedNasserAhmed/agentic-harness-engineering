from deepeval.dataset import EvaluationDataset, Golden
from deepeval.test_case import ToolCall

dataset = EvaluationDataset(
    goldens=[
        Golden(
            input="I am customer201, I would like a refund for the laptop_stand and usb_hub",
            expected_output="A refund ticket for $32 has been issued successfully",
            expected_tools=[
                ToolCall(
                    name="get_user_purchase_history",
                    input_parameters={"user": "customer201"},
                ),
                ToolCall(name="get_today_date", input_parameters={}),
                ToolCall(
                    name="calculate_right_refund",
                    input_parameters={
                        "user": "customer201",
                        "items": [{"name": "laptop_stand"}, {"name": "usb_hub"}],
                    },
                ),
                ToolCall(
                    name="issue_refund_ticket",
                    input_parameters={"user": "customer201", "refund_amount": 32},
                ),
            ],
        ),
        Golden(
            input="I am customer201, I would like a refund for the laptop_stand",
            expected_output="A refund ticket for $20 has been issued successfully",
            expected_tools=[
                ToolCall(
                    name="get_user_purchase_history",
                    input_parameters={"user": "customer201"},
                ),
                ToolCall(name="get_today_date", input_parameters={}),
                ToolCall(
                    name="calculate_right_refund",
                    input_parameters={
                        "user": "customer201",
                        "items": [{"name": "laptop_stand"}],
                    },
                ),
                ToolCall(
                    name="issue_refund_ticket",
                    input_parameters={"user": "customer201", "refund_amount": 20},
                ),
            ],
        ),
        Golden(
            input="I am customer201, I do not want a refund. I just want to know what I purchased",
            expected_output="No refund tickets were issued. Only the customer's purchased items were listed",
            expected_tools=[
                ToolCall(
                    name="get_user_purchase_history",
                    input_parameters={"user": "customer201"},
                ),
            ],
        ),
        Golden(
            input="I am customer999, I would like a refund for the usb_hub",
            expected_output="Inform the customer that the username is invalid and request a valid username",
            expected_tools=[
                ToolCall(
                    name="get_user_purchase_history",
                    input_parameters={"user": "customer999"},
                ),
            ],
        ),
        Golden(
            input="I am customer305, I would like a refund for the wireless_mouse",
            expected_output="A refund ticket for $18 has been issued successfully",
            expected_tools=[
                ToolCall(
                    name="get_user_purchase_history",
                    input_parameters={"user": "customer305"},
                ),
                ToolCall(name="get_today_date", input_parameters={}),
                ToolCall(
                    name="calculate_right_refund",
                    input_parameters={
                        "user": "customer305",
                        "items": [{"name": "wireless_mouse"}],
                    },
                ),
                ToolCall(
                    name="issue_refund_ticket",
                    input_parameters={"user": "customer305", "refund_amount": 18},
                ),
            ],
        ),
        Golden(
            input="I am customer201, I would like a refund for the usb_hub",
            expected_output="A refund ticket for $12 has been issued successfully only for the usb_hub",
            expected_tools=[
                ToolCall(
                    name="get_user_purchase_history",
                    input_parameters={"user": "customer201"},
                ),
                ToolCall(name="get_today_date", input_parameters={}),
                ToolCall(
                    name="calculate_right_refund",
                    input_parameters={
                        "user": "customer201",
                        "items": [{"name": "usb_hub"}],
                    },
                ),
                ToolCall(
                    name="issue_refund_ticket",
                    input_parameters={"user": "customer201", "refund_amount": 12},
                ),
            ],
        ),
        Golden(
            input="I am customer201, I would like a refund for the wireless_mouse",
            expected_output="No refund was issued because the customer did not purchase this item",
            expected_tools=[
                ToolCall(
                    name="get_user_purchase_history",
                    input_parameters={"user": "customer201"},
                ),
            ],
        ),
    ]
)
