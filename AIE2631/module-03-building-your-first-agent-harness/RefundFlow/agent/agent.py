
from models import model
from tools import calculate_right_refund , get_today_date
from tools import issue_refund_ticket,get_user_purchase_history
from dotenv import load_dotenv
from langchain.agents import create_agent
from prompts import agent_system_prompt
from objects import Answer
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from uuid import uuid4

load_dotenv()

# Initialize the refund agent with the required tools, structured output,
# and conversation memory to maintain context across interactions.
agent = create_agent(
    model=model,
    system_prompt=agent_system_prompt,
    tools=[calculate_right_refund,get_user_purchase_history,issue_refund_ticket,get_today_date],
    response_format=Answer,
    checkpointer=InMemorySaver()
)

def run_conversation():
    # Generate a unique thread identifier for the current customer session.
    config = {"configurable": {"thread_id": str(uuid4())}}

    # Start the conversation with an initial customer refund request.
    text = "I would like to request a refund"
    print(text)
    
    question = HumanMessage(content=text)
    conversation = True

    # Continue interacting until the agent reaches a final refund decision.
    while conversation:

        # Invoke the agent and retrieve its validated structured response.
        response = agent.invoke({"messages":question}, config=config)
        structured_response = response["structured_response"]

        # Display the agent's response to the customer.
        print(structured_response.answer)

        # Determine whether additional customer interaction is required.
        conversation = structured_response.conversation

        if conversation:
            # Collect the customer's next message while preserving session context.
            user_input = input("reply: \n")
            question = HumanMessage(content=user_input)

    # Confirm that the refund support workflow has concluded.
    print("the job is done!")

# Uncomment the following line to launch the interactive refund agent.
#run_conversation()
