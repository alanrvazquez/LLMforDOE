# LLMforDOE

[![DOI](https://zenodo.org/badge/1091876126.svg)](https://doi.org/10.5281/zenodo.17958795)

R and Python code to accompany Vazquez, A. R. and Rother, K. M. (2025). "A systematic assessment of Large Language Models for constructing two-level fractional factorial designs." Submitted to *Quality Engineering*.

## A. SCRIPT FILES

Use these to generate the design construction tasks, process them using GPT or Gemini models, adn evaluate the resulting designs.

- `Generate_Construction_Tasks.R`: R code to generate design construction tasks using Prompt 2. The tasks are saved into a folder called **instructions**.

- `Process_Task_using_Gemini.py`: Python code to submit the tests to the Gemini model. A private API key from Google is needed to submit queries to the LLM. For more information, please visit https://ai.google.dev/gemini-api/docs/quickstart. The results from the queries are saved into a folder called **gemini_results**.

- `Process_Task_using_GPT.py`: Python code to submit the tests to the Gemini model. A private API key from OpenAI is needed to submit queries to the LLM. For more information, please visit https://platform.openai.com/docs/quickstart. The results from the queries are saved into a folder called **gpt_results**.


- `Evaluate_Designs.py`: Python code to evaluate the designs constructed using an LLM. The results from the evaluation are saved into a folder called **evaluation_results**.


## B. UTILITY CODE

It includes files used to evaluate and process the designs and tasks.

-  `DoE_functions.R`: Set of R functions to evaluate two-level fractional factorial designs.

-  `FrF2.py`: Set of Python functions to evaluate two-level fractional factorial designs. The file also contains functions to turn the output of an LLM into numpy arrays.



## C. DATA FOLDERS

- **instruction**: Contains the JSON files with the design construction tasks for the LLMs.

- **gemini_results**: Contains the CSV files with the output of the Gemini model to the design construction tasks. 

- **gpt_results**: Contains the CSV files with the output of the GPT model to the design construction tasks. 

- **evaluation_results**: Contains Excel files with the evaluation of the designs in terms of resolution and moment aberration. 