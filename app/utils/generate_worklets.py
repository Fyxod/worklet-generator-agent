from langchain.prompts import ChatPromptTemplate
from app.llm import llm, llm2
from app.utils.llm_response_parser import extract_json_from_llm_response
from langchain.schema.messages import HumanMessage
from concurrent.futures import ThreadPoolExecutor
import asyncio
from app.llm import invoke_llm

def get_prompt_template_V2():
    return ChatPromptTemplate.from_template("""You are an expert in analyzing and generating structured worklet ideas. Your task is to generate **five new worklets** based on the provided examples.

### **Instructions:**
- Ensure that the new worklets are **unique yet thematically aligned** with the given worklets.
- **Follow the exact format** below for each new worklet.
- **Ensure ideas are innovative yet practically implementable.**
- **Exclude specific names of people, organizations, or brands.**

---

### ** Structure of Each Worklet Idea:**
1. **Title**: A concise and engaging title summarizing the worklet not more than 4-6 words.
2. **Problem Statement**: Clearly describe the problem this worklet aims to address. between 28-33 words
3. **Goal**: Define the objective and intended outcome. between 30 -35 words 
4. **Expectations**: Describe what participants are expected to do or accomplish.  between 38 to 45 words 
5. **Training/Prerequisite**: List any required knowledge, skills, or prior learning needed.
6. **Difficulty (1-10)**: Rate the complexity of this worklet on a scale from 1 (very easy) to 10 (very challenging).
7. **Reference Work**: Include at least one reference work, preferably an academic or research paper. If two strong references are available, include both

---

### ** Existing Worklets for Reference:**
{worklet_data}

---

### ** Additional Guidelines:**
**Ensure originality**—new worklets should be inspired by, but not directly derivative of, the provided examples.  
**Introduce fresh perspectives**—each worklet should offer a unique angle or approach.  
**Maintain structured clarity**—ideas should be easy to understand and apply.  
**Stick to the context**—avoid introducing unrelated topics. 
**Word Limit**- Strictly adhere to word limits to avoid formatting errors in PDF generation.   

Respond **strictly in JSON format** as shown below:

```json
{{
    "worklets": [
        {{
            "Title": "...",
            "Problem Statement": "... (28-33 words)",
            "Goal": "... (30-35 words)",
            "Expectations": "... (38-45 words)",
            "Training/Prerequisite": "...",
            "Difficulty": 5,
            "Reference Work": [
                                    {{
                                        "title": "..................",
                                        "link": "..................."
                                    }},
                                    {{
                                        "title": ".......................",
                                        "link": "........................."
                                    }}
                              ]
        }},
        {{
            "Title": "...",
            "Problem Statement": "... (28-33 words)",
            "Goal": "... (30-35 words)",
            "Expectations": "... (38-45 words)",
            "Training/Prerequisite": "...",
            "Difficulty": 3,
            "Reference Work":[
                                    {{
                                        "title": "..................",
                                        "link": "..................."
                                    }},
                                    {{
                                        "title": ".......................",
                                        "link": "........................."
                                    }}
                              ]
        }},
        {{
            "Title": "...",
            "Problem Statement": "... (28-33 words)",
            "Goal": "... (30-35 words)",
            "Expectations": "... (38-45 words)",
            "Training/Prerequisite": "...",
            "Difficulty": 8,
            "Reference Work": [
                                    {{
                                        "title": "..................",
                                        "link": "..................."
                                    }},
                                    {{
                                        "title": ".......................",
                                        "link": "........................."
                                    }}
                              ]
        {{
            "Title": "...",
            "Problem Statement": "... (28-33 words)",
            "Goal": "... (30-35 words)",
            "Expectations": "... (38-45 words)",
            "Training/Prerequisite": "...",
            "Difficulty": 6,
            "Reference Work": [
                                    {{
                                        "title": "..................",
                                        "link": "..................."
                                    }},
                                    {{
                                        "title": ".......................",
                                        "link": "........................."
                                    }}
                              ]
        }},
        {{
            "Title": "...",
            "Problem Statement": "... (28-33 words)",
            "Goal": "... (30-35 words)",
            "Expectations": "... (38-45 words)",
            "Training/Prerequisite": "...",
            "Difficulty": 9,
            "Reference Work": [
                                    {{
                                        "title": "..................",
                                        "link": "...................."
                                    }},
                                    {{
                                        "title": ".......................",
                                        "link": "........................."
                                    }}
                              ]
        }}
    ]
}}
Now, **generate 5 well-structured and distinct worklets** following these guidelines.
""")




