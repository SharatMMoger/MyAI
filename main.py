import dispatcher
from tasks import (
    calculator_task_v2,
    file_reading_task,
    summarize_task_v2,
    ask_task_v2,
    memory_task_v2,
    compare_task,
    progress_task,
    nl_command_task,
    llm_fallback_task,
    goal_task
)

# Register all tasks — ORDER MATTERS
# goal must be FIRST (its text contains other commands), llm_fallback must be LAST
dispatcher.register('goal', goal_task.can_handle, goal_task.run)
dispatcher.register('calculator', calculator_task_v2.can_handle, calculator_task_v2.run, verify=calculator_task_v2.verify)
dispatcher.register('file_reading', file_reading_task.can_handle, file_reading_task.run)
dispatcher.register('summarize', summarize_task_v2.can_handle, summarize_task_v2.run)
dispatcher.register('ask', ask_task_v2.can_handle, ask_task_v2.run)
dispatcher.register('memory', memory_task_v2.can_handle, memory_task_v2.run)
dispatcher.register('compare', compare_task.can_handle, compare_task.run)
dispatcher.register('progress', progress_task.can_handle, progress_task.run)
dispatcher.register('nl_command', nl_command_task.can_handle, nl_command_task.run)
dispatcher.register('llm_fallback', llm_fallback_task.can_handle, llm_fallback_task.run)

print("Welcome to MyAI!")
print("Type 'exit' to quit.")

while True:
    question = input("Ask me something: ")

    if not question.strip():
        continue

    if question.lower() == "exit":
        print("Goodbye!")
        break

    response = dispatcher.dispatch(question)
    print("MyAI:", response if response else "Sorry, I couldn't process that.")