from langchain.agents import Tool
from langchain.agents import AgentType
from langchain import LLMMathChain, SQLDatabase, SQLDatabaseChain
from langchain.tools.google_trends import GoogleTrendSearch
from langchain.tools.python.tool import PythonREPLTool
from langchain import OpenAI
from langchain.agents import initialize_agent
from langchain.tools import YouTubeSearchTool
from langchain.tools import HumanInputRun
from langchain.agents.agent_toolkits import FileManagementToolkit
from langchain.agents.agent_toolkits import GmailToolkit
from langchain.tools.youtube import YouTubeSubscribe
from langchain.agents.agent_toolkits import YouTubeToolkit
from langchain.chat_models import ChatOpenAI
import langchain
import os

from workspace.custom_tools.custom import YouTubeCustom

os.environ["http_proxy"] = "http://127.0.0.1:22307"
os.environ["https_proxy"] = "http://127.0.0.1:22307"

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

# tools = YouTubeToolkit().get_tools()
# tools.append(GoogleTrendSearch())
tools = [YouTubeCustom()]

mrkl = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=2,
    early_stopping_method="generate",
)

langchain.debug = True

if __name__ == '__main__':
    res = mrkl.run("获取youtube上关于mysql的视频保存到数据库中")
    print(res)
