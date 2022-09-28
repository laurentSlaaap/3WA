from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routes.user import user

# Api init
app = FastAPI()



# CORS settings
origins = ['https://localhost:8000',
            "http://localhost:3000",
            "http://localhost:3000/*",
            
]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# routes caller
app.include_router(user)

