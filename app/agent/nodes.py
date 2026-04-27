import json
import os
from langchain.messages import ToolMessage
from langchain_openai import ChatOpenAI
from app.agent.state import AgentState
from app.core.config import get_settings
from app.tools.rag_tool import retrieve_relevant_chunks
from app.tools.github_tool import get_repo_info
from app.tools.user_capture_tool import capture_user_info
from app.agent.prompt import system_pmt_agent

config = get_settings()
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY

llm_openai = ChatOpenAI(model="gpt-4o-mini",temperature=0.0)
toolkit = [retrieve_relevant_chunks,get_repo_info,capture_user_info]
llm_with_tools = llm_openai.bind_tools(tools=toolkit) # type: ignore

def llm_node(state:AgentState):
    message = state["messages"]
    if not any(msg.type == "system" for msg in message):
        result = llm_with_tools.invoke([system_pmt_agent] + message)
    else:
        result = llm_with_tools.invoke(message)
    return {
        "messages":[result]
    }


def tool_node(state:AgentState,config):
    message = state["messages"]
    tool_by_name = { tool.name : tool for tool in toolkit}
    tool_result = []
    for tool_call in message[-1].tool_calls: # type: ignore
        tool = tool_by_name[tool_call["name"]]
        if tool_call["name"] == "capture_user_info":
            tool_call["args"]["thread_id"] = config["configurable"]["thread_id"]
        observation = tool.invoke(tool_call["args"])
        content = json.dumps(observation) if isinstance(observation,list) else observation
        tool_result.append(ToolMessage(content=content,tool_call_id=tool_call["id"]))
    
    return {
        "messages":tool_result
    }

def if_tool_call(state:AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls: # type: ignore
        return "goto_tool_node"
    else:
        return "goto_end"