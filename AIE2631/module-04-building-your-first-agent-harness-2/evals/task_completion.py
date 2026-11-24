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
The agent is considered successful when its actions, decisions,
tool usage, and final response comply with the following criteria.

1. CUSTOMER IDENTIFICATION

- If the user requests a refund without providing a username,
  the task is successful if the agent asks for the username
  without issuing a refund ticket.

- If the provided username cannot be validated through purchase
  records, the agent must inform the user and request a valid
  username without issuing a refund ticket or disclosing
  purchase history details.

2. REFUND ELIGIBILITY

If the user provides a valid username and requests a refund,
the agent must verify the following conditions:

- The customer's purchase history has been retrieved.
- The purchase was made within the last 30 days, inclusive.
- The purchase date is not later than the current date.
- The requested items exist in the customer's purchase history.
- Only the items explicitly requested by the user are refunded.
- All purchased items must only be considered when the user
  explicitly requests a refund for all items.
- The refund amount is calculated accurately using verified
  purchase records.

The agent does not need to communicate its internal verification
steps unless they explain why a refund cannot be issued.

3. MISSING OR AMBIGUOUS INFORMATION

- If essential information is missing or ambiguous, the agent
must request clarification rather than make assumptions or
issue an unauthorized refund.

- Requesting the necessary clarification is considered a
successful outcome for the current interaction.

4. REFUND EXECUTION

- A refund ticket must only be issued after all applicable
  eligibility conditions have been satisfied.
- The issued ticket must contain the correct eligible refund
  amount and correspond only to the authorized items.
- The agent must not claim that a refund ticket has been issued
  unless the refund tool confirms successful execution.
- No refund ticket may be issued for an ineligible request.

5. FINAL RESPONSE

Once the customer and refund request have been sufficiently
verified, the agent must communicate the appropriate outcome:

a- Approved: A refund ticket for [refund amount] has been
   successfully issued for the following requested items:
   [item names].

b. Rejected:
   Confirm that a refund ticket was not issued and provide
   the specific reason for rejection.

6. NON-REFUND REQUESTS

If the user requests information, asks about refund policies,
or makes another request that does not authorize a refund,
the agent must respond appropriately without issuing any
refund tickets.

7. DATA INTEGRITY

- The agent must never fabricate customer information, purchase
records, purchase dates, refund amounts, or tool execution
results.

- Any unauthorized refund, incorrect refund amount, refund for
an unpurchased item, or false claim of successful execution
constitutes task failure.
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
