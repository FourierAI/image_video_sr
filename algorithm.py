import cv2

def resize_im(im,zoom_factor,option):
    if option == "最近邻插值算法":
        im_ = cv2.resize(im, (0,0), fx=zoom_factor, fy=zoom_factor, interpolation=cv2.INTER_NEAREST)
    elif option == "双线性插值算法":
        im_ = cv2.resize(im, (0,0), fx=zoom_factor, fy=zoom_factor, interpolation=cv2.INTER_LINEAR)
    elif option == "双三次插值算法":
        im_ = cv2.resize(im, (0,0), fx=zoom_factor, fy=zoom_factor, interpolation=cv2.INTER_CUBIC)
    elif option == "EDSR深度学习算法":
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        path = f"config/EDSR_x{zoom_factor}.pb"
        sr.readModel(path)
        sr.setModel("edsr", zoom_factor)
        im_ = sr.upsample(im)
    elif option == "FSRCNN深度学习算法":
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        path = f"config/FSRCNN_x{zoom_factor}.pb"
        sr.readModel(path)
        sr.setModel("fsrcnn", zoom_factor)
        im_ = sr.upsample(im)
    else: 
        im_ = [[0,0],[0,0]]
    return im_

def resize_video(im,resolution,option):
    if option == "最近邻插值算法":
        im_ = cv2.resize(im, resolution, fx=0, fy=0, interpolation=cv2.INTER_NEAREST)
    elif option == "双线性插值算法":
        im_ = cv2.resize(im, resolution, fx=0, fy=0, interpolation=cv2.INTER_LINEAR)
    elif option == "双三次插值算法":
        im_ = cv2.resize(im, resolution, fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
    else: 
        im_ = [[0,0],[0,0]]
    return im_


if __name__ == "__main__":
    cap = cv2.VideoCapture('1.mp4')

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, 5, (2560,1440))
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            b = cv2.resize(frame,(2560,1440),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
            out.write(b)
        else:
            cap.release()
            out.release()

    
