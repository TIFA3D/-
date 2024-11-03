from datetime import datetime

from fastapi import APIRouter, UploadFile, File
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field

# from 回收站 import ImgAndObj as imgandobj_model
# from 回收站.FQA import show_time

imgtoobj_api = APIRouter()

# class ImgsIn(BaseModel):
#     phone: str = Field('123-4567-8901', description="电话号码必须为3+4+4的纯数字格式")  # 必填
#     imgurl: str = Field(..., description="路径为")
#     upload_time: datetime = Field(show_time(), description="图片上传日期")  # 自动生成
# #
#
# @imgandobj_api.post("/addImg")
# async def addImg(imgs_in: ImgsIn):
#
#     img = await imgandobj_model.create(
#         phone_id = imgs_in.phone,
#         imgurl = imgs_in.imgurl,
#
#     )
#     return {f"成功为用户 {imgs_in.phone} 添加了一条信息"}
#

# @imgandobj_api.delete("/deleteImg/{phone}")
# async def deleteImg(phone: str, imgurl: str):
#     delete_count = await imgandobj_model.filter(phone_id=phone, imgurl=imgurl).delete()
#     if not delete_count:
#         raise HTTPException(status_code=404, detail=f"用户名为 {phone} 且图片路径为 {imgurl} 的图片信息不存在")
#     return {"data": f"删除了用户名为 {phone} 且图片路径为 {imgurl} 的图片信息"}

#
# @imgandobj_api.get("/getIdImg/{phone}")
# async def getIdImg(phone: str):
#     imgs = await imgandobj_model.filter(phone_id=phone).values('phone_id','imgurl','upload_time','objurl','objtime')
#     if not imgs:
#         raise HTTPException(status_code=404, detail=f"用户名为 {phone} 的图片信息不存在")
#     return imgs


from api.model import cs
# class ObjsIn(BaseModel):
#     objurl: str = Field(..., description="chair.obj")
#     objtime: datetime = Field(show_time(), description="无需输入")
#

@imgtoobj_api.post("/CreateObj")
async def CreateObj(imgfile: UploadFile = File(...)):
    # user = await users_model(username=usre_in.username, password=usre_in.password, email=usre_in.email)
    # await user.save()
    # input =imgurl
    # url = 'imgtoobj'
    # output = f'{imgurl}.obj'

    obj = cs(imgfile,'imgtoobj/kkk.obj')
    return obj
    # return output