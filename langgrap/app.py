import os 
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from tools import CustomTools
from langgraph.prebuilt import ToolNode, tools_condition
import gradio as gr
from typing import Annotated


class AgentState(TypedDict):
    q: str
    queryCategory: Optional[str]  # football, search, general
    messages: Annotated[list[AnyMessage], add_messages]


# Initialize the LLM with tools
tools = [
    CustomTools.search, 
    CustomTools.matches
]
llm = ChatOpenAI(model="gpt-4")
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)


def assistant(state: AgentState):
    # System message
    textual_description_of_tool = """
    matches()->str: 
        Pulls Match Resources from footballdata.org 

    search(q:str)->str:
        Perform a search operation.
    """
    sys_msg = SystemMessage(content=f"You are a helpful assistant:\n{textual_description_of_tool}")
    return {
        "messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]
    }


# Build the graph
builder = StateGraph(AgentState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

react_graph = builder.compile()


### Gradio wrapper
chat_history = []

def chat_interface(message, history):
    # Convert history to messages
    messages = [HumanMessage(content=message)]
    for user, bot in history:
        messages.insert(0, HumanMessage(content=user))
        messages.insert(1, AIMessage(content=bot))

    result = react_graph.invoke({"messages": messages})
    final_msgs = result["messages"]

    # Get the latest assistant reply
    for m in reversed(final_msgs):
        if isinstance(m, AIMessage):
            return m.content

    return "No response from assistant."


### Launch Gradio
gr.ChatInterface(fn=chat_interface, type="messages").launch()
