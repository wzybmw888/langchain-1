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
from langchain.agents.agent_toolkits import YouTubeToolkit
from langchain.chat_models import ChatOpenAI
import langchain
import os

from langchain.tools.youtube.api import YouTubeAPIOperate
from workspace.custom_tools.custom import YouTubeCustom

#
os.environ["http_proxy"] = "http://127.0.0.1:22307"
os.environ["https_proxy"] = "http://127.0.0.1:22307"
#
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

tools = [
    GoogleTrendSearch(),
    YouTubeCustom(),
    PythonREPLTool(),
]

tools.extend(YouTubeToolkit().get_tools())
tools.extend(
    FileManagementToolkit(root_dir=r"E:\PythonProject\langchain\workspace",
                          selected_tools=["read_file", "write_file"]).get_tools()
)
tools.extend(GmailToolkit().get_tools())

mrkl = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=5,
    early_stopping_method="generate",
)

langchain.debug = True

if __name__ == '__main__':
    res = mrkl.run(
        "我想知道最近三个月关于home gym话题的趋势,如果趋势上升，从youtube上找到相关的视频，保存在youtube邮箱草稿中和本地文件中，如果没有趋势，就不进行后续操作！")
    print(res)
