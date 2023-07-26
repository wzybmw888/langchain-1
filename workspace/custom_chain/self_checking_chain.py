from __future__ import annotations
from dotenv import load_dotenv
from langchain import PromptTemplate, LLMChain

load_dotenv()


class CustomChain:
    def __init__(self, llm, input):
        self.prompt_template = """For complex problems, you should break the problem into multiple subproblems, using 1,2,3,... To mark out the subproblem. 
        For simple problems, output the problem directly.
        {input}
        """
        self.llm = llm
        self.input = input

    def run(self):
        llm_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(template=self.prompt_template, input_variables=["input"])
        )
        return llm_chain.predict(input=self.input)


