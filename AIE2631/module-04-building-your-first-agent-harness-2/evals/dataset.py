import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent"))

from agent import agent
from dataset import dataset
from model import eval_model

from deepeval.metrics import TaskCompletionMetric
from deepeval.integrations.langchain import CallbackHandler


SUCCESSFUL_TASK_DEFINITION = """
The agent succeeds when its actions, decisions, tool usage,
and final response satisfy the following criteria:

1. CUSTOMER IDENTIFICATION
- If the username is missing, request it without issuing a refund.
- If the username cannot be validated through purchase records,
  request a valid username without issuing a refund or disclosing
  purchase history.

2. REFUND ELIGIBILITY
- Retrieve and verify the customer's purchase history.
- Ensure each requested purchase is within 30 days, inclusive,
  and its purchase date is not in the future.
- Refund only explicitly requested and previously purchased items.
- Refund all items only when explicitly requested.
- Calculate the exact eligible amount using verified purchase records.
- Do not communicate internal checks unless explaining rejection.

3. CLARIFICATION
- If essential information is missing or ambiguous, request
  clarification without making assumptions or issuing a refund.
- Requesting necessary clarification counts as task success.

4. REFUND EXECUTION
- Issue a refund ticket only after all applicable eligibility
  checks pass, using the correct amount and authorized items.
- Claim successful issuance only when confirmed by the refund tool.
- Never issue refunds for ineligible requests.

5. FINAL RESPONSE
- Approved: Confirm successful ticket issuance, specifying the
  refund amount and refunded item names.
- Rejected: Confirm that no ticket was issued and explain why.

6. NON-REFUND REQUESTS
- Answer informational, policy-related, or other non-refund
  requests appropriately without issuing refund tickets.

7. DATA INTEGRITY
- Never fabricate customer information, purchase records,
  purchase dates, refund amounts, or tool execution results.
- Unauthorized refunds, incorrect amounts, refunds for unpurchased
  items, or false execution claims constitute task failure.
"""


metrics = [
    TaskCompletionMetric(
        threshold=0.8,
        model=eval_model,
        task=SUCCESSFUL_TASK_DEFINITION,
        include_reason=True,
    )
]


for golden in dataset.evals_iterator(metrics=metrics):
    response = agent.invoke(
        {"messages": [{"role": "user", "content": golden.input}]},
        config={
            "configurable": {"thread_id": str(uuid4())},
            "callbacks": [CallbackHandler()],
        },
    )
