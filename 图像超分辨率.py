import streamlit as st
import numpy as np
import cv2
from algorithm import *
import os

def is_im(file_name):
  suffix = file_name.split('.')[-1]
  if suffix in ['png', 'jpg', 'jpeg', 'gif']:
    return True
  return False

st.title('图像超分辨率')

uploaded_file = st.file_uploader("请上传图片文件")
if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    file_name = uploaded_file.name
    if is_im(file_name):
      
      im = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

      st.image(im, channels="BGR")
      st.write('图片尺寸')
      st.write(im.shape)

      option = st.selectbox(
          '选择你需要的算法',
          ('最近邻插值算法', '双线性插值算法','双三次插值算法',
          'EDSR深度学习算法', 'FSRCNN深度学习算法'))

      if option in ['EDSR深度学习算法', 'FSRCNN深度学习算法']:
        zoom_factor = st.number_input('请输入超分辨率的缩放因子, 目前深度学习算法只支持2-4倍', min_value = 2, max_value = 4, step = 1, format='%d')
      else:
        zoom_factor = st.number_input('请输入超分辨率的缩放因子, 目前深度学习算法只支持2-4倍', min_value = 2, max_value = 6, step = 1, format='%d')
      
      if st.button('生成图像'):
        with st.spinner("生成中，请稍等。"):
          im_result  = resize_im(im,zoom_factor,option)
          st.image(im_result, channels="BGR")
          st.write(im_result.shape)

          # 持久化到硬盘
          cv2.imwrite("tmp.png", im_result)
        st.success("生成成功，请下载。")
        with open('tmp.png', 'rb') as file:
          btn = st.download_button(
              label="下载图像",
              data=file,
              file_name=f"{file_name.split()[0]}",
              mime="image/png"
            )
        os.remove("tmp.png")
    else:
      st.error('请上传图像文件', icon="🚨")
 
       




        