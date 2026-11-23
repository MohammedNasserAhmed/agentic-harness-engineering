from pydantic import BaseModel, Field


class RefundResponse(BaseModel):
    answer: str = Field(
        description="The response provided to the user regarding their inquiry."
    )
    conversation: bool = Field(
        description="Indicates whether the conversation should continue. " \
                    "Set to False when the agent has reached a final refund decision; " \
                    "otherwise, set to True if further discussion or information is required.",
        default=True
    )


class PurchasedItem(BaseModel):
    name: str = Field(
        description="The name of the item purchased by the customer."
    )
