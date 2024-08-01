from llamaapi import LlamaAPI
import json
import os
import time

# Replace 'Your_API_Token' with your actual API token
llama = LlamaAPI('LL-69WCQLo6Rh6ucWGD5jMhWcxeMJZsKikJWlBUfzVys7K8KJw9gKLbokgLxn7zudlp')


categories = {
    "literature": "Lit",
    "medical-articles": "Med",
    "moviescripts": "Mov",
    "news-press-releases": "NPR",
}

def iterate_category(category_name, category_prefix, error_log_path):
    reqMainDesc = """
    for every sentence(lit-x) that I will give you, I need to help me to return the SVO as Spacy do for this sentence, like this structure:
    {
    "lit-1": {
          "SVO_relationships": [
            {
              "subject": "the fake, country-wet freshness",
              "verb": "evaporated",
              "stem": "evaporate",
              "object": "like the tail end of a sweet dream"
            },
            {
              "subject": "the hot streets",
              "verb": "wavered",
              "stem": "waver",
              "object": "in the sun"
            },
            {
              "subject": "I",
              "verb": "kept hearing",
              "stem": "hear",
              "object": "about the Rosenbergs over the radio and at the office"
            },
            {
              "subject": "I",
              "verb": "couldn't get",
              "stem": "get",
              "object": "them out of my mind"
            }
          ],
          "total_SVOs": 4
      },

      "lit-2": {...
    }
    are you ready?
    """
    folder_path = f'E:/workspaces/PythonWS/Selenium-python/chatGPT/myDataset/{category_name}'
    files = sorted(os.listdir(folder_path))[51:100]
    all_data = {}
    errors = []
    output_json_temp = f'E:/workspaces/PythonWS/Selenium-python/chatGPT/myResult/Using_LLAMA3/{category_name}.json'
    os.makedirs(os.path.dirname(output_json_temp), exist_ok=True)
    with open(output_json_temp, 'w', encoding='utf-8') as json_file:
        for idx, file_name in enumerate(files, start=1):
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    req = text
                    time.sleep(10)

                    # API Request JSON Cell
                    api_request_json = {"model": "llama3-70b",
                        "messages": [
                            {"role": "system","content": reqMainDesc},
                            {"role": "user", "content": req},
                        ]
                    }

                    # Make your request and handle the response
                    response = llama.run(api_request_json)
                    print(json.dumps(response.json(), indent=2))
                    svos = response
                    if svos:
                        all_data[f"{category_prefix}-{idx}"] = {
                            "SVO_relationships": svos,
                            "total_SVOs": len(svos)
                        }
                    else:
                        errors.append(f"No SVOs found in file {file_name} ({category_prefix}-{idx})")
                    print(all_data)
                    json.dump(all_data, json_file, indent=4, ensure_ascii=False)
            except Exception as e:
                errors.append(f"Error processing file {file_name} ({category_prefix}-{idx}): {str(e)}")
    output_json_path = f'E:/workspaces/PythonWS/Selenium-python/chatGPT/myResult/Using_LLAMA3/{category_name}.json'
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, 'w', encoding='utf-8') as json_file2:
        json.dump(all_data, json_file2, indent=4, ensure_ascii=False)
    print(f"SVOs for {category_name} saved to {output_json_path}")

    # Write errors to log file
    with open(error_log_path, 'a', encoding='utf-8') as log_file:
        for error in errors:
            log_file.write(error + '\n')
    print(f"Errors for {category_name} logged to {error_log_path}")

# Error log path
error_log_path = 'E:/workspaces/PythonWS/Selenium-python/chatGPT/myDataset/myResult/Using_LLAMA3/error_log.txt'
os.makedirs(os.path.dirname(error_log_path), exist_ok=True)

if __name__ == "__main__":

    try:
        while True:

            # Process each category
            for category, prefix in categories.items():
                print(category)
                iterate_category(category, prefix, error_log_path)

    except KeyboardInterrupt:
        print("KeyboardInterrupt detected, exiting...")




