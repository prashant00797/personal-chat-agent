from fastapi import APIRouter, HTTPException
from app.schema.register_schema import RegisterUser
from app.services.supabase_service import sc
router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/register")
def register_user(request:RegisterUser):
    return add_user_supabase(request)


# service
def add_user_supabase(request):
    res = sc.table("users").insert({"name":request.name,"company":request.company,"email":request.email}).execute()
    if res.data:
        id = res.data[0]["id"] # type: ignore
    else:
        raise HTTPException(status_code=500,detail="Failed to enter in supabse db. Please try again")
    return id
    