async def generate_worklets(worklet_data, model):
    prompt_template = get_prompt_template_V2()  # Fetch the latest template dynamically
    prompt = prompt_template.format(worklet_data=worklet_data)
    generated_worklets = invoke_llm(prompt, model)

    extracted_worklets = extract_json_from_llm_response(generated_worklets)

    # Run refine_worklet in parallel using ThreadPoolExecutor
    # with ThreadPoolExecutor() as executor:
    #     loop = asyncio.get_running_loop()
    #     refined_worklets = await asyncio.gather(
    #         *[loop.run_in_executor(executor, refine_worklet, worklet)
    #           for worklet in extracted_worklets["worklets"]]
    #     )

    # extracted_worklets["worklets"] = refined_worklets
    return extracted_worklets

def refine_worklet(worklet_data):

    prompt = ChatPromptTemplate.from_template("""
    You are an expert in analyzing and generating structured worklet ideas. You will be provided with two worklet jsons. Your task is to compare both of them and return only "True" if they are similar and "False" if they are not similar.
    Worklet 1:
    {worklet_data_1}
    Worklet 2:
    {worklet_data_2}
    """)

    worklet_data_1 = worklet_data

    while True:
        worklet_data_2 = get_new_refined_worklet(worklet_data)
        check = llm2.invoke(prompt.format(worklet_data_1=worklet_data_1, worklet_data_2=worklet_data_2))
        # parsing the response to check if they are similar or not
        print(check.content)
        if check.content == "True":
            break
        else:
            worklet_data_1 = worklet_data_2

    return worklet_data_2


