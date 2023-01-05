print("Python Timelapse Camera V1.3")
print("By Oliver Hagen")

#This is pretty bad code- plenty of refactoring needed.

def help():
    print("""\nOVERVIEW OF FUNCTIONS:
capture() - Capture a timelapse.
help() - Shows this text.
render() - Render a timelapse.
view() - A viewfinder.
split() - Splits a video into frames.
getCameras() - Gets a list of available cameras
camSet(x) - Sets the camera to use to camera number 'x'

Hold control+c at any time to quit the programme.\n""")

try:
    import time
    import os
    import numpy as np
    from cv2 import VideoWriter, VideoWriter_fourcc
    import cv2
    help()
except: # Block is used to give a nice error message if some libraries aren't installed.
  print("\nYou don't have all of the required libraries to use this programme.")
  print("""This programme requires:
 - time
 - os
 - numpy
 - cv2""")

cameraToUse = 0

def getCameras():
    print("available sources are:")
    for i in range(-100000,100000):
        cap = cv2.VideoCapture(i)
        success,image = cap.read() 
        if success:
            print(i)
    cap.release()
    print("Set the camera you want to use with camSet(num)")

def camSet(num):
    global cameraToUse
    cameraToUse = num

def getSize(num):
    cap = cv2.VideoCapture(cameraToUse)#Opens camera for pictures
    for i in range(0,2):
        # This is looped because the first image the camera takes is without fail larger than subsequent images.
        # The first picture is therefore overwritten twice, giving us a filesize which is better for size estimation.
        # NOTE: The view() function below writes text to the image to assure users that nothing bogus is going on with these pictures, but
        # writing text to this image inflates the filesize, giving flawed estimation. Also, this image is only there for a very short amount of time, so there's no real point.
        return_value, image = cap.read()#saves a moment of camera input, called 'image'
        cv2.imwrite("CurrentView.jpg", image)#saves the image
    del(cap)#Closes the camera
    picSize = os.path.getsize("CurrentView.jpg")*0.9
    outputSize = round(picSize*num/1000000,1)
    print("This will take approximately ",outputSize,"MB")
    os.remove("CurrentView.jpg")#Deletes the unnecessary picture

