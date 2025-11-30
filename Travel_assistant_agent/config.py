import os
from dataclasses import dataclass
import google.auth



# 1. 明确指定你的项目 ID
# ---------------------------------------------
# 替换为你的项目 ID (即你设置的配额项目 ID)
PROJECT_ID = "ringed-bebop-478606-d1" 
# ---------------------------------------------

os.environ.setdefault("GOOGLE_CLOUD_PROJECT", PROJECT_ID)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")


@dataclass
class TravelAgentConfiguration:
    """Configuration for travel-related models and parameters.

    Attributes:
        orchestrator_model (str): Model for orchestration tasks.
        critic_model (str): Model for evaluation tasks.
        worker_model (str): Model for working/generation tasks.
        max_search_iterations (int): Maximum search iterations allowed.
    """
    orchestrator_model: str = "gemini-2.5-pro"
    critic_model: str = "gemini-2.5-pro"
    worker_model: str = "gemini-2.5-flash"
    max_search_iterations: int = 10


config = TravelAgentConfiguration()