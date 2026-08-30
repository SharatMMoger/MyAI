import file_search
import file_tools
import calculator_ai
import conversation_memory
import nlp_parser
import dispatcher
import context_state
from tasks.calculator_task import run as calculator_task
from tasks.summary_task import run as summary_task
dispatcher.register("calculator", calculator_task)
#dispatcher.register("summarize", summary_task)

def execute(plan, question):

    #print("EXECUTOR:", plan)

    parsed = nlp_parser.parse(question)

    for step in plan:
        #print("Running:", step)
        result = dispatcher.run(step, question)
        if result:
            return result

        # -----------------------
        # Search File
        # -----------------------

        if step == "search_file":

            if parsed and parsed.get("object"):

                keyword = parsed["object"]

                results = file_search.search_file(keyword)

                if not results:
                    return "No matching file found."
                results = file_search.search_file(keyword)
                if not results:
                    return "No matching file found."
                found_file = results

        # -----------------------
        # Read File
        # -----------------------

        elif step == "read_file":
            if parsed and parsed.get("object"):
                results = file_search.search_file(parsed["object"])
                if results:
                    filename = results[0]
                    context_state.set_value("last_file", filename)
                    return file_tools.read_file(filename)
                return "No matching file found."

        # -----------------------
        # Memory
        # -----------------------

        elif step == "calculator":

            return calculator_task(question)
        
        # -----------------------
        # Summary
        # -----------------------

        #elif step == "summarize":
            if parsed and parsed.get("object"):
                results = file_search.search_file(parsed["object"])
                if results:
                    filename = results[0]
                    text = file_tools.read_file(filename)
                    return summary_task(text)
                return "No matching file found."
    
    return None