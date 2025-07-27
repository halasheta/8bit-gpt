import os
import time
from typing import List, Tuple
from openai import OpenAI
import re
import logging
import argparse


# The shared disk by the emulator and this program
SHARED_DSK = "/path/to/Shared"


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

    logging.debug(f"User prompt [{len(message)}]: {message}")
    return message


def query_llm(client: OpenAI, user_prompt: str, chat_history: List[dict], max_new_tokens: int = 150) -> Tuple[str, List[dict]]:
    """Queries the LLM inference client using the user prompt and previous chat history.

    Args:
        client (OpenAI): OpenAI-compatible client server.
        user_prompt (str): The user input extracted from the emulator.
        chat_history (List[dict]): The chat history betweent the user and assistant.
        max_new_tokens (int): The maximum number of tokens to generate using the client.

    Returns:
        Tuple[str, List[dict]]: A tuple of the output LLM message and the updated chat history.
    """
    # Append prompt to chat history
    chat_history.append({"role": "user", "content": user_prompt})

    curr_history = chat_history
    if len(curr_history) > 10:
        # Trim the first two rounds of conversations
        curr_history = chat_history[:2] + chat_history[-5:]
        logging.debug(curr_history)

    # Send prompt to LLM
    response = client.chat.completions.create(
        model="Llama-2-13b-chat-hf",
        temperature=0.8,
        max_tokens=max_new_tokens,
        messages=curr_history,
        stop=["\nUser:", "\n"])

    # Ensure there are no unicode characters
    llm_message = response.choices[-1].message.content.encode(
        'ascii', 'ignore')
    llm_message = llm_message.strip().decode('ascii')

    logging.debug(f"LLM response [{len(llm_message)}]: {llm_message}")
    curr_history.append({'role': 'assistant', 'content': llm_message})

    return llm_message, curr_history


def write_output(response: str,) -> None:
    """Writes the LLM response to the output file.

    Args:
        response (str): The LLM output response.
    """
    output_file = os.path.join(SHARED_DSK, "out.txt")

    # Split messages based on punctuation
    messages = re.findall(r'.*?(?:\.{3}|[?.])', response)

    # Write to file in Mac Roman encoding
    with open(output_file, "w", encoding="mac_roman", newline="\r") as f:
        f.writelines([m.strip() + '\r' for m in messages])


def main():
    """Main function to run the program."""
    # Connect to model inference server
    # This URL is obtained by creating an SSH tunnel with the vec-inf job instance
    client = OpenAI(base_url="http://localhost:8080/v1", api_key="EMPTY")
    logging.debug('Connected to inference server')

    # Initialize chat history with informal style priming
    chat_history = [
        {
            "role": "user",
            "content": "From now on, talk casually in lowercase like you're vibing. Keep your messages short (1-2 sentences MAXIMUM) and talk like I'm a friendly stranger you're getting to know."
        },
        {
            "role": "assistant",
            "content": "Aight, chill mode activated."
        },
    ]

    # Main read write loop with the emulator input
    while True:
        input_file = os.path.join(SHARED_DSK, "input.txt")
        if os.path.exists(input_file):
            try:
                user_prompt = extract_input(input_file)

                # Query the LLM with the user prompt
                response, chat_history = query_llm(
                    client, user_prompt, chat_history)

                write_output(response)
            except Exception as e:
                print(f"Error processing input: {e}")
        # Wait before checking again
        time.sleep(1)


if __name__ == "__main__":
    # Intialize parser and parse args
    parser = argparse.ArgumentParser(prog='8-bit-gpt')
    parser.add_argument('-d', '--debug', action='store_true')

    # Set debug mode based on user input
    args = parser.parse_args()
    logging.getLogger().setLevel(logging.DEBUG if args.debug else logging.INFO)

    main()
