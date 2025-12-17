import json
import pandas as pd
import datetime
import ssl
import certifi
import httpx
import random
from openai import OpenAI


# ✅ Set uthe number of replicates for the experimets
nReplicates = 10
nRuns = 32

# ✅ Set up secure HTTP client to fix SSL verification issues
ssl_context = ssl.create_default_context(cafile=certifi.where())
http_client = httpx.Client(verify=ssl_context)

# ✅ Initialize OpenAI client
client_OpenAI = OpenAI(
    api_key="",  # 🔁 Replace with your actual API key
    http_client=http_client
)

print("Starting GPT Query Script")
print(datetime.datetime.now())

# ✅ Load and shuffle instructions
input_file = f'instructions/instruction_dataset_n{nRuns}.json'
with open(input_file, 'r', encoding='utf-8') as f:
    tasks = json.load(f)

for ii in range(nReplicates):

    random.shuffle(tasks)  # ✅ Randomize submission order
    
    print("Instructions loaded and randomized")
    print(datetime.datetime.now())
    
    # ✅ Send each prompt to ChatGPT
    results = []
    
    for idx, task in enumerate(tasks):
        prompt = task.get("prompt", "")
        print(f"Sending task {idx + 1} to GPT...")
    
        try:
            response = client_OpenAI.responses.create(
                model = "gpt-5.1-chat-latest",
                reasoning = { "effort": "medium" },
                input = [
                    {"role": "user", "content": prompt}
                ]
            ) # Note the experiments were run on December 2, 2025
    
            result_text = response.output[1].content[0].text.strip()
            print(f"Task {idx + 1} completed.")
    
        except Exception as e:
            print(f"Error with task {idx + 1}: {e}")
            result_text = f"ERROR: {e}"
    
        results.append({
            "Question #": idx + 1,
            "RunSize": task.get("N"),
            "TaskID": task.get("ID"),
            "Prompt": prompt,
            "Resolution": task.get("resolution"),
            "WordLengthPattern": str(task.get("WordLengthPattern")),
            "ClearInteractions": task.get("clearIteractions"),
            "Response": result_text
        })
    
    # ✅ Save results to CSV
    df = pd.DataFrame(results)
    nRunsize = task.get("N")
    output_file = f"gpt_results/responses_gpt_n{nRunsize}_replicate{ii+1}.csv"
    df.to_csv(output_file, index=False)

print(f"✅ Responses saved to {output_file}")
