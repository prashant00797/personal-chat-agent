import re
from app.services.supabase_service import sc
from langchain_core.tools import tool

@tool
def capture_user_info(name:str="",company:str="",email:str=""):
    """
        Save a visitor's contact details to the database.
        Call this when the user shares their contact information — name, company and email.
        Extract whatever fields are available from the conversation and pass them to the tool.
        The tool will validate before saving.
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    existing = sc.table("users").select("id").eq("email", email).execute()
    
    if not re.match(email_regex, email):
        return "Email address looks invalid. Please provide a valid email like name@company.com"
    
    elif existing.data:
        return "Details already saved. Prashant will be in touch!"
    
    elif not name or not company or not email:
        return "I'd be happy to save your details! Please share your name, company and email together in one message."
    
    sc.table("users").insert({
        "name":name,
        "email":email,
        "company":company
    }).execute()
    
    return "User Successfully added"
