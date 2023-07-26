import logging

from langchain import LLMMathChain, SQLDatabase, SQLDatabaseChain
from langchain.agents import AgentType
from langchain.tools.gmail import get_gmail_credentials
from langchain.tools.google_trends import GoogleTrendSearch
from langchain.tools.python.tool import PythonREPLTool
from langchain.agents import initialize_agent
from langchain.tools import GmailCreateDraft, Tool, GmailSendMessage
from langchain.agents.agent_toolkits import FileManagementToolkit
from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSearchAPIWrapper

from langchain.tools.youtube import YouTubeSearch
from workspace.custom_chain.self_checking_chain import CustomChain
from workspace.custom_tools.custom import YouTubeCustom
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()


def init():
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    search = GoogleSearchAPIWrapper()

    db = SQLDatabase.from_uri("mysql+pymysql://root:123456@127.0.0.1:3306/mict", include_tables=['video'],
                              sample_rows_in_table_info=2)
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

    tools = [
        GoogleTrendSearch(),
        YouTubeCustom(),
        GmailSendMessage(),
        Tool(
            name="Youtube-DB",
            func=db_chain.run,
            description="useful for when you need to answer questions about Youtube. Input should be in the form of a question containing full context"
        )
    ]

    mrkl = initialize_agent(
        tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=5,
        early_stopping_method="generate",
    )
    return llm, mrkl


if __name__ == '__main__':
    # input = "我想知道最近三个月关于home gym话题的趋势,如果趋势上升，从youtube上找到相关的视频，保存在数据库中，将视频信发送到wzybmw888@163.com的邮箱，如果没有趋势，就不进行后续操作！"
    # custom_chain = CustomChain(llm, input)
    # res = custom_chain.run()
    # print(res)
    # mrkl.run(res)
    # mrkl.run("将video表中主要内容发送给wzybmw888@163.com的邮箱")
    DEFAULT_SCOPES = ["https://mail.google.com/", "https://www.googleapis.com/auth/gmail.modify",
                      "https://www.googleapis.com/auth/youtubepartner",
                      "https://www.googleapis.com/auth/youtube.readonly"]
    get_gmail_credentials(client_secrets_file="credentials.json", scopes=DEFAULT_SCOPES)
    input = "我想知道最近三个月关于home gym话题的趋势,如果趋势上升，从youtube上找到相关的视频，保存在数据库中，将视频信息发送到20021028@qq.com的邮箱，如果没有趋势，就不进行后续操作！"
    llm, mrkl = init()

    custom_chain = CustomChain(llm, input)
    res = custom_chain.run()
    mrkl.run(res)
