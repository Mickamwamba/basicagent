import os
from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import FunctionAgent
import asyncio
from tools import CustomTools
import gradio as gr

class BasicLammaAgent: 
    def __init__(self):

        api_key = os.getenv("OPEN_AI_KEY")
        self.llm = OpenAI(model="gpt-4o", api_key=api_key)
        football_tool = CustomTools.matches

        self.agent = FunctionAgent(
            llm=self.llm, 
            tools=[football_tool], 
            system_prompt="You are a general agent, helping to answer general questions."
        )

    async def __call__(self, q: str):
        response = await self.agent.run(user_msg=q)

        # Extract final output message from AgentOutput
        if hasattr(response, "final_output") and hasattr(response.final_output, "content"):
            return response.final_output.content
        
        # Fallbacks for unexpected formats
        if isinstance(response, str):
            return response

        return str(response)



# Instantiate once and reuse
agent_instance = BasicLammaAgent()

async def llmResponse(message, history): 
    return await agent_instance(message)

gr.ChatInterface(
    fn=llmResponse, 
    type="messages"
).launch()
