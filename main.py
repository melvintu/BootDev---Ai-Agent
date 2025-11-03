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

    count = 0
    while count <= 5:
        try:
            print("This is the messages that are being sent to content", messages)
            content = generate_content(client, messages, verbose)

            if hasattr(content, "text"):
                print("content text found", content.text)
                #return content.text
                break

            if any("I want to call" in part.text for part in content.candidates[0].content.parts if hasattr(part, "text")):
                print("I want to call was used")
                candidate_parts = content.candidates[0].content.parts
                print("These are the candidate parts of the generated response", candidate_parts)
                messages.append(types.Content(role="user", parts=candidate_parts))

            count += 1
            print("No text found, i is incremented", count)

        except Exception as e:
            print(f"Error while generating content: {e}")
            break
    
    if count == 5:
        print("Max number of iterations reached")

def generate_content(client, messages, verbose):
    print("Generating content")

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
        return response

    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose) 
        try:
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            else: 
                print(function_call_result.parts[0].function_response.response["result"])
            #messages.append(types.Content(role="user", parts=[function_call_part]))
            messages.append(function_call_result)
        except Exception as e:
            print(f"Error calling function: {e}")
    
    return response
        

if __name__ == "__main__":
    main()
