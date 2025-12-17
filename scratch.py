response = client_OpenAI.responses.create(
                model = "gpt-5.1-chat-latest",
                reasoning = { "effort": "medium" },
                input = [
                    {"role": "user", "content": prompt}
                ]
            )

result_text = response.output[1].content[0].text
response.output.


response = client_Gemini.models.generate_content(
    model="gemini-2.5-flash",
    contents = prompt,
        config=types.GenerateContentConfig(
        #thinking_config=types.ThinkingConfig(thinking_budget=1024)
        # Turn off thinking:
        # thinking_config=types.ThinkingConfig(thinking_budget=0)
        # Turn on dynamic thinking:
        thinking_config=types.ThinkingConfig(thinking_budget=-1)
    )
)

response.candidates[0].content.parts[0].text.strip()


df_list[ii] = pd.read_csv(f"gpt_results/responses_gpt_n{nRunsize}_replicate{ii+1}.csv")

# Generate dated filename
filename = f"numpy_results/parsed_responses_n{nRunsize}.npy"

df[ii]['Response'] = df[ii]['Response'].apply(enforce_csv_block)

# Apply parser to each response
df[ii]['ParsedResponse'] = df[ii]['Response'].apply(parse_embedded_csv)



ii = 2
df = pd.read_csv(f"gpt_results/responses_gpt_n{nRunsize}_replicate{ii+1}.csv")

df['Response'] = df['Response'].apply(enforce_csv_block)

# Apply parser to each response
df['ParsedResponse'] = df['Response'].apply(parse_embedded_csv)

# Filter valid arrays
valid_arrays = df['ParsedResponse'].dropna().to_list()
invalid_count = len(df) - len(valid_arrays)

for i, arr in enumerate(valid_arrays):
    valid_numpy_array[i] = arr


df = pd.read_csv(f"{llm}_results/responses_{llm}_n{nRunsize}_replicate{ii+1}.csv")
df["TaskID"]

for ii in range(11, 12):
  print(ii)
