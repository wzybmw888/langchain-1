print("Answer the following questions as best you can. You have access to the following tools:\n\nyoutube_subscribe: Use this tool to follow the blogger's youtube channel with the provided message fields.\nyoutube_search: Use this tool to search related videos with the provided message fields.\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [youtube_subscribe, youtube_search]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nWhen answering, you MUST speak in the following language: {language}.\n\n    Question: {input}\n    {agent_scratchpad}")