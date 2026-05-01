import asyncio
import json
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage


async def ai_reponse(user_request,req):
   graph = req.app.state.graph
   messages = [HumanMessage(content=user_request.message)]
   config = {'configurable':{'thread_id':user_request.thread_id}}

# STREAMING
   async def event_generator():
        try:
            async for event in graph.astream_events(
                {"messages": messages},
                config=config,
                version="v2"
            ):
                kind = event.get("event")

                if kind == "on_tool_start":
                    tool_name = event.get("name", "unknown")
                    yield f"data: {json.dumps({'type': 'tool_call', 'tool': tool_name})}\n\n"

                elif kind == "on_chat_model_stream":
                    chunk = event.get("data", {}).get("chunk")
                    if chunk and getattr(chunk, "content", None):
                        token = chunk.content
                        yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"
                        # await asyncio.sleep(0.09) -> removing since latency already there due to render server at virginia.


            yield f"data: {json.dumps({'type': 'end'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': repr(e)})}\n\n"
 
   return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
