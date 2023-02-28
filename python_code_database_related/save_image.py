import os
import face_recognition as facerecg

#making a sql file
import pyodbc
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=KHAOULA\SQLEXPRESS;'
                      'Database=face_recognition;'
                      'Trusted_Connection=yes;')
cur = conn.cursor()
print ("Label the Images properly")
#input folder path, checks the folder for .jpg file
path = input("Folder Path: ")
print ("Scanning for image files")

for files in os.listdir(path):
    if files.endswith(".jpg") or files.endswith(".png") or files.endswith(".jpeg"):
        print (f"Encoding {files}")
        #extract the name of file
        name = files.split(".")[0]
        # print (name)
        #extract the path of img file
        file_path = os.path.join(path,files)
        # #load the image file
        face = facerecg.load_image_file(file_path)
        # #encoding the image file
        face_encoding = facerecg.face_encodings(face)[0]
        ts = face_encoding.tobytes()
        # print (type(face_encoding))


        # entering values in SQL
        cur.execute("insert into ImageDB(Person, face) values(?, ?)", (name, ts))

#writing all the values in DB
conn.commit()
cur.close()
print("Successfully Add Image DB")
