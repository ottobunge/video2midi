import cv2 


class VideoReader:
    def __init__(self, file_path):
        self.fp = file_path

    def read(self):
        video = cv2.VideoCapture(self.fp)
        currentframe = 0
        while(True): 
            ret, frame = video.read() 

            if ret: 
                currentframe += 1
                yield currentframe, frame
            else: 
                break
        video.release() 
        cv2.destroyAllWindows()
