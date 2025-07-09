import subprocess
import os
import json
# import requests
from transformers import pipeline

DSK = "/Users/hsheta/Desktop/Mini vMac.app/Contents/mnvm_dat/disk2.dsk"



# def extract_input() -> str:
#     """"Extracts the input text from the Mini vMac Disk Image."""
#     # Mount the disk image
#     subprocess.run(["hmount", DSK])

#     # Copy input file from disk image to current dire
#     subprocess.run(["hcopy", "-m", "input.txt", "user_input.txt"])

#     # Unmount the disk image to avoid disk corruption
#     subprocess.run(["humount"])

#     # Read the extracted input file
#     with open("user_input.txt", "r", encoding="mac_roman") as f:
#         return f.read().strip()
    

def extract_input() -> str:
     # Read the extracted input file
    with open("/Users/hsheta/Desktop/Shared/input.txt", "r", encoding="mac_roman") as f:
        return f.read().strip()

def load_private_key() -> str:
    """Loads the HuggingFace private key from a file."""
    file_path = "_private/auth.json"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at {file_path}")
    
    with open(file_path) as f:
        data = json.load(f)

    return data.get("HUGGINGFACE_API_KEY", "")

def query_llm(prompt: str) -> str:
    """Queries the LLM with the given prompt."""
    pipe = pipeline("text-generation", model="microsoft/DialoGPT-small")

    messages = [{"role": "user",
                  "content": prompt}]
    response = pipe(messages, max_new_tokens=253, num_return_sequences=1)

    llm_message = response[0]['generated_text'][1]['content']
    print(f"LLM response: {llm_message}")

    return llm_message
   

    # url = "https://api-inference.huggingface.co/models/distilgpt2"
    # headers = {"Authorization": f"Bearer {api_key}"}
    # payload = {"inputs": prompt}

    # try:
    #     res = requests.post(url, headers=headers, json=payload)
    #     res.raise_for_status()  # Raise an error for bad responses

    # except requests.exceptions.RequestException as e:
    #     print(f"Error querying the LLM: {e}")
    #     return


    # output = res.json()
    # return output[0]['generated_text']

def write_output(response: str):
    """Writes the LLM response to the output file."""
    with open("/Users/hsheta/Desktop/Shared/out.txt", "w", encoding="mac_roman", newline="\r") as f:
        f.write(response)
    
    # subprocess.run(["hmount", DSK], check=True)
    # subprocess.run(["hcopy", "-m", "host_output.txt", "output.txt"], check=True)
    # subprocess.run(["humount"])


if __name__ == "__main__":
    # Extract input from the Mini vMac Disk Image
    user_prompt = extract_input()
    print(f"User prompt: {user_prompt}")

    # Query the LLM with the user prompt
    response = query_llm(user_prompt) 
    print(f"LLM response: {response}")

    write_output(response)


    # text = "I feel anxious.\r"

    # with open("out.txt", "w", encoding="mac_roman", newline="\r") as f:
    #     f.write(text)
