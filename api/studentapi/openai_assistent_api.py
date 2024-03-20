
import os
import json
import yaml
import time
from dotenv import load_dotenv
from utils import read_all_students, read_students, create_students, update_students, delete_students
from db import Session, engine, Student

# A Class to Manage All Open API Assistant Calls and Functions
from openai.types.beta.threads import Run
from openai.types.beta.thread import Thread
# from openai.types.beta.assistant_create_params import Tool
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()

# API_KEY = os.getenv("OPENAI_API_KEY")
# OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
# print(OPENAI_API_KEY)

# print("read_all_students",read_all_students())             #pass the image url

API_KEY = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=API_KEY)
# Map available functions
available_functions = {
    "read_all_students_data": read_all_students,
    "read_student_by_id": read_students,
    "create_new_students": create_students,
    # "update_student": update_students,
    "delete_student": delete_students
}

from pathlib import Path

config_path = 'config.yaml'

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

# Extracting information from the config
bot_instructions = config['bot_instructions']
tools = config['tools']

def student_to_dict(student):
    return {
        "id": student.id,
        "name": student.name,
        "age": student.age,
        "grade": student.grade
    }

class StudentAssistantManager:
    def __init__(self, model: str = "gpt-3.5-turbo-1106"):
        self.client = OpenAI()
        self.model = model
        self.assistant = None
        self.thread = None
        self.run = None

    def create_assistant(self, name: str, instructions: str, tools) -> None:
        self.assistant = self.client.beta.assistants.create(
            name=name,
            instructions=instructions,
            tools=tools,
            model=self.model
        )

    def create_thread(self) -> Thread:
        self.thread = self.client.beta.threads.create()
        return self.thread

    def add_message_to_thread(self, role: str, content: str) -> None:
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role=role,
            content=content
        )

    def run_assistant(self, instructions: str) -> Run:
        self.run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions=instructions
        )
        return self.run

    def wait_for_completion(self, run: Run, thread: Thread) -> Run:

        while run.status in ["in_progress", "queued"]:
            run_status = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=self.run.id
            )
            print(f"Run is {run.status}. Waiting...")
            time.sleep(3)  # Wait for 3 seconds before checking again

            if run_status.status == 'completed':
                processed_response = self.process_messages()
                return processed_response
                # break
            elif run_status.status == 'requires_action':
                print("Function Calling ...")
                self.call_required_functions(run_status.required_action.submit_tool_outputs.model_dump())
            elif run.status == "failed":
                print("Run failed.")
                break
            else:
                print(f"Waiting for the Assistant to process...: {run.status}")

    def process_messages(self):
        messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
        return messages

    def call_required_functions(self, required_actions: dict):
        tool_outputs = []

        for action in required_actions["tool_calls"]:
            function_name = action['function']['name']
            arguments = json.loads(action['function']['arguments'])
            print('function_name', function_name)
            print('function_arguments', arguments)

            if function_name in available_functions:
                function_to_call = available_functions[function_name]
                output = function_to_call(**arguments)

                # Check if output is an instance of Student and convert to dict if so
                if isinstance(output, Student):
                    output = student_to_dict(output)
                elif isinstance(output, list) and all(isinstance(item, Student) for item in output):
                    output = [student_to_dict(student) for student in output]

                # Ensure output is serializable to JSON
                output = json.dumps(output, default=str)  # Use default=str to handle any other non-serializable types

                tool_outputs.append({
                    "tool_call_id": action['id'],
                    "output": output,  # This is now ensured to be a string
                })

            else:
                raise ValueError(f"Unknown function: {function_name}")

        print("Submitting outputs back to the Assistant...")
        self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=self.thread.id,
            run_id=self.run.id,
            tool_outputs=tool_outputs
        )

def format_messages_to_dict(messages) -> dict:
    formatted_messages = {"messages": []}

    for message in messages.data:
        role_label = "User" if message.role == "user" else "Assistant"
        message_contents = []
        
        for content in message.content:
            if content.type == "text":
                message_content = content.text.value
                message_contents.append({"role": role_label, "content": message_content})
                
        formatted_messages["messages"].append(message_contents)
        
    return formatted_messages

def studentAssistant(prompt: str):
    fmp_analyst = StudentAssistantManager()

    fmp_analyst.create_assistant(
        name="StudentAssistant",
        instructions=bot_instructions,
        tools=tools
    )

    fmp_analyst.create_thread()

    fmp_analyst.add_message_to_thread(
        role="user",
        content=prompt
    )

    run = fmp_analyst.run_assistant(
        instructions=bot_instructions
    )

    final_res = fmp_analyst.wait_for_completion(
        run=run,
        thread=fmp_analyst.thread
    )

    response = format_messages_to_dict(final_res)

    return response
    
# response1 = studentAssistant("""
# list the all student in db
# """)