# _*_ coding : utf-8 _*_
# @Time : 2024/7/8 17:45
# @Author : 刘俊雄
# @File : 模型测试2
# @Project : python程序
import io
import os

import cv2
import rembg
import torch
from PIL import Image
import numpy as np
from fastapi import UploadFile, File
from starlette.responses import StreamingResponse

from tsr.system import TSR
from tsr.utils import to_gradio_3d_orientation, remove_background, resize_foreground

os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

def cs(img,obj):
    input_img_url = img
    output_img_url = obj

    # 设置设备
    print('正在设置设备。。。')
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print('设备设置完成')

    # 加载模型
    print('正在加载模型。。。')
    model = TSR.from_pretrained(
        "stabilityai/TripoSR",
        config_name="config.yaml",
        weight_name="model.ckpt",
    )
    model.renderer.set_chunk_size(8192)
    model.to(device)
    print('模型加载完成')

    print('正在创建 rembg 会话。。。')
    # 创建 rembg 会话
    rembg_session = rembg.new_session()
    print('rembg 会话创建成功')

    def fill_background(image):
        image = np.array(image).astype(np.float32) / 255.0
        image = image[:, :, :3] * image[:, :, 3:4] + (1 - image[:, :, 3:4]) * 0.5
        image = Image.fromarray((image * 255.0).astype(np.uint8))
        return image

    def preprocess(input_image, do_remove_background=True, foreground_ratio=0.85):
        if do_remove_background:
            image = input_image.convert("RGB")
            image = remove_background(image, rembg_session)
            image = resize_foreground(image, foreground_ratio)
            image = fill_background(image)
        else:
            image = input_image
            if image.mode == "RGBA":
                image = fill_background(image)
        return image

    def image_to_obj(input_image_path, output_obj_path, mc_resolution=256, remove_bg=True):
        # 加载图片
        print('正在加载图片。。。')
        image = Image.open(input_image_path).convert("RGBA")
        print('图片加载成功')

        # 预处理图片
        print('正在预处理图片。。。')
        image = preprocess(image, do_remove_background=remove_bg)
        print('图片预处理成功')

        # 生成场景代码
        print('正在生成场景代码。。。')
        scene_codes = model(image, device=device)
        print('场景代码生成成功')

        # 提取网格并转换为 OBJ 格式
        print('正在提取网格。。。')
        mesh = model.extract_mesh(scene_codes, True, resolution=mc_resolution)[0]
        mesh = to_gradio_3d_orientation(mesh)
        print('网格提取成功')

        # 导出 OBJ 文件
        print('正在导出 OBJ 文件。。。')
        mesh.export(output_obj_path)
        print('OBJ 文件导出成功')

    # 示例用法
    input_image_path = input_img_url  # 替换为您的图片路径
    output_obj_path = output_img_url  # 您希望保存 OBJ 文件的路径
    mesh = image_to_obj(input_image_path, output_obj_path)
    print('代码执行完毕')



if __name__ == '__main__':
    img = input('请输入图片名称并将图片放在imgtoobj文件夹中（图片名称为xxx.xxx,如imgtoobj/chair.png）:')
    obj = f'{img}.obj'
    cs(img,obj)
