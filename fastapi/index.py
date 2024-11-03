# _*_ coding : utf-8 _*_
# @Time : 2024/7/7 20:57
# @Author : 刘俊雄
# @File : 测试
# @Project : python程序
import uvicorn
from fastapi import FastAPI

# import mysql
# from 回收站.users_api import users_api
from api.imgtoobj_api import imgtoobj_api
# from 回收站 import login_api
# from mysql import TORTOISE_ORM
# from 回收站 import qd

app = FastAPI()

# qd(app, TORTOISE_ORM)
# qd(app)

app.include_router(imgtoobj_api, prefix='/imgtoobj', tags=["图生模型接口"])
# app.include_router(imgs_api, prefix='/imgs', tags=["img接口"])
# app.include_router(objs_api, prefix='/obj', tags=["obj接口"])
# app.mount("/mount", StaticFiles(directory="mount"), name="mount")

@app.get('/')
async def root():
    return {"message": "Hello world!"}

# @app.get('/get_mm')
# async def get_mm(request: Request):
#     get_mm = request.query_params
#     print(get_mm)
#     return {"params": get_mm}
#
# @app.post('/post_mm')
# async def post_mm(request: Request):
#     post_mm = await request.json()
#     print(post_mm)
#     return {"json": post_mm}

if __name__ == '__main__':
    uvicorn.run(app="index:app", host="127.0.0.1", port=8020, reload=True)
