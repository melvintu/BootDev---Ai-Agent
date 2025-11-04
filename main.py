import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import available_functions, call_function
from prompts import system_prompt
from config import MAX_ITERS

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

    count = 0
    while True:
        count += 1
        if count > MAX_ITERS:
            print(f"Maximum iterations {MAX_ITERS} reached")
            sys.exit(1)

        try:
            content = generate_content(client, messages, verbose)
            if hasattr(content, "text"):
                print("==================")
                print("FINAL RESPONSE:")
                print(content.text)
                print("==================")
                break
        except Exception as e:
            print(f"Error while generating content: {e}")

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

    if not getattr(response, "function_calls", None):
        return response

    for part in response.candidates[0].content.parts:
        if hasattr(part, "text") and part.text and ("I will" in part.text or "I'll" in part.text):
            messages.append(types.Content(role="user", parts=[part]))
            break

    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose) 
        try:
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(function_call_result)
        except Exception as e:
            print(f"Error calling function: {e}")

if __name__ == "__main__":
    main()
