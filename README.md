# ADL 2023 final project
This repository provides an overview of the project's structure and serves as a guide on how to execute the experiments in our work *"Can LLMs Do It All? Towards Crafting Multi-Agent LLM Evaluators by LLMs"*. This project is built on top of [ChatEval](https://github.com/thunlp/ChatEval) [1].


- Reference
    1. [ChatEval: Towards Better LLM-based Evaluators through Multi-Agent Debate](https://arxiv.org/abs/2308.07201)

## Project Structure
The main folders and files are structured as follows:
```
.
├─ ...
├─ agentverse
│  ├─ ...
│  └─ tasks
│    ├─ ...
│    └─ llm_eval
│       ├─ data
│       │  ├─ ...
│       │  └─ faireval
│       │     └─ preprocessed_data
│       │        └─ test.json  //This file contains the dataset(Vicuna Bench & responses)
│       └─ multi_role
│         └─ only_static_assign
│            ├─ ...
│            └─ faireval
│               ├─ ...
│               └─ two_turns_sequential
│                 └─ two_different_role
│                    └─ calc_score_comparison
│                       └─ gpt_35_0301
│                          └─ config.yaml  //This file contains the personas for multi-agents and experimental settings
├─ llm_eval.py  //This is the main function for experiments.
└─ scripts
  └─ llm_eval
     ├─ ...
     └─ multi_role
       └─ only_static_assign
          ├─ ...
          └─ faireval
             ├─ ...
             └─ two_turns_sequential
               └─ two_different_role
                  ├─ calc_score_comparison
                  │  └─ gpt_35_0301.sh  //This is the script for running the experiments
                  └─ calc_score_comparison_reverse
                     └─ gpt_35_0301.sh  //This is the script for running the experiments with reverse responses to conduct position calibration
```

## Description of how to run the code
In our work, all experiments are carried out using the `gpt_35_0301.sh`. However, we alter the `config.yaml` which under `./agentverse/tasks/llm_eval/multi_role/only_static_assign/faireval/two_turns_sequential/two_different_role/calc_score_comparison/gpt_35_0301` for various experimental setups and distinct personas.

## Customized Persona
- First, switch to the `customize_persona` directory.
```bash
cd ./customize_persona
```

- Then, run the following command to generate the customized personas.
```bash
bash ./scripts/generate_persona.sh
```

- Finally, run the experiment with the generated personas as follows.
```bash
bash ./scripts/llm_eval.sh
```

- Note that we need to alter the `config.yaml` under `./agentverse/tasks/llm_eval/multi_role/only_static_assign/faireval/two_turns_sequential/two_different_role/calc_score_comparison/gpt_35_0301` directory for various experimental setups and distinct personas.