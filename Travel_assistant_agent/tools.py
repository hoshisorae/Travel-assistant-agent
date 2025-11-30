 

def compare_budget_and_calculate_overage(total_cost: float, budget_limit: float) -> dict:
    """
    精确对比行程总花费与用户预算。
    
    Args:
        total_cost (float): 规划出的行程总费用。
        budget_limit (float): 用户的预算上限。如果为 0 或 None，表示无预算限制。

    Returns:
        dict: 包含审核结果状态、差额数值、超支百分比和建议消息的结构化字典。
    """
    # 1. 处理无预算限制的情况
    if budget_limit is None or budget_limit <= 0:
        return {
            "status": "APPROVED",
            "message": "User did not specify a budget limit. Plan approved automatically.",
            "difference": 0.0,
            "overage_percent": 0.0
        }

    # 2. 计算差额
    difference = total_cost - budget_limit

    # 3. 预算内 -> 批准
    if difference <= 0:
        return {
            "status": "APPROVED",
            "message": f"Plan is within budget. Remaining funds: {abs(difference):.2f}",
            "difference": difference,
            "overage_percent": 0.0
        }
    
    # 4. 超支 -> 拒绝
    else:
        overage_percent = (difference / budget_limit) * 100
        return {
            "status": "REJECTED",
            "message": f"Budget exceeded by {difference:.2f} ({overage_percent:.1f}%). Cost reduction required.",
            "difference": difference,
            "overage_percent": round(overage_percent, 2)
        }
