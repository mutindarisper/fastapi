from fastapi import APIRouter

router = APIRouter() #use router instead of app so that we can use it as a route in the main app

@router.get("/auth")
async def get_user():
    return {"user": "authenticated"}