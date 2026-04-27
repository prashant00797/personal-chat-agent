from fastapi import APIRouter
from app.api.api_service.register_service import add_user_supabase
from app.schema.register_schema import RegisterUser


router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/register")
def register_user(request:RegisterUser):
    return add_user_supabase(request)
    