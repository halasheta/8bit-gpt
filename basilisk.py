import os
import time
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

SHARED_DSK = "/Users/hsheta/Desktop/Shared"


def extract_input(input_file) -> str:
    """Extracts the input text from the Basilisk Unix Root Directory.

    Args:
        input_file (str): Path to the input file in the shared disk.
    Returns:
        str: The extracted input message.
    """
    # Read the extracted input file
    with open(input_file, "r", encoding="mac_roman") as f:
        message = f.read().strip()

    # Delete file after reading to avoid re-reading
    os.remove(input_file)

    return message


# def query_llm(prompt: str) -> str:
#     """Queries the LLM with the given prompt."""
#     pipe = pipeline("text-generation", model="microsoft/DialoGPT-small")

#     messages = [{"role": "user","content": prompt}]

#     # Ensure the message is small enough for the C program buffer
#     response = pipe(messages, max_new_tokens=253, num_return_sequences=1)

#     llm_message = response[0]['generated_text'][1]['content']

#     return llm_message


def query_llm(generator, user_prompt: str, chat_history: list, max_new_tokens: int = 253) -> tuple:
    """"""
    # append prompt to chat history
    chat_history.append({"role": "user", "content": user_prompt})

    if len(chat_history) > 10:
        # trim the first two rounds of conversations
        chat_history = chat_history[4:]

    response = generator(
        chat_history,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.9,
        top_p=0.95,
    )
    print(response)
    llm_message = response[0]['generated_text'][1]['content']
    chat_history.append({'role': 'assistant', 'content': llm_message})


def write_output(response: str) -> None:
    """Writes the LLM response to the output file."""
    output_file = os.path.join(SHARED_DSK, "out.txt")
    with open(output_file, "w", encoding="mac_roman", newline="\r") as f:
        f.write(response)


if __name__ == "__main__":
    # Load model
    # model_path = "microsoft/phi-3-mini-4k-instruct"
    # text_pipeline = pipeline("text-generation",
    #                          model=model_path, trust_remote_code=True)
    # # tokenizer = AutoTokenizer.from_pretrained(model_path)
    # # model = AutoModelForCausalLM.from_pretrained(model_path)

    # # Initialize chat history with informal style priming
    # chat_history = [
    #     {"role": "user", "content": "From now on, talk casually — like you're vibing on Reddit. No stiff stuff."},
    #     {"role": "assistant", "content": "Aight, chill mode activated."}
    # ]

    # while True:
    #     input_file = os.path.join(SHARED_DSK, "input.txt")
    #     if os.path.exists(input_file):
    #         try:
    #             user_prompt = extract_input(input_file)
    #             print(f"User prompt: {user_prompt}")

    #             # Query the LLM with the user prompt
    #             response, chat_history = query_llm(
    #                 text_pipeline, user_prompt, chat_history)
    #             print(f"LLM response: {response}")

    #             write_output(response)
    #         except Exception as e:
    #             print(f"Error processing input: {e}")
    #     time.sleep(2)  # Wait 2 seconds before checking again
    from vec_inf import VecInfClient
    client = VecInfClient()
    response = client.launch_model("Meta-Llama-3.1-8B-Instruct")
    job_id = response.slurm_job_id
    status = client.get_status(job_id)
    if status.status == ModelStatus.READY:
        print(f"Model is ready at {status.base_url}")
    client.shutdown_model(job_id)
