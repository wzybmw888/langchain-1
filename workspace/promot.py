from langchain import LLMChain, OpenAI
from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain.agents.agent_toolkits import YouTubeToolkit

import os

os.environ["http_proxy"] = "http://127.0.0.1:22307"
os.environ["https_proxy"] = "http://127.0.0.1:22307"

def custom_prompt(tools):
    prefix = """Answer the following questions as best you can. You have access to the following tools:"""
    suffix = """When answering, you MUST speak in the following language: {language}.
Question: {input}
{agent_scratchpad}
"""

    prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix=prefix,
        suffix=suffix,
        input_variables=["input", "language","agent_scratchpad"],
    )
    return prompt


if __name__ == '__main__':
    tools = []
    tools += YouTubeToolkit().get_tools()
    prompt = custom_prompt(tools)
    llm_chain = LLMChain(llm=OpenAI(temperature=0,model_name="gpt-3.5-turbo"), prompt=prompt)
    agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools)
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, verbose=True
    )
    res = agent_executor.run(
        input="给出2023年6月后youtube上home gym观看最多的5个视频", language="chinese"
    )
    print(res)