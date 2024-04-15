from fastapi import FastAPI
from app.router import UserRoutes, TeamRoutes,AppointmentRoutes
from app.database import Base, engine
https://code-with-me.global.jetbrains.com/xMK2cyVuT9aV6qn6PpuDOw#p=PY&fp=88472F15F25BA4FC077457CE9462056FD2848AC9B2047A8FD46933DB0BEE4481&newUi=true


app = FastAPI(debug=True)
#
app.include_router(UserRoutes.router)
app.include_router(TeamRoutes.router)
app.include_router(AppointmentRoutes.router)
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