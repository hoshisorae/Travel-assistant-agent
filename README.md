# project Overview - Travel Assistant Agent

This project contains the core logic for the Travel Assistant Agent, a robust multi-agent system designed to handle complex, end-to-end travel planning with mandatory budget constraints. The agent is built using the Google Agent Development Kit (ADK) and follows a highly modular, workflow-sequenced architecture.

## Problem Statement

Traditional travel planning is highly inefficient, demanding significant manual effort to:

Synthesize Diverse Constraints: Users must juggle multiple, often conflicting, constraints like budget limits, destination preferences, dates, and activity types.

Verify Feasibility: Planners must constantly cross-reference activities and logistics against the total budget, leading to tedious, iterative revisions (e.g., finding cheaper flights to afford a better hotel).

Fragmented Data Gathering: Information gathering for flights, accommodation, and attractions typically requires searching multiple websites (fragmentation).

This manual process is time-consuming, prone to calculation errors, and often leads to suboptimal travel experiences due to budget overruns or missed opportunities.

## Solution Statement

A multi-agent system provides a scalable and efficient solution:

Automated Budget Loop: The core planning_loop_agent automatically iterates and validates the itinerary against the hard budget limit, eliminating manual recalculations and guaranteeing a compliant final plan.

Parallel Efficiency: Dedicated sub-agents (activities_manager, logistics_manager) perform data gathering concurrently, dramatically accelerating the research phase.

Orchestrated Workflow: The system follows a fixed, verifiable workflow, ensuring every output is built upon validated data from the preceding step, leading to a robust, high-quality itinerary.

## Architecture

Core to the Travel Assistant Agent is the Master_Orchestrator, which manages the entire planning lifecycle. It is not a monolithic application but a project manager that coordinates specialized sub-agents.

The Master_Orchestrator is constructed using the Agent class from the Google ADK. Its definition mandates a strict, five-step sequential workflow, focusing on data transfer and error handling. Crucially, it relies on the ADK runtime to execute the sub-agents based on the defined flow, rather than delegating via function calling (to avoid API limitations with multiple tools).

### The real power of the system lies in its team of specialized sub-agents:

**Parameter Extractor (Implicit Step 1):**

The Orchestrator's initial role is to act as a data preparation agent, analyzing the raw user prompt and outputting a single, structured JSON object containing all necessary constraints (destination, dates, budget, etc.).

**Data Gatherers (Parallel Execution):**

Activities Manager (activities_manager): Focuses purely on generating a list of potential activities and associated costs based on user preferences.

Logistics Manager (logistics_manager): Focuses purely on generating options for transportation (flights, ground) and accommodation, along with associated costs.

**Core Planning & Budgeting Engine:**

Planning Loop Agent (planning_loop_agent): This is the heart of the system. It receives the full dataset (Parameters, Activities, Logistics) and iteratively constructs an itinerary. It acts as a LoopAgent that self-validates or triggers recalculations until the Total Cost is verified to be below the Budget Limit.

**Final Reporting Agent:**

Review Enhancement Module (review_enhancement_module): Acts as a Secretary Agent. It receives the final, optimized JSON itinerary and formats it into the user-friendly, high-quality Markdown report presented to the user.

## Workflow

The Master_Orchestrator strictly enforces this five-step sequence:

**Parameter Extraction:** Convert raw user query into structured JSON parameters (destination, budget_limit, preferences).

**Data Gathering (Parallel):** Call activities_manager and logistics_manager simultaneously using the extracted parameters.

**Core Planning & Budgeting (Loop):**  Pass parameters + all gathered data (Activities/Logistics lists) to the planning_loop_agent to iterate until a budget-approved itinerary is generated.

**Final Reporting:** Pass the 'final_optimized_itinerary' to the review_enhancement_module.

**Output:**  Present the final formatted Markdown report to the user.



## Installation
This project was built against Python 3.11.It is suggested you create a virtual environment using your preferred tooling (e.g., venv or uv).

**Install dependencies:**
```bash
pip install google-adk google-genai aiohttp
```

**Running the Agent in ADK Web mode**

From the command line of the working directory execute the following command.
```bash
adk web
```

**Run the integration test:**

For a non-interactive, end-to-end test of the workflow, run:
```bash
python run_test.py
```


## Project Structure

Travel_assistant_agent/: The main Python package for the agent.

* agent.py: Defines the main Master_Orchestrator and the core sequential workflow.

   * agent_utils.py: Contains utility functions, such as suppress_output_callback, used for flow control and output management.

   * sub_agent/: Contains the individual sub-agents, each responsible for a specific task.

   * config.py: Contains the configuration for the agents, such as the models to use.

* run_test.py: Integration test script demonstrating the full workflow execution.
