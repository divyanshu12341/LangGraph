import os 
from typing import TypedDict

# Let's create state first 
class pipelinestate(TypedDict):
    raw_input:str
    edited_text:str
    script_text:str
    final_output:str

from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
llm = ChatGroq(model = "openai/gpt-oss-120b",temperature = 0.7)
def editor_node(state:pipelinestate)->dict:
    """
    Stage-1: Cleans up grammar,removes typos and refine the tone
    """
    prompt = (
        "You are an expert copyeditor.Cleans up the following raw text",
        "Fix any grammatical errors,spelling mistakes and smooths out the transition flow",
        "while keeping core message intact,return only edited text /n /n"
        f"Text:\n{state['raw_input']}"
    )
    response  = llm.invoke(prompt)
    return {"edited_text":response.text.strip()}

def scriptwriter_node(state:pipelinestate)->dict:
    """
    Stage-2: Format the clean text into an engaging video 
    script style 
    """
    print("\n [Stage 2] Executing Scriptwriter node ----")
    prompt = (
        "You are a charismatic youtube content creator.Take this edited text and transform it into highly engaging,punchy,conversational video script hook.Make it sound like a real person speaking passionately.Return only the script content; \n \n"
        f"Edited text: \n{state['edited_text']}"
    )
    response = llm.invoke(prompt)
    return {"script_text":response.content.strip()}

def translator_node(state:pipelinestate)->dict:
    """
    Stage-3: Translate the text into natural flowing hinglish   
    """
    print("\n [Stage 2] Executing Hinglish translator node ----")
    prompt = (
        "You are an expert content localizer for indian market.take the following script and convert it into natural,flowing hinglish.Do not simply translate it sentence-by-sentence or repeat information.Alternating between comfortable english and hindi phrases.Just like an intellectual tech educator would speak naturally on a live stream.Keep the energy high.Return only the final hinglish text; \n \n"
        f"Edited text: \n{state['script_text']}"
    )
    response = llm.invoke(prompt)
    return {"final_output":response.content.strip()}

# now your states and nodes are ready and now it is time to create a graph and for creating the graph,you have to connect these nodes and for that you have to use the edges.
# edges are very important to create workflows 
from langgraph.graph import StateGraph,START,END

# Create a graph
graph = StateGraph(pipelinestate)

# add nodes in our graph
graph.add_node("editor",editor_node)
graph.add_node("scriptwriter",scriptwriter_node)
graph.add_node("translator",translator_node)


# add edges (sequential(one after another))
graph.add_edge(START,"editor")
graph.add_edge("editor","scriptwriter")
graph.add_edge("scriptwriter","translator")
graph.add_edge("translator",END)

# COMPILE THE GRAPH 
app = graph.compile()
result = app.invoke({
     "raw_input":"Success comes from consistency.Every expert was once a beginner.Small steps lead to big achievements.Keep learning and keep growing."
})
print("RAW RESULT ARE \n \n")
print(result['final_output'])