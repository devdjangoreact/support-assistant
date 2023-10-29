import uvicorn
import fastapi
import restapi.router
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI()

origins = ["http://localhost:3000", "http://127.0.0.1:3000", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
restapi.router.configure(app)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