def view():
    print("Press 'q' to return to the main programme.")
    cap = cv2.VideoCapture(cameraToUse)#Opens camera for pictures
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    return_value, image = cap.read()#saves a moment of camera input, called 'image'
    cv2.putText(image, "This image is used to get the dimensions of pictures taken by the camera,", (0,200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3)
    cv2.putText(image, "so that the preview window can be squished while preserving the aspect ratio of the video feed.", (0,240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
    cv2.putText(image, "It is deleted when the view() function is quit.", (0,280), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
    cv2.imwrite("CurrentView.jpg", image)#saves the image
    img = cv2.imread("CurrentView.jpg",1)#Opens the image to discern dimensions, and therefore scale the preview window properly
    height,width,test = img.shape
    #cap.set(3,int(width/(height/300)))#See above
    #cap.set(4,300)
    while(True):
        ret, frame = cap.read()# Same as above.
        cv2.imshow("preview",frame)
        cv2.resize(img, (int(width/(height/400)), 400))
        if cv2.waitKey(1) & 0xFF == ord("q"):#If the user presses 'q', this ends.
            del(cap)#Closes the camera
            cv2.destroyAllWindows()#Closes the preview window
            os.remove("CurrentView.jpg")#Deletes the unnecessary picture
            break

def capture():
    
    foldername = input("Please choose a name for this timelapse:\n")
    path = os.getcwd()
    try:os.mkdir(path+"/"+foldername)
    except:
        print("There's already a timelapse folder with that name, please try again.")
        return

    decide1 = int(input("""Choose a mode:
    1 - Take a certain number of pictures
    2 - Take pictures for a certain amount of time.
    """))#Options 1 and 2 reuse a lot of code, which I plan to refactor at some point.

    file = open("Log.txt","w")#Stores the time at which each picture is taken, for possible addition to the timelapse later.
    file.write("Working info for programme, DO NOT EDIT!\n")

    if decide1 == 1:
        count = 0
        number = int(input("How many pictures?"))
        interval = float(input("How often (Length of time between pictures, in seconds)?"))
        #getSize(number)
        cont = input("Press enter to start.")
        camera = cv2.VideoCapture(cameraToUse)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        starttime=str(time.ctime())
        message = str("Activated at: "+starttime)
        print(message)
        t1 = time.time()
        t2 = time.time()
        tstart = time.time()
        picnum = 1
        while count != number:
            if t2-t1 <= (interval):# As time.sleep() isn't very accurate, passing time is judged by difference between the time the last image was taken, and the current time.
                t2 = time.time()
            else:
                t1 = time.time()
                currenttime=str(time.ctime())
                print("Taking picture",count+1,"of",number," at",currenttime)
                message = currenttime
                file.write(str(message)+"\n")# Picture time is added to the file for later.
                message = str(picnum)+".jpg"# Picture is numbered for use by render() later.
                return_value, image = camera.read()
                cv2.imwrite(message, image)
                picnum=picnum+1
                count = count+1
                t2 = time.time()
        count = count+1

    elif decide1 == 2:
        number = int(input("How long to take pictures for (in minutes):"))
        interval = float(input("How often (Length of time between pictures, in seconds)?"))
        #getSize(number/interval*60)
        cont = input("Press enter to start.")
        camera = cv2.VideoCapture(cameraToUse)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        starttime=str(time.ctime())
        message = str("Activated at: "+starttime)
        print(message)
        count = 0
        numpics= int(number/interval*60)
        nownum = 0
        t1 = time.time()
        t2 = time.time()
        tstart = time.time()
        picnum = 1
        while count <= number*60:
            if t2-t1 <= interval:
                t2 = time.time()
            else:
                t3 = time.time()
                currenttime=str(time.ctime())
                print("Taking picture",nownum+1,"of",numpics," at",currenttime)
                message = currenttime
                file.write(str(message)+"\n")
                message = str(picnum)+".jpg"
                return_value, image = camera.read()
                cv2.imwrite(message, image)
                count = count+(t2-t1)
                nownum = nownum+1
                picnum = picnum+1
                t1 = t3
                t2 = time.time()
        count = picnum #To sort out disparity between variable names in different parts of the programme. I know.


    else:
        print("That's not an option; try again.")
        

    if decide1 == 1 or decide1 == 2:
        del(camera)#Camera is closed once picture-taking is done.
        tend = time.time()
        file.close()
        taken = tend-tstart
        taken = round(taken/60,2)
        print("DONE in",taken,"minutes.")
        haha = 1
        print("Tidying up...")
        os.rename(path+"/Log.txt", path+"/"+foldername+"/Log.txt")
        while(haha<=count-1):
            os.rename(path+"/"+str(haha)+".jpg", path+"/"+foldername+"/"+str(haha)+".jpg")
            haha = haha+1
        print("Done!")
    else:
        file.write("Program terminated due to user error.")
        file.close()

def render():

    foldername = input("Please choose a timelapse to render:\n")
    outputName = "./"+input("Please choose a name for the outputted timelapse movie:\n")+".mp4"
    FPS = int(input("Please choose a framerate for the outputted timelapse movie:\n"))
    timestamp = int(input("Superimpose timestamp? (1 = yes, 0 = no)\n"))
    
    if timestamp == 1:
        try:
            file = open(str(foldername+"/Log.txt"),"r")
            fileContents = file.readlines()
        except:
            timestamp = 0
            print("ERROR: No Log.txt found\nAs this file contains timestamp data and can't be found, no timestamp will be applied.")
    
    print("Now rendering...")

    path = os.getcwd()+"/"+foldername

    filename = path+"/1.jpg"
    img = cv2.imread(filename,1)
    height,width,test = img.shape

    pics = 0
    for root, dirs, files in os.walk(path):
        for file in files:    
            if file.endswith('.jpg'):
                pics += 1
    
    seconds = int((pics)/FPS)

    fourcc = VideoWriter_fourcc(*'h264')
    video = VideoWriter(outputName, fourcc, float(FPS), (width, height))

    t1 = time.time()
    t2 = time.time()
    tStart = time.time()
    broke = False
    count = 1
    
    for _ in range(FPS*seconds):
        filename = path+"/"+str(count)+".jpg"
        frame = cv2.imread(filename,1)
        if timestamp == 1:
            if (count>= len(fileContents)):
                message = "No time data"
                if broke == False:
                    print("Some timestamp data is missing!")
                    broke = True
            else:
                message = str(fileContents[count].strip("\n"))
            #This horrible block of code write the same text to the image in different positions (in black) around a central position, which is then written in white.
            #The effect of this is to create an outline around the text, ensuring legibilty against all backgrounds.
            #Usage is (image, text, pos(x,y), font, size, colour(R,G,B), stroke size (I think))
            cv2.putText(frame, message, (int(width/60)+3,int(height/20)+3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
            cv2.putText(frame, message, (int(width/60)-3,int(height/20)-3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
            cv2.putText(frame, message, (int(width/60)-3,int(height/20)+3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
            cv2.putText(frame, message, (int(width/60)+3,int(height/20)-3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
            cv2.putText(frame, message, (int(width/60),int(height/20)+3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
            cv2.putText(frame, message, (int(width/60),int(height/20)-3), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
            cv2.putText(frame, message, (int(width/60)+3,int(height/20)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
            cv2.putText(frame, message, (int(width/60)-3,int(height/20)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
            cv2.putText(frame, message, (int(width/60),int(height/20)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)
        video.write(frame)#Writes a finished frame to the .mp4 file
        count = count+1
        t2 = time.time()
        if t2-t1 >= 2:
            print(str(int(count/pics*100))+"%")#Progress updates are always nicer than a 'frozen' screen.
            t1 = time.time()
            t2 = time.time()
        
    video.release()#.mp4's done
    tEnd = time.time()
    print("Done, in "+str(round((tEnd-tStart), 2))+" seconds.")

def split():
    name  = input("name of file to split?\n")
    foldername = input("Folder to put frames in?\n")
    path = os.getcwd()
    try:os.mkdir(path+"/"+foldername)
    except:
        print("There's already a timelapse folder with that name, please try again.")
        return

    vidcap = cv2.VideoCapture(name)
    success,image = vidcap.read()
    count = 0
    while success:
      cv2.imwrite("%d.jpg" % count, image)     # save frame as JPEG file      
      success,image = vidcap.read()
      count += 1
      if count%100 == 0:
          print(count)
    print("Tidying up...")
    haha = 0
    while(haha<=count-1):
        os.rename(path+"/"+str(haha)+".jpg", path+"/"+foldername+"/"+str(haha)+".jpg")
        haha = haha+1
    print("Done!")
