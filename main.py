import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from internal.controller.ApiUserController import routerUser
from internal.controller.ApiEmailController import routerEmail
from internal.controller.ApiEmailFolderController import routerEmailFolder
from internal.facade.UserFacade import UserFacade
from internal.Entities import User

app = FastAPI(debug=True)
origins = [
    "http://localhost:3000", 
]
app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

app.include_router(routerUser, prefix="/api/user")
app.include_router(routerEmail, prefix="/api/email")
app.include_router(routerEmailFolder, prefix="/api/email_folder")

@app.get("/api")
def index():
    return {"status":"success"}

if __name__ == "__main__":

    try:
        userFacade: UserFacade = UserFacade()
        userFacade.create_if_not_exists_user_master()
    except Exception as e:
        print("Ошибка созданиея мастер-пользователя:", str(e))

    uvicorn.run(app, host="0.0.0.0", port=8092)