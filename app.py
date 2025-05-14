import os 
from smolagents import OpenAIServerModel,CodeAgent,tool,DuckDuckGoSearchTool
from tools import GoogleSearchTool

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
        # search_tool = DuckDuckGoSearchTool()
        search_tool = GoogleSearchTool.search
        code_agent = CodeAgent(
            model=model, 
            tools=[sample_tool,search_tool]
        )

        response = code_agent.run(question)
        return response

    


agent = BasicAgent()


agent("Who is Michael Jackson?")

# print(GoogleSearchTool.search("Who is Michael Jackson"))