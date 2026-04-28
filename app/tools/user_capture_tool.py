from typing import Any, Dict, List, cast
from app.services.supabase_service import sc
from langchain_core.tools import tool

@tool
def capture_user_info(name:str="",company:str="",email:str=""):
    """
        Capture user contact details when they are explicitly shared in conversation.

        Trigger this tool ONLY when the user provides meaningful contact information such as:
        - a valid email address (preferred), and/or
        - a clear company name, and/or
        - their name

        Guidelines:
        - Do NOT call this proactively — only when the user voluntarily shares details.
        - Prefer calling this when an email is present, as it acts as a unique identifier.
        - If only partial information (name or company) is available, you may still call it, but avoid repeated or unnecessary calls.
        - Do NOT call multiple times for the same message.

        Inputs:
        - name (optional)
        - company (optional)
        - email (optional)

        At least one meaningful field should be present.
    """
    if not email or not company:
        return "Details not sufficient to enter in DB"
    
    if email:
        existing_record = sc.table("users").select("*").eq("email",email).execute()
        data = cast(List[Dict[str, Any]], existing_record.data or [])
        if data:
            record = data[0]
            sc.table("users").update({
                "name":name or record["name"],
                "company":company or record["company"]
            }).eq("email",email).execute()

    sc.table("users").insert({
        "name":name,
        "email":email,
        "company":company
    }).execute()
    
    return "User Successfully added"
