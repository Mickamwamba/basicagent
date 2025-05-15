import os 
from smolagents import OpenAIServerModel,CodeAgent,tool,DuckDuckGoSearchTool
from tools import CustomTools
import gradio as gr 

class BasicAgent: 

    def __init__(self):
        pass
    @tool 
    def sample_tool()->str:
        """This tool is used to respond to general questions. If no specific action is specificied this tool should be called
        Args: None
        """

        return "Hello, How can I help you today? Be free to say it loud"
    
    def __call__(self, question: str)-> str:
        model = OpenAIServerModel(
            model_id="gpt-4", 
            api_key=os.getenv("OPEN_AI_API_KEY")
        )
        sample_tool = self.sample_tool
        search_tool = CustomTools.search
        match_tool = CustomTools.matches
        code_agent = CodeAgent(
            model=model, 
            tools=[sample_tool,search_tool,match_tool]
        )

        response = code_agent.run(question)
        return response

    


def llmResponse(message, history): 
    agent = BasicAgent()
    return agent(message)


gr.ChatInterface(
    fn=llmResponse, 
    type="messages",
    save_history=True
).launch()
