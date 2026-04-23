from app.services.supabase_service import sc


def register_user(userData:dict):
    print(userData)
    sc.table("users").insert(userData).execute()
    return "User Successfully added"


# test
# res = register_user({"name":"rohit","company":"meta","email":"r@g.co"})
# print(res)