import cv2
import time
import numpy as np

def nothing(x):
    pass

def capture():
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Capture tools")

 
    #cv2.createTrackbar('key S to capture picture','test',0,1,nothing)
    
    cv2.createTrackbar('Number of capture images in one second','Capture tools',1,30,nothing)
    cv2.createTrackbar('Last time(seconds)','Capture tools',1,60,nothing)

    img_counter = 1 
    round_capture = 0
    boolSave = False
    capture_images_number=1

    while True:

        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break

        
        frame_ori=frame.copy()

        img = np.zeros((70,640, 3), np.uint8) # image for put text

        img[:]=(255,255,255) # set background to black

        cv2.putText(img,"S to capture image", (10, 15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(img,"Q to quit", (560, 60), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(img,"C to run Number of capture images in one second and Last time", (10, 35), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 0), 1, cv2.LINE_AA)

        frame=np.vstack((frame,img)) # combine two image
        
        #cv2.imshow("test", cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))


        cv2.imshow('Capture tools', frame)

        continous_t = cv2.getTrackbarPos('Last time(seconds)','Capture tools') # duration time
        continous_s = cv2.getTrackbarPos('Number of capture images in one second','Capture tools') #number of capture images

        k = cv2.waitKey(1)

        if k  & 0xFF == ord('q'):
            # q pressed
            print("Escape hit, closing...")
            break

        elif k & 0xFF == ord('s'):
            # s pressed
            img_name = "opencv_frame_{}.jpg".format(img_counter)
            cv2.imwrite(img_name, frame_ori)
            print("{} written!".format(img_name))
            img_counter += 1

        elif k & 0xFF == ord('c'):
            boolSave = True
            round_capture+=1 # continous capture add 
            round_image_counter = 1 # continous capture image
            FPS= 1/continous_s #  FPS calcuate 
            start=time.time() # start time


        if boolSave==True and time.time()-start > FPS and  round_image_counter <= (continous_t*continous_s) :  # image/s   and  last time 

            #print(FPS,round_image_counter,continous_t,continous_s)
            print("Round {0} image {1}\t ".format(round_capture,round_image_counter))
            img_name = "opencv_frame_round_{0}_{1}.jpg".format(round_capture,round_image_counter)

            cv2.imwrite(img_name, frame_ori)

            print("{} written!".format(img_name))

            round_image_counter+=1

            start=time.time()

            if round_image_counter > continous_t*continous_s:
                round_image_counter =0
                FPS=0
                boolSave =False


              
    
    cam.release()
    cv2.destroyAllWindows()

def main():
    capture()

if __name__ == '__main__':

    main()
