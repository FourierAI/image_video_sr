import streamlit as st
import numpy as np
from algorithm import *
import tempfile
import os

tmp_dict = {'1280*720 [720P]':(1280, 720), '1920*1080 [1080P]':(1920, 1080),
          '2560*1440 [2k]':(2560, 1440),'3840*2160 [4k]':(3840, 2160)}

def is_video(file_name):
  suffix = file_name.split('.')[-1]
  if suffix in ['avi', 'wmv', 'mpg', 'mpeg', 'mov','mp4']:
    return True
  return False

image_placeholder = st.empty()
st.title('视频超分辨率')

uploaded_file = st.file_uploader("请上传视频文件")
if uploaded_file is not None:
    file_name = uploaded_file.name

    if is_video(file_name):
      try:
        st.video(uploaded_file.getvalue())
      except Exception:
        e = RuntimeError('文件上传出错，请重试！')
        st.exception(e)
      option = st.selectbox(
          '选择你需要的算法',
          ('最近邻插值算法', '双线性插值算法','双三次插值算法'))

      resoultion_str = st.selectbox(
          '选择视频输出分辨率',
          ('1280*720 [720P]', '1920*1080 [1080P]',
          '2560*1440 [2k]','3840*2160 [4k]'))

      resoultion = tmp_dict[resoultion_str]

      if st.button('生成视频'):
        with st.spinner("生成中，请稍等。"):
          tfile = tempfile.NamedTemporaryFile(delete=False)
          tfile.write(uploaded_file.read())

          cap = cv2.VideoCapture(tfile.name)

          fourcc = cv2.VideoWriter_fourcc(*'XVID')

          out_file_name = f'{file_name.split(".")[0]}.avi'

          out = cv2.VideoWriter(out_file_name, fourcc, 5, resoultion)

          frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

          my_bar = st.progress(0)
          percent_complete = 0
          while cap.isOpened():
              ret, frame = cap.read()
              if ret:
                  b = resize_video(frame, resoultion, option)
                  out.write(b)
                  my_bar.progress(percent_complete/frame_count)
                  percent_complete = percent_complete + 1

              else:
                  cap.release()
                  out.release()

        st.success('生成成功，请下载。')

        with open(out_file_name, 'rb') as file:
          btn = st.download_button(
              label="Download Video",
              data=file,
              file_name=out_file_name,
              mime="application/octet-stream"
            )

        os.remove(out_file_name)
    else:
      st.error('请上传视频文件', icon="🚨")
       
 
       




        