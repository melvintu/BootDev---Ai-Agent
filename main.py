import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import available_functions
from functions.call_function import call_function
from prompts import system_prompt

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args= []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python. main.py "your promprt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    generate_content(client, messages, verbose)

def generate_content(client, messages, verbose):

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],system_instruction=system_prompt
            )
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose) 
        try:
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            else: 
                print(function_call_result.parts[0].function_response.response["result"])
        except Exception as e:
            print(f"Error calling function: {e}")
        

if __name__ == "__main__":
    main()
