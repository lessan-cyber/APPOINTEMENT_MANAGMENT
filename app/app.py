from fastapi import FastAPI
from app.router import UserRoutes

app = FastAPI()
#
app.include_router(UserRoutes.router)
# app.include_router(team_routes.router)
# app.include_router(appointment_routes.router)
# app.include_router(permission_routes.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}