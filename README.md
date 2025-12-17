# LLMforDOE

R and Python code to accompany Vazquez, A. R. and Rother, K. M. (2025). "A systematic assessment of Large Language Models for constructing two-level fractional factorial designs." Submitted to *Quality Engineering*.

This github repository contains the following sections:

A. SCRIPT FILES
B. UTILITY CODE 
D. DATA FOLDERS


## A. SCRIPT FILES.

Use these to construct the design construction tasks and process them using GPT or Gemini models.

- `Generate_Construction_Tasks.R`: R code to generate design construction tasks using Prompt 2. The tasks are saved into a folder called **instructions**.

- `Process_Task_using_Gemini.py`: Python code to submit the tests to the Gemini model. A private API key from Google is needed to submit queries to the LLM. For more information, please visit https://ai.google.dev/gemini-api/docs/quickstart. The results from the queries are saved into a folder called **gemini_results**.

- `Process_Task_using_GPT.py`: Python code to submit the tests to the Gemini model. A private API key from OpenAI is needed to submit queries to the LLM. For more information, please visit https://platform.openai.com/docs/quickstart. The results from the queries are saved into a folder called **gpt_results**.


- `Evaluate_Designs.py`: Python code to evaluate the designs constructed using an LLM. The results from the evaluation are saved into a folder called **evaluation_results**.


## B. UTILITY CODE.

It includes files used to evaluate and process the designs and tasks.

-  `DoE_functions.R`: Set of R functions to evaluate two-level fractional factorial designs.

-  `FrF2.py`: Set of Python functions to evaluate two-level fractional factorial designs.



## C. DATA FOLDERS.

- **instruction**: Contains the JSON files with the design construction tasks for the LLMs.

- **gemini_results**: Contains the CSV files with the output of the Gemini model to the design construction tasks. 

- **gpt_results**: Contains the CSV files with the output of the GPT model to the design construction tasks. 

- **evaluation_results**: Contains Excel files with the evaluation of the designs in terms of resolution and moment aberration. 