import json
import re
import argparse
import pandas as pd
from sklearn.metrics import cohen_kappa_score


def get_calibration (method = "compare_between_agent"): 
    global q_num

    if method == "compare_with_human":

        for i in data:
            asst1 = 0
            asst2 = 0
            q_num+=1
            # print ("Question number:" + str(q_num))
            for e in i["evaluation"]:
                # Input string
                input_string = e["evaluation"]

                # Regular expression to extract the score number
                pattern1 = r'The score of Assistant 1: ([\d.]+)'
                pattern2 = r'The score of Assistant 2: ([\d.]+)'
                # Use re.search to find the match
                match1 = re.search(pattern1, input_string)
                match2 = re.search(pattern2, input_string)
                # Check if a match is found
                if match1:
                    # Extract the score number from the matched group
                    score_number = match1.group(1)
                    #print(e["evaluation"])
                    # print("Assistant 1 Score Number:", score_number)
                    asst1+=float(score_number)
                else:
                    pass
                    #print(e)
                    # print("No score found for assistant 1.")
                # Check if a match is found
                if match2:
                    # Extract the score number from the matched group
                    score_number = match2.group(1)
                    #print(e["evaluation"])
                    # print("Assistant 2 Score Number:", score_number)
                    asst2+=float(score_number)
                else:
                    pass
                    # print(e)
                    # print("No score found for assistant 2.") # here
            if asst1>asst2:
                results.append("CHATGPT")
                # results.append("VICUNA13B")
                # print("CHATGPT")
            elif asst1==asst2:
                results.append("TIE")
                # print("TIE")
            else:
                results.append("VICUNA13B")
                # results.append("CHATGPT")
                # print("VICUNA13B")

    elif method == "compare_between_agent":

        for i in data:
            d=0
            q_num+=1
            print ("Question number:" + str(q_num))
            for e in i["evaluation"]:
                d+=1
                asst1 = 0
                asst2 = 0
                # Input string
                input_string = e["evaluation"]

                # Regular expression to extract the score number
                pattern1 = r'The score of Assistant 1: ([\d.]+)'
                pattern2 = r'The score of Assistant 2: ([\d.]+)'
                # Use re.search to find the match
                match1 = re.search(pattern1, input_string)
                match2 = re.search(pattern2, input_string)
                # Check if a match is found
                if match1:
                    # Extract the score number from the matched group
                    score_number = match1.group(1)
                    #print(e["evaluation"])
                    print("Assistant 1 Score Number:", score_number)
                    asst1=float(score_number)
                else:
                    pass
                    #print(e)
                    print("No score found for assistant 1.")
                # Check if a match is found
                if match2:
                    # Extract the score number from the matched group
                    score_number = match2.group(1)
                    #print(e["evaluation"])
                    print("Assistant 2 Score Number:", score_number)
                    asst2=float(score_number)
                else:
                    # pass
                    # print(e)
                    print("No score found for assistant 2.") 
                
                print("Round:", d)
                # if (asst1!=0): 
                # d==1, d==2 has no records 
                if d==1:
                        # print("asst1, asst2: " + str(asst1) +", "+ str(asst2)) 
                        if asst1>asst2:
                            agent_results.loc[('agent1', 'first')].results.append('A')
                        elif asst1==asst2:
                            agent_results.loc[('agent1', 'first')].results.append('TIE')
                        else:
                            agent_results.loc[('agent1', 'first')].results.append('B')
                elif d==2:
                        # print("asst1, asst2: " + str(asst1) +", "+ str(asst2)) 
                        if asst1>asst2:
                            agent_results.loc[('agent2', 'first')].results.append('A')
                        elif asst1==asst2:
                            agent_results.loc[('agent2', 'first')].results.append('TIE')
                        else:
                            agent_results.loc[('agent2', 'first')].results.append('B')
                elif d==3:
                        # print("asst1, asst2: " + str(asst1) +", "+ str(asst2)) 
                        if asst1>asst2:
                            agent_results.loc[('agent3', 'first')].results.append('A')
                        elif asst1==asst2:
                            agent_results.loc[('agent3', 'first')].results.append('TIE')
                        else:
                            agent_results.loc[('agent3', 'first')].results.append('B')



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--human_results_path", default="./eval_helper/review_gpt35_vicuna-13b_human.txt")
    parser.add_argument("--agent_results_path", default="./Results/1_oriReverse.json")
    parser.add_argument("--kappa_path", default="./Results/1_kappa_oriReverse.json")
    args = parser.parse_args()


    with open(args.human_results_path) as f:
        human_results = f.readlines()   # if it is text file
        human_results = [item.strip() for item in human_results]

    with open(args.agent_results_path,"r") as fp:
        data = json.load(fp)



    # Create empty dataframe with agent and run as multi-index
    agent_results = pd.DataFrame(columns=['results'], 
                                index=pd.MultiIndex.from_product([['agent1', 'agent2'], 
                                                                ['first', 'second', 'average', 'label']], names=['agent', 'run']))

    # Add empty lists as the column values  
    agent_results['results'] = agent_results.apply(lambda x: [], axis=1)

    print(agent_results)

    results = []
    q_num=0 


    get_calibration (method = "compare_between_agent")

    print(agent_results)
    # print(human_results)


    # kappa = cohen_kappa_score(human_results, results)
    kappa_AB = cohen_kappa_score(agent_results['results']['agent1']['first'], agent_results['results']['agent2']['first'])
    kappa_AC = cohen_kappa_score(agent_results['results']['agent1']['first'], agent_results['results']['agent3']['first'])
    kappa_BC = cohen_kappa_score(agent_results['results']['agent2']['first'], agent_results['results']['agent3']['first'])
    #print("Kappa:", str(kappa))

    with open(args.kappa_path, 'w') as f:
        # f.write(f'accuracy Score: {acc}\n')
        f.write(f'Kappa Score AB: {kappa_AB}\n')
        f.write(f'Kappa Score AC: {kappa_AC}\n')
        f.write(f'Kappa Score BC: {kappa_BC}\n')
        agent_results.to_string(f)
        agent_results.to_string(f)


    # from FleissKappaCalculation_mod import calculateFleissKappa 
    # import math
        
    # def test_KappaFleiss():
    #     k = calculateFleissKappa(df, ["A", "B"], 80, 5, 0) # df, categories, NSub/items/runs, nRatings/nRators, version
    #     assert math.isclose(0.210, k, rel_tol=1e-3), 'calculateFleissKappa doesn\'t calculate the right result'


    # test_KappaFleiss()




