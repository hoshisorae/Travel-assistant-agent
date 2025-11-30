import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types


try:
    from Travel_assistant_agent.agent import root_agent
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("请确认你是在项目根目录下运行，并且 'Travel_assistant_agent' 文件夹中包含 __init__.py")
    sys.exit(1)

async def main():
    """运行智能体并模拟用户查询流程"""
    
    print("🚀 初始化旅行规划智能体测试...")

    
    session_service = InMemorySessionService()
    app_name = "travel_app"
    user_id = "test_traveler"
    session_id = "session_001"
      
    await session_service.create_session(
        app_name=app_name, 
        user_id=user_id, 
        session_id=session_id
    )

 
    runner = Runner(
        agent=root_agent, 
        app_name=app_name, 
        session_service=session_service
    )

   
 
    queries = [
        "帮我规划一条从西雅图市中心到马萨诸塞州的塞勒姆的7天旅行，预算为5000美元，我想参观有关女巫审判相关的历史景点，我也很喜欢吃海鲜。",
        # "看起来不错，谢谢你的规划！" # 可选的第二轮对话
    ]

    print(f"✅ 智能体已加载: {root_agent.name}")
    print("----------------------------------------------------------------")

  
    for query in queries:
        print(f"\n🔵 [用户 User]: {query}")
        print("⚪ [系统]: 智能体正在思考和调用工具... (这可能需要几秒钟)")
        

        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=genai_types.Content(
                role="user", 
                parts=[genai_types.Part.from_text(text=query)]
            ),
        ):


            if event.is_final_response() and event.content and event.content.parts:
                response_text = event.content.parts[0].text
                print(f"\n🟢 [智能体 Agent]:\n{response_text}")

if __name__ == "__main__":


    asyncio.run(main())