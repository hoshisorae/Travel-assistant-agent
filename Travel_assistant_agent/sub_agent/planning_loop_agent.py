from google.adk.agents import Agent, LoopAgent
from google.adk.tools import google_search, google_maps_grounding, FunctionTool 
from ..config import config
from ..tools import compare_budget_and_calculate_overage
from ..agent_utils import suppress_output_callback


def exit_planning_loop():
    """Called when the budget is approved by the Budget Keeper (APPROVED); sends a stop signal to the LoopAgent."""
    return {"status": "approved", "message": "Budget approved. Exiting planning loop."}

planning_coordinator = Agent(
    model=config.orchestrator_model, 
    name="planning_coordinator",
    description=
    """
    You are the central planning coordinator, responsible for combining activities and logistics into a coherent, actionable travel itinerary that respects the budget. You are in charge of planning.

    [Core Logic Changes]:
    - **New loop control**: you will receive {budget_review_result} from the 'budget_keeper'.
    - **If** the "decision" in {budget_review_result} is "APPROVED", you must immediately call the `exit_planning_loop` function to stop the entire loop.
    - **If** the decision is "REJECTED", you must revise the plan based on the "feedback" and output a new JSON plan.

    (...other instructions remain unchanged...)

    Tool Usage for Routing:
        - Use `Maps_grounding` to verify distances between selected locations to group them logically (e.g., "Day 1: North City", "Day 2: South City").
        - Use `Google Search` to find specific transit times or ticket prices if missing from the raw lists.

    Output Structure Mandate:
    Your output **must** be a structured JSON object (if the budget is rejected), or a call to the `exit_planning_loop` tool (if the budget is approved).
    """,
    tools=[
        google_search, 
        google_maps_grounding,
        FunctionTool(exit_planning_loop) 
    ], 
    output_key="draft_itinerary",
)

budget_keeper = Agent(
    model=config.critic_model, 
    name="budget_keeper",
    description=
    """
    You are the Budget Keeper, responsible for strictly ensuring the travel itinerary complies with the user's budget. You only approve or reject plans.

    Tool Usage:
        You must use the `compare_budget_and_calculate_overage` tool to validate the numbers.

    Input:
        You will receive the 'draft_itinerary' JSON.
        
    Output Structure Mandate:
        Your final output must be a JSON object that includes the approval/rejection signal and feedback:
        {
            "decision": "APPROVED" or "REJECTED",
            "feedback": "None" (if approved) OR "Specific instructions on what to cut..." (if rejected),
            "verified_total_cost": 1234.56
        }
    """,
    tools=[compare_budget_and_calculate_overage], 
    output_key="budget_review_result",
)

planning_loop_agent = LoopAgent(
    name="planning_loop_agent",
    description="Engine that iteratively plans and verifies the budget, maximizing cost efficiency within 3 attempts.",
    sub_agents=[
        budget_keeper,
        planning_coordinator,
    ],
    
    max_iterations=3, 
    after_agent_callback=suppress_output_callback,
)



print("✅ Planning Loop Agent created using FunctionTool exit pattern.")