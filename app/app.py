from fastapi import FastAPI
#from app.route import user_routes, team_routes, appointment_routes, permission_routes

app = FastAPI()
#
# app.include_router(userRoute.router)
# app.include_router(team_routes.router)
# app.include_router(appointment_routes.router)
# app.include_router(permission_routes.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}