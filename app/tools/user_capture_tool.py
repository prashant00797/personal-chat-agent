from app.services.supabase_service import sc
from langchain_core.tools import tool

@tool
def capture_user_info(thread_id:str,company:str="",email:str=""):
    """
        Update the user's record with their company name and/or email address.
        Trigger this when the user shares EITHER their company name OR their email
        — or both — at any point in the conversation.
        Input: thread_id (current session ID), company (optional), email (optional).
        At least one of company or email must be present to trigger this tool.
        Never call this proactively — only when the user volunteers the information.
    """
    sc.table("users").update({"company":company,"email":email}).eq("id",thread_id).execute()
    return "User Successfully added"
