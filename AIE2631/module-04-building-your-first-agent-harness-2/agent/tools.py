from langchain.tools import tool
from data import users_data
from dotenv import load_dotenv
import logging
from schemas import PurchasedItem
from datetime import date

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s "
)


@tool
def get_user_purchase_history(user: str) -> dict:
    """Retrieve the purchase history associated with the provided username.
    Return the customer's purchase records if the username exists."""
    logging.info(f"using get_user_purchase_history tool on user: {user}")
    if users_data.get(user):
        return users_data[user]
    return {"status": "there was no username found"}


@tool
def calculate_right_refund(user: str, items: list[PurchasedItem]) -> str:
    """Calculate the total refund amount for the specified purchased items.
    Requires a valid username and a list of items requested for refund."""

    logging.info(f"using calculate_right_refund tool to get user's: {user} refund")

    if users_data.get(user):
        total_refund = 0

        for item in items:
            if users_data[user].get(item.name):
                total_refund += users_data[user][item.name]["price"]

        return f"the value of the refund is: {total_refund}"

    return {"status": "there was no username found"}


@tool
def issue_refund_ticket(user: str, refund_amount: int) -> str:
    """Create and submit a refund ticket for the specified customer and amount.
    Use only after verifying the customer's eligibility and refund value."""

    logging.info(f"using issue_refund_ticket for user: {user}")
    return f"a refund ticket has been issued successfully with the amount of {refund_amount}"


@tool
def get_today_date() -> str:
    """Retrieve the current date in YYYY-MM-DD format.
    This tool requires no arguments and should only be called after verifying
    that the customer exists and has a purchased item eligible for review."""
    logging.info(f"using the date tool")
    return date.today().isoformat()


# Example: Retrieve a customer's purchase history
# print(get_user_purchase_history.invoke("customer201"))

# Example: Define purchased items for a refund request
# laptop_stand = PurchaseItem(name="laptop_stand")
# usb_hub = PurchaseItem(name="usb_hub")

# Example: Calculate the refund amount for selected items
# print(calculate_right_refund.invoke({"user":"customer201",
#                                      "items":[laptop_stand, usb_hub]}))

# Example: Issue a refund ticket for a verified customer
# print(issue_refund_ticket.invoke({"user":"customer201", "refund_amount":32}))

# Example: Retrieve the current date for refund eligibility validation
# print(get_today_date.invoke({}))
