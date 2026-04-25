import asyncio
import json
import traceback
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from app.agent.prompt import get_onboarding_prompt
from app.schema.chat_schema import ChatRequest
from app.services.supabase_service import sc
from rich.pretty import pprint


router = APIRouter(tags=["Chat"])

@router.post("/chat")
async def user_message(user_request:ChatRequest,req:Request):
    return await ai_reponse(user_request,req)


# service --> this needs to be abstracted
async def ai_reponse(user_request,req):
   cp = req.app.state.checkpointer
   graph = req.app.state.graph
   user_name_query = sc.table("users").select("name","id").eq("id",user_request.thread_id).execute()
   if user_name_query.data:
       user_name = user_name_query.data[0]["name"] # type: ignore
       user_id = user_name_query.data[0]["id"] # type: ignore
   else:
       raise HTTPException(status_code=500,detail="DB server failure")
   config = {"configurable":{"thread_id":user_id}}
   onboarding_message = get_onboarding_prompt(user_name=user_name) # type: ignore
   if not await cp.aget_tuple(config):
       messages = [onboarding_message,HumanMessage(content=user_request.message)]
    #    pprint(cp.aget_tuple(config))
   else:
       messages = [HumanMessage(content=user_request.message)]


#    result = await graph.ainvoke(
#     {"messages": messages},
#     config=config
#     )
#    print(result)
# --> thinking of abstracting this too -- todo
   async def event_generator():
        try:
            async for event in graph.astream_events(
                {"messages": messages},
                config=config,
                version="v2"
            ):
                pprint(event)
                kind = event.get("event")

                if kind == "on_tool_start":
                    tool_name = event.get("name", "unknown")
                    yield f"data: {json.dumps({'type': 'tool_call', 'tool': tool_name})}\n\n"

                elif kind == "on_chat_model_stream":
                    chunk = event.get("data", {}).get("chunk")
                    # pprint(chunk)
                    if chunk and getattr(chunk, "content", None):
                        token = chunk.content
                        yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"
                        await asyncio.sleep(0.03)


            yield f"data: {json.dumps({'type': 'end'})}\n\n"

        except Exception as e:
            traceback.print_exc() 
            yield f"data: {json.dumps({'type': 'error', 'message': repr(e)})}\n\n"
 
   return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

  