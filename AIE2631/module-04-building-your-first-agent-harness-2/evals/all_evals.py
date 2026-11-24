
import sys
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv

from deepeval import evaluate
from deepeval.evaluate import CacheConfig, DisplayConfig
from deepeval.integrations.langchain import CallbackHandler
from deepeval.metrics import (
    ArgumentCorrectnessMetric,
    GEval,
    PlanAdherenceMetric,
    PlanQualityMetric,
    StepEfficiencyMetric,
    TaskCompletionMetric,
    ToolCorrectnessMetric,
)
from deepeval.test_case import LLMTestCase, SingleTurnParams, ToolCall, ToolCallParams

# Support both package-based and direct script execution.
if __package__:
    from .dataset import dataset
    from .model import eval_model
else:
    from dataset import dataset
    from model import eval_model


# Define the business rules and success criteria used to evaluate
# whether the agent has correctly completed the customer's request.
SUCCESSFUL_TASK_DEFINITION = """
If the username is missing, ask the user to provide it.
For a refund request, identify the customer and the requested purchases, and
check that each purchase is no more than 30 days old and is not in the future.
Refund only the items requested by the user. If the customer or requested item
cannot be found, do not issue a refund ticket and explain why.
Once the necessary information is available, tell the user whether a refund
ticket was issued and its amount, or explain why no refund was issued.
For an information-only request, answer the question without issuing a ticket.
"""


def build_metrics():
    """Initialize the seven evaluation metrics using the configured evaluator model and thresholds."""

    # Agentic metrics: evaluate the agent's execution trajectory,
    # task completion, planning quality, plan adherence, and efficiency.
    trace_metrics = [
        TaskCompletionMetric(
            threshold=0.8,
            model=eval_model,
            task=SUCCESSFUL_TASK_DEFINITION,
            include_reason=True,
        ),
        StepEfficiencyMetric(
            threshold=0.8,
            model=eval_model,
            include_reason=True,
        ),
        PlanQualityMetric(
            threshold=0.8,
            model=eval_model,
            include_reason=True,
        ),
        PlanAdherenceMetric(
            threshold=0.8,
            model=eval_model,
            include_reason=True,
        ),
    ]

    # Single-turn metrics: evaluate tool argument accuracy,
    # tool selection and usage, and final answer correctness.
    single_turn_metrics = [
        ArgumentCorrectnessMetric(
            threshold=None,
            model=eval_model,
            include_reason=True,
        ),
        ToolCorrectnessMetric(
            threshold=0.9,
            model=eval_model,
            include_reason=True,
            evaluation_params=[ToolCallParams.INPUT_PARAMETERS],
        ),
        GEval(
            name="Answer Correctness",
            evaluation_params=[
                SingleTurnParams.INPUT,
                SingleTurnParams.ACTUAL_OUTPUT,
                SingleTurnParams.EXPECTED_OUTPUT,
            ],
            evaluation_steps=[
                "Check that the actual output and expected output have the same "
                "logical conclusion about the user's request.",
            ],
            threshold=0.8,
            model=eval_model,
            verbose_mode=True,
        ),
    ]
    return trace_metrics, single_turn_metrics


def main():
    # Load environment variables, including API credentials.
    load_dotenv()

    # Add the agent directory to the Python module search path
    # and import the refund agent.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent"))
    from agent import agent

    # Initialize evaluation metrics and execution configurations.
    trace_metrics, single_turn_metrics = build_metrics()

    # Disable cache reading and writing to ensure fresh evaluations.
    cache_config = CacheConfig(use_cache=False, write_cache=False)

    # Disable automatic post-evaluation result inspection.
    display_config = DisplayConfig(inspect_after_run=False)

    # Store generated test cases for single-turn evaluation.
    test_cases = []

    # Phase 1: Execute each golden test case and evaluate the
    # agent's execution trajectory using the four agentic metrics.
    for golden in dataset.evals_iterator(
        metrics=trace_metrics,
        cache_config=cache_config,
        display_config=display_config,
    ):
        # Invoke the agent using the predefined golden input.
        # Generate a unique thread ID to isolate each conversation.
        # Register CallbackHandler to capture the execution trace
        # required by the agentic evaluation metrics.
        response = agent.invoke(
            {"messages": [{"role": "user", "content": golden.input}]},
            config={
                "configurable": {"thread_id": str(uuid4())},
                "callbacks": [CallbackHandler()],
            },
        )

        # Extract all tool calls and their input arguments
        # from the agent's conversation and execution history.
        tools_called = []
        for message in response["messages"]:
            for tool_call in getattr(message, "tool_calls", []) or []:
                tools_called.append(
                    ToolCall(
                        name=tool_call["name"],
                        input_parameters=tool_call["args"],
                    )
                )

        # Convert the existing agent response into an LLMTestCase.
        # Include the original input, actual answer, expected answer,
        # executed tool calls, and expected tool calls.
        # Reuse the same execution to avoid redundant agent invocations
        # and unnecessary token consumption.
        # Keep test cases local to prevent dataset duplication across runs.
        test_cases.append(
            LLMTestCase(
                input=golden.input,
                actual_output=response["structured_response"].answer,
                expected_output=golden.expected_output,
                tools_called=tools_called,
                expected_tools=golden.expected_tools,
            )
        )

    # Phase 2: Evaluate the collected test cases using the three
    # single-turn metrics without executing the refund agent again.
    evaluate(
        test_cases=test_cases,
        metrics=single_turn_metrics,
        cache_config=cache_config,
        display_config=display_config,
    )

    # Display a summary of the completed evaluation process.
    print(f"\nCompleted all 7 metrics for {len(test_cases)} test cases.")


# Execute the evaluation pipeline when this script runs directly.
if __name__ == "__main__":
    main()