# test = {'worklets': [{'Title': 'Federated Learning Model Pruning', 'Problem Statement': 'Federated learning models often become large, hindering deployment on resource-constrained edge devices. Pruning techniques can reduce model size, but their application in federated settings is complex. ', 'Goal': 'To develop and evaluate federated learning algorithms that incorporate model pruning techniques to reduce model size while maintaining accuracy and improving communication efficiency, ensuring optimal edge deployment.', 'Expectations': 'Participants will implement federated averaging with pruning, evaluate performance on a benchmark dataset, analyze communication costs, and provide a report comparing different pruning strategies and their impacts.', 'Training/Prerequisite': 'Federated learning basics, model pruning techniques, PyTorch/TensorFlow, communication protocols.', 'Difficulty': 7, 'Reference Work': [{'title': 'Federated Learning: Challenges, Methods, and Future Directions', 'link': 'https://arxiv.org/abs/1912.04977'}, {'title': 'Pruning neural networks at scale', 'link': 'https://proceedings.neurips.cc/paper_files/paper/2018/file/54473917af4f6007cd6ddc7c29aa472c-Paper.pdf'}]}, {'Title': 'Synthetic Data Generation (Privacy)', 'Problem Statement': 'Generating realistic synthetic data that preserves privacy is challenging. Existing methods often fail to capture complex relationships or introduce unacceptable privacy risks which limits data utility.', 'Goal': 'To develop synthetic data generation techniques using differential privacy or similar privacy frameworks, ensuring the generated datasets are statistically similar to the original data but safeguard individual privacy.', 'Expectations': 'Participants will implement a synthetic data generator, evaluate its privacy guarantees, compare against existing methods, and report on the trade-off between data utility and privacy protection.', 'Training/Prerequisite': 'Differential privacy, generative models, Python, data analysis, statistical modeling.', 'Difficulty': 6, 'Reference Work': [{'title': 'The Algorithmic Foundations of Differential Privacy', 'link': 'https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf'}, {'title': 'Modeling Tabular data using Conditional GAN', 'link': 'https://arxiv.org/abs/2103.01950'}]}, {'Title': 'Explainable AI for Icon Recognition', 'Problem Statement': 'While icon recognition models achieve high accuracy, understanding their decision-making process remains a challenge. Lack of interpretability hinders trust and limits the ability to improve models.', 'Goal': 'To develop and apply explainable AI techniques to icon recognition models, providing insights into which features drive predictions and helping to identify and correct biases.', 'Expectations': "Participants will implement XAI methods (e.g., SHAP, LIME), apply them to an icon recognition model, visualize explanations, and report on the model's behavior and potential biases.", 'Training/Prerequisite': 'Icon recognition, convolutional neural networks, explainable AI techniques, Python, data visualization.', 'Difficulty': 7, 'Reference Work': [{'title': 'Explainable AI: Opening the Black Box', 'link': 'https://arxiv.org/abs/1811.04822'}, {'title': 'SHAP Values', 'link': 'https://arxiv.org/abs/1705.07874'}]}, {'Title': 'Adversarial Robustness Icon Detection', 'Problem Statement': 'Icon detection models are vulnerable to adversarial attacks. Small, imperceptible perturbations in input images can cause models to misclassify icons, leading to security vulnerabilities.', 'Goal': 'To develop robust icon detection models that are resistant to adversarial attacks by using adversarial training or defense mechanisms to enhance the reliability of these models.', 'Expectations': 'Participants will implement adversarial training, evaluate model robustness against common attacks, compare different defense strategies, and report on the trade-off between accuracy and robustness.', 'Training/Prerequisite': 'Icon detection, adversarial attacks, adversarial training, PyTorch/TensorFlow, image processing.', 'Difficulty': 8, 'Reference Work': [{'title': 'Explaining and Harnessing Adversarial Examples', 'link': 'https://arxiv.org/abs/1412.6572'}, {'title': 'Towards Deep Learning Models Resistant to Adversarial Attacks', 'link': 'https://arxiv.org/abs/1706.06083'}]}, {'Title': 'Cross-Lingual Hand Gesture Recognition', 'Problem Statement': 'Hand gesture recognition models are usually trained and tested on specific language and cultural contexts, limiting their effectiveness across diverse user populations who use varied gestures.', 'Goal': 'To develop a hand gesture recognition system that is robust across different languages and cultural backgrounds by adapting and generalizing models to handle the variation and nuances.', 'Expectations': 'Participants will collect/curate multilingual hand gesture datasets, train a cross-lingual model, evaluate performance on different languages, and report on adaptation strategies and cultural nuances.', 'Training/Prerequisite': 'Hand gesture recognition, transfer learning, multilingual data processing, Python, data augmentation.', 'Difficulty': 9, 'Reference Work': [{'title': 'Cross-Lingual Transfer Learning for Document Classification', 'link': 'https://aclanthology.org/D10-1091/'}, {'title': 'A Review of Hand Gesture Recognition Technologies and Applications', 'link': 'https://www.mdpi.com/1424-8220/21/2/651'}]}]}

def get_new_refined_worklet(worklet_data):
    
    prompt = ChatPromptTemplate.from_template("""
    You are an expert in analyzing and generating structured worklet ideas. Your task is to refine the provided worklet to make it better and more structured and engaging. Make sure it follows the word limits and the structure below.

    Worklet to be refined:
    {worklet_data}

    Structure of Each Worklet Idea
    1. Title: A concise and engaging title summarizing the worklet not more than 4-6 words.
    2. Problem Statement: Clearly describe the problem this worklet aims to address. between 28-33 words
    3. Goal: Define the objective and intended outcome. between 30 -35 words 
    4. Expectations: Describe what participants are expected to do or accomplish.  between 38 to 45 words 
    5. Training/Prerequisite: List any required knowledge, skills, or prior learning needed.
    6. Difficulty (1-10): Rate the complexity of this worklet on a scale from 1 (very easy) to 10 (very challenging).
    7. Reference Work: Include at least one reference work, preferably an academic or research paper. If two strong references are available, include both

    return the refined worklet in JSON format same as the provided one.
    """)

    refined_worklet = llm2.invoke(prompt.format(worklet_data=worklet_data))

    return extract_json_from_llm_response(refined_worklet.content)


# print(refine_worklet(test["worklets"][0]))