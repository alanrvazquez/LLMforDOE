import json
import pandas as pd
import datetime
import ssl
import certifi
import httpx
import random
from google import genai
from google.genai import types

# ✅ Set uthe number of replicates for the experimets
nReplicates = 12
nRuns = 32

# ✅ Set up secure HTTP client to fix SSL verification issues
#ssl_context = ssl.create_default_context(cafile=certifi.where())
#http_client = httpx.Client(verify=ssl_context)

# ✅ Initialize Gemini client
client_Gemini = genai.Client(api_key="")  

print("Starting Gemini Query Script")
print(datetime.datetime.now())

# ✅ Load and shuffle instructions
input_file = 'instructions/instruction_dataset_n' + str(nRuns) + '.json'
with open(input_file, 'r', encoding='utf-8') as f:
    tasks = json.load(f)

for ii in range(11,nReplicates):

    random.shuffle(tasks)  # ✅ Randomize submission order
    
    print("Instructions loaded and randomized")
    print(datetime.datetime.now())
    
    # ✅ Send each prompt to ChatGPT
    results = []
    
    for idx, task in enumerate(tasks):
        prompt = task.get("prompt", "")
        print(f"Sending task {idx + 1} to Gemini...")
    
        try:
            response = client_Gemini.models.generate_content(
                model="gemini-2.5-flash",
                contents = prompt,
                config = types.GenerateContentConfig(
                        # Turn on dynamic thinking:
                        thinking_config=types.ThinkingConfig(thinking_budget=-1)
                        )
            )
    
            result_text = response.candidates[0].content.parts[0].text.strip()
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
    output_file = f"gemini_results/responses_gemini_n{nRunsize}_replicate{ii+1}.csv"
    df.to_csv(output_file, index=False)

print(f"✅ Responses saved to {output_file}")
