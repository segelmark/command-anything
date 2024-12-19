#!/usr/bin/env python3

import argparse
import sys
import time
import threading
import itertools
import asyncio
from pydantic import BaseModel, Field
from typing import List
from openai import AsyncOpenAI

class LoadingAnimation:
    def __init__(self):
        self.spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.busy = False
        self.thread = None
        self.current_status = ""

    def animate(self):
        while self.busy:
            sys.stdout.write(f'\r{next(self.spinner)} {self.current_status}')
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r' + ' ' * (len(self.current_status) + 2) + '\r')
        sys.stdout.flush()

    def start(self, status):
        self.current_status = status
        self.busy = True
        self.thread = threading.Thread(target=self.animate)
        self.thread.start()

    def stop(self):
        self.busy = False
        if self.thread:
            self.thread.join()

async def main():
    parser = argparse.ArgumentParser(description='Generate, preview, and optionally execute a script from an LLM.')
    parser.add_argument('prompt', nargs='*', help='The prompt to send to the LLM.')
    parser.add_argument('-m', '--model', default='gpt-4o', help='The model to use.')
    parser.add_argument('-p', '--parameters', nargs='*', help='Additional parameters for the prompt.')
    parser.add_argument('-l', '--language', default='python', help='Programming language of the script.')
    args = parser.parse_args()

    loading = LoadingAnimation()
    client = AsyncOpenAI()

    prompt_text = ' '.join(args.prompt)
    if args.parameters:
        prompt_text += ' ' + ' '.join(args.parameters)

    # Define the Pydantic model for the structured response
    class ScriptOutput(BaseModel):
        reasoning: str = Field(..., description="Explanation of how the script works.")
        script: str = Field(..., description=f"The {args.language} script code.")

    prompt_with_instructions = f"Write a {args.language} script that does the following:\n\n{prompt_text}\n\n" \
                               f"Provide a brief reasoning and the script in JSON format matching the specified schema."

    try:
        # Only show animation while waiting for the API response
        loading.start("Waiting for LLM response...")
        
        completion = await client.beta.chat.completions.parse(
            model=args.model,
            messages=[
                {'role': 'user', 'content': prompt_with_instructions}
            ],
            response_format=ScriptOutput,
            temperature=0,
        )
        
        loading.stop()
        
    except Exception as e:
        loading.stop()
        print(f"\nError communicating with OpenAI API: {e}")
        sys.exit(1)

    # Extract the assistant's response
    message = completion.choices[0].message
    if hasattr(message, 'parsed'):
        output = message.parsed
        reasoning = output.reasoning
        script = output.script
    elif hasattr(message, 'refusal'):
        print("\nThe assistant refused to provide a script.")
        sys.exit(1)
    else:
        print("\nError: No parsed response received.")
        sys.exit(1)

    print('\nReasoning:\n')
    print(reasoning)
    print('\nGenerated Script:\n')
    print(script)

    print('\nDo you want to execute this script? (y/n)')
    choice = input().lower()
    if choice == 'yes' or choice == 'y':
        if args.language.lower() == 'python':
            try:
                loading.start("Executing script")
                exec_globals = {}
                exec(script, exec_globals)
                loading.stop()
            except Exception as e:
                loading.stop()
                print(f"\nAn error occurred while executing the script: {e}")
        else:
            print('\nAutomatic execution is only supported for Python scripts.')
    else:
        print('\nExecution cancelled.')

if __name__ == '__main__':
    asyncio.run(main())