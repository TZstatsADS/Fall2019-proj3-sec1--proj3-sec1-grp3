import cv2
import glob
import os
import numpy as np

path = os.getcwd()

class FaceCropper(object):
    CASCADE_PATH = path + "/haarcascade_frontalface_default.xml"

    def __init__(self):
        print(self.CASCADE_PATH)
        self.face_cascade = cv2.CascadeClassifier(path + "/haarcascade_frontalface_default.xml")
        

    def generate(self, image_path, show_result=False, d = 0):
        img = cv2.imread(image_path)
        if (img is None):
            print("Can't open image file")
            return 0

        #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(img, 1.1, 5, minSize=(100, 100))
        facecnt = len(faces)
        print("Detected faces: %d" % facecnt)

        if (faces is None):
            return faces
        elif len(faces) > 1:
            eval = []

            # solve the issue when there are multiple detection
            for face in faces:
                x,y,w,h = face
                r = max(w, h) / 2
                size = r*2
                eval.append(size)
            ind = eval.index(max(eval))
            faces = faces.tolist()
            faces = [faces[ind]]

        # zoom a bit more than usual
        for (x, y, w, h) in faces:
            newx, newy,neww,newh = x+d,y+d,w-d,h-d
            r = max(neww, newh) / 2
            centerx = newx + neww / 2
            centery = newy + newh / 2
            nx = int(centerx - r)
            ny = int(centery - r)
            nr = int(r * 2)
            faceimg = img[ny:ny+nr, nx:nx+nr]
            lastimg = cv2.resize(faceimg, (256, 256))

            return lastimg

        if (show_result):
            for (x, y, w, h) in faces:
                newx, newy, neww, newh = x, y, w - d, h - d
                cv2.rectangle(img, (newx, newy), (newx+neww, newy+newh), (255,0,0), 2)
            cv2.imshow('img', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


        # if store_result:
        #     cv2.imwrite("image%d.jpg" % i, faceimg)
        #     print("image is stored.")

if __name__ == '__main__':

    # Test run the following code to see if the image is correctly chopped.

    # image_path = os.getcwd()+"\\0530.jpg"
    #print(os.getcwd())

    # if (argc != 2):
    #     print('Usage: %s ' % image_path)
    #     quit()

    # faceDetector = FaceCropper()
    # img = faceDetector.generate(image_path, show_result=False, d=30)
    # print(img)
    # cv2.imwrite('image.jpg',img)
    # img = faceDetector.generate(image_path, show_result=False)
    # cv2.imwrite('image2.jpg', img)

    # Start to perform chopping to your dataset by doing the following
    
    
    image_path = path + "/data/test_images"
    if not os.path.exists(path + '/data/data_0'):
        os.makedirs(path + '/data/data_0')
    destination = path + "/data/data_0"
    if not os.path.isdir(destination):
        os.makedirs(destination)
    if os.path.isdir(image_path):
        file_names = glob.glob(image_path+"/*.jpg")
        faceDetector = FaceCropper()
        for i in range(len(file_names)):
            name = file_names[i]
            print(name)
            result = faceDetector.generate(name)
            if result is None:
                result = faceDetector.generate(file_names[i + 1])
                resname = destination + "/" + os.path.basename(name)
                cv2.imwrite(resname, result)

            else:
                resname = destination + "/" + os.path.basename(name)
                cv2.imwrite(resname, result)

        print("The Face Chopping is done!")