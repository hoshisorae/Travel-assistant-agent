from google.adk.agents import Agent, LoopAgent
from google.adk.tools import google_search, google_maps_grounding, FunctionTool 
from ..config import config
from ..tools import compare_budget_and_calculate_overage
from ..agent_utils import suppress_output_callback

# ----------------------------------------------------------------------
# 【新增】循环退出函数 - 取代 BaseChecker 的作用
# ----------------------------------------------------------------------
def exit_planning_loop():
    """在预算被 Budget Keeper 批准 (APPROVED) 时调用，向 LoopAgent 发送停止信号。"""
    # 返回一个状态字典，LoopAgent 会识别工具调用并停止循环
    return {"status": "approved", "message": "Budget approved. Exiting planning loop."}

planning_coordinator = Agent(
    model=config.orchestrator_model, 
    name="planning_coordinator",
    description=
    """
    你是中央计划协调员，负责将活动和物流数据合成为一个连贯、可执行且考虑预算的旅行行程。你负责计划。
    
    【核心逻辑修改】：
    - **新循环控制**: 你将接收来自 'budget_keeper' 的 {budget_review_result}。
    - **如果** {budget_review_result} 中的 "decision" 是 "APPROVED"，你必须立即调用 `exit_planning_loop` 函数以停止整个循环。
    - **如果** decision 是 "REJECTED"，你必须根据 "feedback" 修正计划，并输出新的 JSON 计划。
    
    （...其他指令保持不变...）

    Tool Usage for Routing:
        - Use `Maps_grounding` to verify distances between selected locations to group them logically (e.g., "Day 1: North City", "Day 2: South City").
        - Use `Google Search` to find specific transit times or ticket prices if missing from the raw lists.

    Output Structure Mandate:
        你的输出 **必须** 是一个结构化的 JSON 对象（如果预算被拒绝），或者调用 `exit_planning_loop` 工具（如果预算被批准）。
    """,
    tools=[
        google_search, 
        google_maps_grounding,
        FunctionTool(exit_planning_loop) # <-- 新增退出工具
    ], 
    output_key="draft_itinerary",
)

budget_keeper = Agent(
    model=config.critic_model, 
    name="budget_keeper",
    description=
    """
    你是预算守护者，负责严格确保旅行行程遵守用户预算。你只批准或拒绝计划。
    
    Tool Usage:
        你必须使用 `compare_budget_and_calculate_overage` 工具来验证数字。

    Input:
        你会收到 'draft_itinerary' JSON。
        
    Output Structure Mandate:
        你的最终输出必须是一个 JSON 对象，包含批准/拒绝信号和反馈：
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
        # LoopAgent 会重复运行：
        # 1. planning_coordinator (输出计划或调用退出工具)
        # 2. budget_keeper (输出审计结果)
        budget_keeper,
        planning_coordinator,
    ],
    
    max_iterations=3, 
    after_agent_callback=suppress_output_callback,
)



print("✅ Planning Loop Agent created using FunctionTool exit pattern.")