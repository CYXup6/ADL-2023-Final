import os
import json
from typing import List
from agentverse.message import Message


def get_evaluation(setting: str = None, messages: List[Message] = None, agent_nums: int = None) -> List[dict]:

    discussion_results = []
    evaluation_results = []
    if setting == "every_agent":
        # save all the evaluation results
        for message in messages:
            discussion_results.append({"role": message.sender,
                            "discussion": message.content})

        # Currently 2 round, concurrent, so the response will start from messages[-3:]
        for message in messages[-agent_nums:]:
            evaluation_results.append({"role": message.sender,
                            "evaluation": message.content})

    return discussion_results, evaluation_results
