import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from internal.controller.ApiUserController import routerUser
from internal.controller.ApiEmailController import routerEmail
from internal.controller.ApiEmailFolderController import routerEmailFolder
from internal.facade.UserFacade import UserFacade
from internal.data.ApplicationDbContext import ApplicationDbContext



app = FastAPI(
    title="Лабораторная работа №2 и №3. Савва Даниил",
    debug=True
)
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
    """Для проверки, что сервис работает"""
    return {"status":"success"}

@app.on_event("startup")
def on_startup():
    #try:
    ApplicationDbContext.init_db()
    
    # except Exception as e:
    #     print("Ошибка генерации таблиц в базе данных", str(e))
    #     print("\n\n\nВозможно это был первый запуск создания image для postgres, из-за задержки автоматической настройки postgres, скрипт слишком рано запускает автоматическую генерацию таблиц.\nДождитесь пожалуйста загрузки создания image postgres и попробуйте запустить контейнер еще раз")
    #     return
    try:
        userFacade: UserFacade = UserFacade()
        userFacade.create_if_not_exists_user_master()
    except Exception as e:
        print("Ошибка создания мастер-пользователя:", str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8092)
    
