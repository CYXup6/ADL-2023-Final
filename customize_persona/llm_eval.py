import os

# # always remember to put these lines at the top of your code if you are using clash
# os.environ["http_proxy"] = "http://127.0.0.1:7890"
# os.environ["https_proxy"] = "http://127.0.0.1:7890"
# os.environ["all_proxy"] = "socks5://127.0.0.1:7890"

import json
from eval_helper.get_evaluation import get_evaluation

from agentverse.agentverse import AgentVerse
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("--task", type=str, default="llm_eval/multi_role/only_static_assign/adversarial/two_turns_sequential/three_different_role/calc_score_comparison/gpt_4")
parser.add_argument("--data_path", type=str, default="./agentverse/tasks/llm_eval/data/adversarial/preprocessed_data/test.json")
parser.add_argument("--output_dir", type=str, default="./outputs/llm_eval/")
parser.add_argument("--reverse_input", default=False, action="store_true")
parser.add_argument("--persona_file", type=str, default="./persona/persona.json")

args = parser.parse_args()

print(args)

os.makedirs(args.output_dir, exist_ok=True)
with open(os.path.join(args.output_dir, "args.txt"), "w") as f:
    f.writelines(str(args))


with open(args.data_path) as f:
    data = json.load(f)

# load persona from json file
with open(args.persona_file) as f:
    persona = json.load(f)

agentverse = AgentVerse.from_task(args.task)

if "faireval" in args.data_path:
    pair_comparison_output = []

    for num, ins in enumerate(data[:80]):

        print(f"================================instance {num}====================================")

        # reassign the text to agents, and set final_prompt to null for debate at first round
        for agent_id in range(len(agentverse.agents)):
            agentverse.agents[agent_id].source_text = ins["question"]

            if args.reverse_input:
                agentverse.agents[agent_id].compared_text_one = ins["response"]["vicuna"]
                agentverse.agents[agent_id].compared_text_two = ins["response"]["gpt35"]
            else:
                agentverse.agents[agent_id].compared_text_one = ins["response"]["gpt35"]
                agentverse.agents[agent_id].compared_text_two = ins["response"]["vicuna"]

            agentverse.agents[agent_id].name = list(persona['post_process'][num].keys())[agent_id]
            agentverse.agents[agent_id].role_description = persona['post_process'][num][agentverse.agents[agent_id].name]
            agentverse.agents[agent_id].final_prompt = ""

        agentverse.run()

        evaluation = get_evaluation(setting="every_agent", messages=agentverse.agents[0].memory.messages, agent_nums=len(agentverse.agents))

        pair_comparison_output.append({"question": ins["question"],
                                       "response": {"gpt35": ins["response"]["gpt35"],
                                                    "vicuna": ins["response"]["vicuna"]},
                                       "discussion": evaluation[0],
                                       "evaluation": evaluation[1]})

        os.makedirs(args.output_dir, exist_ok=True)
        with open(os.path.join(args.output_dir, "pair_comparison_results.json"), "w") as f:
            json.dump(pair_comparison_output, f, indent=4)


elif "adversarial" in args.data_path:

    pair_comparison_output = []

    for num, ins in enumerate(data):

        print(f"================================instance {num}====================================")

        # reassign the text to agents, and set final_prompt to null for debate at first round
        for agent_id in range(len(agentverse.agents)):
            agentverse.agents[agent_id].source_text = ins["question"]

            if args.reverse_input:
                agentverse.agents[agent_id].compared_text_one = ins["response"]["output_2"]
                agentverse.agents[agent_id].compared_text_two = ins["response"]["output_1"]
            else:
                agentverse.agents[agent_id].compared_text_one = ins["response"]["output_1"]
                agentverse.agents[agent_id].compared_text_two = ins["response"]["output_2"]

            agentverse.agents[agent_id].final_prompt = ""

        agentverse.run()

        evaluation = get_evaluation(setting="every_agent", messages=agentverse.agents[0].memory.messages,
                                    agent_nums=len(agentverse.agents))

        pair_comparison_output.append({"question": ins["question"],
                                       "response": {"output_1": ins["response"]["output_1"],
                                                    "output_2": ins["response"]["output_2"]},
                                       "discussion": evaluation[0],
                                       "evaluation": evaluation[1]})

        os.makedirs(args.output_dir, exist_ok=True)
        with open(os.path.join(args.output_dir, "pair_comparison_results.json"), "w") as f:
            json.dump(pair_comparison_output, f, indent=4)