from enum import Enum
from pydantic import BaseModel, Field


class Country(str, Enum):
    global_ = '全球'
    US = '美国'
    CA = '加拿大'
    GB = '英国'
    AU = '澳大利亚'
    IN = '印度'
    DE = '德国'
    FR = '法国'
    CN = '中国'


class MyModel(BaseModel):
    country: str = Field(..., description="国家")


# 示例用法
m = MyModel(country=Country.US)
print(m)

if __name__ == '__main__':
    print("System: Respond to the human as helpfully and accurately as possible. You have access to the following tools:\n\ngoogle_trend_search: Use this tool to search related google trend with the provided message fields., args: {{'keyword': {{'title': 'Keyword', 'description': 'keyword information', 'type': 'string'}}, 'period': {{'title': 'Period', 'description': 'contains start date, end date', 'example': '2016-12-14 2017-01-25', 'type': 'string'}}, 'cat': {{'title': 'Cat', 'description': 'Category of the industry where the information is queried', 'default': 0, 'type': 'integer'}}, 'geo': {{'title': 'Geo', 'description': 'Category of the country where the information is located', 'default': '', 'type': 'string'}}}}\n\nUse a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).\n\nValid \"action\" values: \"Final Answer\" or google_trend_search\n\nProvide only ONE action per $JSON_BLOB, as shown:\n\n```\n{\n  \"action\": $TOOL_NAME,\n  \"action_input\": $INPUT\n}\n```\n\nFollow this format:\n\nQuestion: input question to answer\nThought: consider previous and subsequent steps\nAction:\n```\n$JSON_BLOB\n```\nObservation: action result\n... (repeat Thought/Action/Observation N times)\nThought: I know what to respond\nAction:\n```\n{\n  \"action\": \"Final Answer\",\n  \"action_input\": \"Final response to human\"\n}\n```\n\nBegin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation:.\nThought:\nHuman: home gym关键词在中国的趋势如何？")