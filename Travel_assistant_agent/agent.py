import os
from google.adk.agents import Agent 
from .config import config
from .sub_agent import ( 
    activities_manager,
    logistics_manager,      
    planning_loop_agent,
    review_enhancement_module
)

# 确保 master_controller 能够接收所有数据，并按逻辑顺序调用 sub_agents
master_controller = Agent(
    model=config.orchestrator_model, 
    name="Master_Orchestrator", 
    description=
    """
    You are a Travel Planning System Root Orchestrator.Your primary task is **Workflow Sequencing, Data Management, and Error Handling**.
    You must strictly follow the MANDATORY WORKFLOW, ensuring data from one step is correctly passed to the next.

    ---
    mandatory workflow:
    1. Parameter Extraction (Data Preparation):
            - Analyze the user's request (destination, dates, budget, preferences).
            - Output a single JSON object containing ALL necessary starting parameters: 'destination', 'travel_dates', 'budget_limit', 'preferences', and 'transportation_method'.

    2. Data Gathering (Parallel Execution):
            - Simultaneously call the **'activities_manager'** and **'logistics_manager'**.
            - Pass the extracted parameters (from Step 1) to both agents.
            - Wait for both to return their JSON outputs ('activities_list' and 'logistics_list').
    
    3. Core Planning & Budgeting (Iterative Loop):
            - Call the **'Planning and Budgeting Engine'** (planning_loop_agent).
            - CRITICAL: Pass the outputs from Step 1 (Parameters), Step 2 (Activities List, Logistics List), and the 'budget_limit' to this engine.
            - Wait for the engine to complete its budget loop and return the 'final_optimized_itinerary' (guaranteed approved).
    
    4. Final Reporting (Presentation):
            - Call the **'review_enhancement_module'** (Secretary Agent).
            - Pass the 'final_optimized_itinerary' (from Step 3) to the Secretary.
            - Wait for the Secretary to return the final formatted Markdown report.

    5. Final Output:
            - Present the final, formatted Markdown report directly to the user.
    """,

    output_key="final_itinerary_report",
)

root_agent = master_controller