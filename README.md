# ADL 2023 final project
This repository provides an overview of the project's structure and serves as a guide on how to execute the experiments in our work [Can LLMs Do It All? Towards Crafting Multi-Agent LLM Evaluators by LLMs]. This project is built on top of https://github.com/thunlp/ChatEval.

### Project Structure
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
