import cv2
import os
import numpy as np
from PIL import Image
from line_notify import LineNotify
from datetime import datetime
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials



class Face_functions:
    def __init__(self):
        self.dict_time  = {}
            
    def Start_get_data(self,ids,name):
        try:
            self.dict_time = np.load('database.npy',allow_pickle='TRUE').item()
        except:
            create_dic = {}
            np.save('database.npy',create_dic)
            self.dict_time = np.load('database.npy',allow_pickle='TRUE').item()
        
        self.dict_time[ids] = [name,int(time.time()),ids]
        cam = cv2.VideoCapture(0)
        cam.set(3, 400)
        cam.set(4, 400) 
        face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        face_id =  ids
        count = 0
        window_name = 'Get new face'
        #print(face_id)
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
                count += 1
                cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
                cv2.imshow(window_name, img)
            k = cv2.waitKey(100) & 0xff
            if k == 27:
                break
            elif count >= 50: 
                 break
        cam.release()
        cv2.destroyAllWindows()
        np.save('database.npy',self.dict_time)        
        return 'Get data complete'
        
    def trainModel(self):
        path = 'dataset'
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
 
        faceSamples=[]
        ids = []

        for imagePath in imagePaths:

            PIL_img = Image.open(imagePath).convert('L') 
            img_numpy = np.array(PIL_img,'uint8')

            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)
            #print('Id : ',id)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)
        recognizer.train(faceSamples, np.array(ids))
        recognizer.write('trainer/trainer.yml')
        print('Update complete')
    
    
        
        
    def scan_run(self):
        
        Database = np.load('database.npy',allow_pickle='TRUE').item()
        count_number = 2
        send_google_sheet_time = int(time.time()) + 30
        list_student_check = []
        
        #print('database', Database)
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer/trainer.yml')
        cascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        #iniciate id counter
        id = 0
        names = []
        name = ''
        # names related to ids: example ==> Marcelo: id=1,  etc
        
        for key,value in sorted(Database.items()):
            names.append(value[0])
            
        print('Name in database :',names )
        
        # Initialize and start realtime video capture
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video widht
        cam.set(4, 480) # set video height

        # Define min window size to be recognized as a face
        minW = 0.1*cam.get(3)
        minH = 0.1*cam.get(4)
        send_time = int(time.time()) + 10
        while True:

            ret, img =cam.read()
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
               )
            
            for(x,y,w,h) in faces:
                
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                
                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
                
                
                current_time = int(time.time())
                
                #print(count_number)
                if(current_time >= send_google_sheet_time ):
                    self.updateSheet(list_student_check , count_number)
                    
                    count_number = count_number + len(list_student_check) 
                    list_student_check = []
                    send_google_sheet_time = int(time.time()) + 30
                    
                        
                if (confidence < 100  and confidence >= 10):
                    
                    confidence = "  {0}%".format(round(100 - confidence))                                       
                    send_time = Database[str(id)][1]
                    name = Database[str(id)][0] # names[id-1]
                    # print('send_time', send_time)
                                        
                    if(current_time >= send_time ):                       
                        #print(name,current_time,send_time)
                        cv2.putText(img, str(name), (x+5,y-5), font, 1, (255,255,255), 2)
                        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
                        cv2.imwrite('image.jpg',img) 
                        time_now = str(datetime.now())
                        token = 'rkaEF5Bc2sK9fftszvZ80bnuNSK8XQFTa9YGkOxJydi'
                        list_student_check.append([str(id),str(name),time_now])
                        '''
                        try:
                            messsage = 'Name : '+ str(name)+'  Date :'+str(time_now)
                            notify  = LineNotify(token)
                            notify.send(messsage,image_path='./image.jpg')
                        except:
                            print('Please check internet')
                        '''
                        
                       
                        Database[str(id)][1] = int(time.time()) + 20
                        #print(Database[str(id)])
                        
                        
                    
                    
                else:
                    name = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))
                
                
                cv2.putText(img, str(name), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
                
            window_name = 'camera'
            #cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
            #cv2.setWindowProperty(window_name,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
            cv2.imshow(window_name,img) 

            k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break

       
        
        cam.release()
        cv2.destroyAllWindows()
    
    def updateSheet(self,lsit_student_check,star_data):
        
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('Python to Sheet-e59681cb97ad.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open("Student sheet").sheet1
        
        for number in range(len(lsit_student_check)):
             sheet.update_cell(number+star_data,1,number+star_data)
             sheet.update_cell(number+star_data,2,lsit_student_check[number][0])
             sheet.update_cell(number+star_data,3,lsit_student_check[number][1])
             sheet.update_cell(number+star_data,4,lsit_student_check[number][2])
             sheet.update_cell(number+star_data,5,'1')
   
        
