from langchain import LLMMathChain
from langchain.agents import AgentType
from langchain.tools.google_trends import GoogleTrendSearch
from langchain.tools.python.tool import PythonREPLTool
from langchain.agents import initialize_agent
from langchain.tools import GmailCreateDraft, Tool,GmailSendMessage
from langchain.agents.agent_toolkits import FileManagementToolkit
from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSearchAPIWrapper

from langchain.tools.youtube import YouTubeSearch
from workspace.custom_tools.custom import YouTubeCustom
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
search = GoogleSearchAPIWrapper()
tools = [
    GoogleTrendSearch(),
    YouTubeCustom(),
    PythonREPLTool(),
    GmailCreateDraft(),
    GmailSendMessage(),
    YouTubeSearch(),
    Tool(
        name="Google_Search",
        description="Search the latest information from google.",
        func=search.run,
    )
]

tools.extend(
    FileManagementToolkit(root_dir=r"/workspace",
                          selected_tools=["read_file", "write_file"]).get_tools()
)

mrkl = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=5,
    early_stopping_method="generate",
)

if __name__ == '__main__':
    # res = mrkl.run(
    #     "我想知道最近三个月关于home gym话题的趋势,如果趋势上升，从youtube上找到相关的视频，保存在youtube邮箱草稿中和本地文件中，如果没有趋势，就不进行后续操作！")
    # print(res)
    # mrkl.run("你现在是一个金融专家，帮我整理最近一周金融相关的信息，发送到wzybmw888@163.com的邮箱中！")
    mrkl.run("发送hello到wzybmw888@163.com的邮箱中！")
