from typing import Callable, Dict, Any
from app.utils.logger import get_logger
import time


logger = get_logger(__name__)

def create_node(agent_func):
    def node(state):
        start = time.time()

        try:
            logger.info(f"[START] {agent_func.__name__}")

            result = agent_func(state)

            duration = round(time.time() - start, 3)

            logger.info(f"[END] {agent_func.__name__} ({duration}s)")

            return result

        except Exception as e:
            logger.error(f"[FAIL] {agent_func.__name__}: {str(e)}")
            return {"errors": [str(e)]}

    return node