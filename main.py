from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.id_card import router as id_card_router
from app.land_use import router as land_use_router


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(id_card_router, prefix="/api")
app.include_router(land_use_router, prefix="/api")

# Error handling


@app.exception_handler(Exception)
async def validation_exception_handler(_, exc):
    return JSONResponse(
        status_code=400,
        content={"de": "An error occurred"},
    )
