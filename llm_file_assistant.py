import json
from openai import OpenAI
from fs_tools import read_file, list_files, write_file, search_in_file

# Map tool names (as strings) to the actual Python functions
AVAILABLE_TOOLS = {
    "read_file": read_file,
    "list_files": list_files,
    "write_file": write_file,
    "search_in_file": search_in_file,
}


def run_assistant(user_query: str, client: OpenAI, tools_schema: list,
                   model: str = "openai/gpt-4o-mini", max_steps: int = 5):
    """
    Send a user query to the LLM, allowing it to call tools across multiple
    steps until it has enough information to produce a final answer.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant that manages resume files using the available tools. Use tools as many times as needed, step by step, before giving your final answer."},
        {"role": "user", "content": user_query}
    ]

    for step in range(max_steps):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools_schema,
        )

        response_message = response.choices[0].message
        messages.append(response_message)

        tool_calls = response_message.tool_calls

        if not tool_calls:
            return response_message.content

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"[Step {step + 1}] Tool Call: {function_name}({function_args})")

            if function_name in AVAILABLE_TOOLS:
                result = AVAILABLE_TOOLS[function_name](**function_args)
            else:
                result = {"error": f"Unknown tool: {function_name}"}

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

    return "Max steps reached without a final answer."
