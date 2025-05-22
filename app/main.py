from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.data import router as get_data

app = FastAPI()

# CORS Middleware (so frontend apps can connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(get_data)


@app.get("/")
def read_root():
    return {"################################### Backend-api live! ####################################"}
