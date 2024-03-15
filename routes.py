from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.post("/search")
async def search(query: Message):
    return {"message": query}
