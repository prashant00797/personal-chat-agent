from langgraph.graph import END, START, StateGraph
from app.agent.nodes import if_tool_call, llm_node, tool_node
from app.agent.state import AgentState


def create_agent_graph():
    builder = StateGraph(AgentState)
    builder.add_node("llm_node", llm_node)
    builder.add_node("tool_node", tool_node)
    builder.add_edge(START, "llm_node")
    builder.add_conditional_edges("llm_node", if_tool_call, 
    {
        "goto_tool_node": "tool_node",
        "goto_end": END
    })
    builder.add_edge("tool_node", "llm_node")
    return builder.compile()
    

