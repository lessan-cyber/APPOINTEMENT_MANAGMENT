from fastapi import FastAPI
from app.router import UserRoutes
from app.database import Base, engine



app = FastAPI()
#
app.include_router(UserRoutes.router)
# app.include_router(team_routes.router)
# app.include_router(appointment_routes.router)
# app.include_router(permission_routes.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

def create_tables():
    Base.metadata.create_all(engine)

create_tables()
# if __name__ == "__main__":
#     create_tables()