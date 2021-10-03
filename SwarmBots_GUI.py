import tkinter
import PIL.Image
import PIL.ImageTk
import cv2
from numpy.lib.shape_base import column_stack

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

class App:
    def __init__(self, window, video_source1, video_source2, video_source3, video_source4, video_source5):
        self.window = window
        self.window.title("SwarmBots")
        self.window.geometry('1095x625')
        self.window.config(bg = 'Black')
        self.window.resizable(0,0)

        C1 = tkinter.Label(window, text="Cam1")
        C1.config(fg="white", bg="gray", font=("Times New Roman", 15))
        C1.place(x=735, y=320)
        Btn1_in= tkinter.Button(window, text="Iniciar/Star")
        Btn1_in.config(fg="black", bg="green", font=("Times New Roman", 10))
        Btn1_in.place(x=790, y=320)
        Btn1_st= tkinter.Button(window, text="Detener/Stop")
        Btn1_st.config(fg="black", bg="red", font=("Times New Roman", 10))
        Btn1_st.place(x=860, y=320)

        C2 = tkinter.Label(window, text="Cam2")
        C2.config(fg="white", bg="gray", font=("Times New Roman", 15))
        C2.place(x=735, y=350)
        Btn2_in= tkinter.Button(window, text="Iniciar/Star")
        Btn2_in.config(fg="black", bg="green", font=("Times New Roman", 10))
        Btn2_in.place(x=790, y=350)
        Btn2_st= tkinter.Button(window, text="Detener/Stop")
        Btn2_st.config(fg="black", bg="red", font=("Times New Roman", 10))
        Btn2_st.place(x=860, y=350)

        C3 = tkinter.Label(window, text="Cam3")
        C3.config(fg="white", bg="gray", font=("Times New Roman", 15))
        C3.place(x=735, y=380)
        Btn3_in= tkinter.Button(window, text="Iniciar/Star")
        Btn3_in.config(fg="black", bg="green", font=("Times New Roman", 10))
        Btn3_in.place(x=790, y=380)
        Btn3_st= tkinter.Button(window, text="Detener/Stop")
        Btn3_st.config(fg="black", bg="red", font=("Times New Roman", 10))
        Btn3_st.place(x=860, y=380)

        C4 = tkinter.Label(window, text="Cam4")
        C4.config(fg="white", bg="gray", font=("Times New Roman", 15))
        C4.place(x=735, y=410)
        Btn4_in= tkinter.Button(window, text="Iniciar/Star")
        Btn4_in.config(fg="black", bg="green", font=("Times New Roman", 10))
        Btn4_in.place(x=790, y=410)
        Btn4_st= tkinter.Button(window, text="Detener/Stop")
        Btn4_st.config(fg="black", bg="red", font=("Times New Roman", 10))
        Btn4_st.place(x=860, y=410)

        C5 = tkinter.Label(window, text="Cam5")
        C5.config(fg="white", bg="gray", font=("Times New Roman", 15))
        C5.place(x=735, y=440)
        Btn5_in= tkinter.Button(window, text="Iniciar/Star")
        Btn5_in.config(fg="black", bg="green", font=("Times New Roman", 10))
        Btn5_in.place(x=790, y=440)
        Btn5_st= tkinter.Button(window, text="Detener/Stop")
        Btn5_st.config(fg="black", bg="red", font=("Times New Roman", 10))
        Btn5_st.place(x=860, y=440)

        self.video_source1 = video_source1
        self.video_source2 = video_source2
        self.video_source3 = video_source3
        self.video_source4 = video_source4
        self.video_source5 = video_source5
        self.photo1 = ""
        self.photo2 = ""
        self.photo3 = ""
        self.photo4 = ""
        self.photo5 = ""

        #Abrir video
        self.vid1 = MyVideoCapture(self.video_source1, self.video_source2, self.video_source3, self.video_source4, self.video_source5)

        #Cree un canvas que pueda ajustarse al tamaño de fuente de video anterior
        self.canvas1 = tkinter.Canvas(window, width=360, height=310)
        self.canvas2 = tkinter.Canvas(window, width=360, height=310)
        self.canvas3 = tkinter.Canvas(window, width=360, height=310)
        self.canvas4 = tkinter.Canvas(window, width=360, height=310)
        self.canvas5 = tkinter.Canvas(window, width=360, height=310)
        self.canvas1.place(x=0, y=0)
        self.canvas2.place(x=365, y=0)
        self.canvas3.place(x=730, y=0)
        self.canvas4.place(x=0, y=315)
        self.canvas5.place(x=365, y=315)

        #Después de llamarlo una vez, el método de actualización se llamará automáticamente cada milisegundos de retardo.
        self.delay = 1
        self.update()

        self.window.mainloop()
        

    def update(self):
        #Obtener un fotograma de la fuente de video
        ret1, frame1, ret2, frame2, ret3, frame3, ret4, frame4, ret5, frame5 = self.vid1.get_frame

        if ret1 and ret2 and ret3 and ret4 and ret5:
                self.photo1 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame1))
                self.photo2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame2))
                self.photo3 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame3))
                self.photo4 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame4))
                self.photo5 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame5))
                self.canvas1.create_image(0, 0, image=self.photo1, anchor=tkinter.NW)
                self.canvas2.create_image(0, 0, image=self.photo2, anchor=tkinter.NW)
                self.canvas3.create_image(0, 0, image=self.photo3, anchor=tkinter.NW)
                self.canvas4.create_image(0, 0, image=self.photo4, anchor=tkinter.NW)
                self.canvas5.create_image(0, 0, image=self.photo5, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source1, video_source2, video_source3, video_source4, video_source5):
        #Abra la fuente de video
        self.vid1 = cv2.VideoCapture(video_source1)
        self.vid2 = cv2.VideoCapture(video_source2)
        self.vid3 = cv2.VideoCapture(video_source3)
        self.vid4 = cv2.VideoCapture(video_source4)
        self.vid5 = cv2.VideoCapture(video_source5)

        if not self.vid1.isOpened():
            raise ValueError("No se puede abrir la fuente de video", video_source1, video_source2, video_source3, video_source4, video_source5)

    @property
    def get_frame(self):
        ret1 = ""
        ret2 = ""
        ret3 = ""
        ret4 = ""
        ret5 = ""
        if self.vid1.isOpened() and self.vid2.isOpened() and self.vid3.isOpened() and self.vid4.isOpened() and self.vid5.isOpened():
            ret1, frame1 = self.vid1.read()
            frame1 = deteccion_facilal(frame1)
            ret2, frame2 = self.vid2.read()
            frame2 = deteccion_facilal2(frame2)
            ret3, frame3 = self.vid3.read()
            frame3 = deteccion_facilal2(frame3)
            ret4, frame4 = self.vid4.read()
            frame4 = deteccion_facilal2(frame4)
            ret5, frame5 = self.vid5.read()
            frame5 = deteccion_facilal2(frame5)
            frame1 = cv2.resize(frame1, (360, 310))
            frame2 = cv2.resize(frame2, (360, 310))
            frame3 = cv2.resize(frame3, (360, 310))
            frame4 = cv2.resize(frame4, (360, 310))
            frame5 = cv2.resize(frame5, (360, 310))
            if ret1 and ret2 and ret3 and ret4 and ret5:
                #Devuelve un indicador de éxito booleano y el fotograma actual convertido a BGR
                return ret1, cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB), ret2, cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB), ret3, cv2.cvtColor(frame3, cv2.COLOR_BGR2RGB), ret4, cv2.cvtColor(frame4, cv2.COLOR_BGR2RGB), ret5, cv2.cvtColor(frame5, cv2.COLOR_BGR2RGB)
            else:
                return ret1, None, ret2, None, ret3, None, ret4, None, ret5, None
        else:
            return ret1, None, ret2, None, ret3, None, ret4, None, ret5, None

    #Suelta la fuente de video cuando el objeto sea destruido.
    def __del__(self):
        if self.vid1.isOpened():
            self.vid1.release()
        if self.vid2.isOpened():
            self.vid2.release()
        if self.vid3.isOpened():
            self.vid3.release()
        if self.vid4.isOpened():
            self.vid4.release()
        if self.vid5.isOpened():
            self.vid5.release()

#Deteccion Facial de cada camara IP 
def deteccion_facilal(frame1):
    gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        frame1 = cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame1

def deteccion_facilal2(frame2):
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    faces2 = faceClassif.detectMultiScale(gray2, 1.3, 5)
    for (x, y, w, h) in faces2:
        frame2 = cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame2

def deteccion_facilal3(frame3):
    gray3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)
    faces3 = faceClassif.detectMultiScale(gray3, 1.3, 5)
    for (x, y, w, h) in faces3:
        frame3 = cv2.rectangle(frame3, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame3

def deteccion_facilal4(frame4):
    gray4 = cv2.cvtColor(frame4, cv2.COLOR_BGR2GRAY)
    faces4 = faceClassif.detectMultiScale(gray4, 1.3, 5)
    for (x, y, w, h) in faces4:
        frame4 = cv2.rectangle(frame4, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame4

def deteccion_facilal5(frame5):
    gray5 = cv2.cvtColor(frame5, cv2.COLOR_BGR2GRAY)
    faces5 = faceClassif.detectMultiScale(gray5, 1.3, 5)
    for (x, y, w, h) in faces5:
        frame5 = cv2.rectangle(frame5, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame5

def callback():
    global v1,v2,v3,v4,v5
    v1=E1.get()
    v2=E2.get()
    v3=E3.get()
    v4=E4.get()
    v5=E5.get()
    if v1 == "" or v2 == "" or v3 == "" or v4 == "" or v5 == "":
        L6.place(x=650 ,y=300)
        return
    initial.destroy()

#Ventana de configuracion de Camaras de los robots
initial = tkinter.Tk()
initial.geometry('1080x620')
initial.config(bg ='midnightblue')
initial.title('Camaras IP')
initial.resizable(0,0)

initial.title("Swarm Bots")
L0 = tkinter.Message(initial, bg='midnightblue', fg="White", font=("Times New Roman", 12),
text="Ingresa las direcciones IP en el siguiente formato: IP:PORT/video\n"
"Input the IP directions in the next format: IP:PORT/video", aspect=900)
L0.place(x=640, y=100)

L1 = tkinter.Label(initial, text="    Cam1   ")
L1.place(x=650, y=150)
E1 = tkinter.Entry(initial, bd =2)
E1.place(x=710, y=150)
L2 = tkinter.Label(initial, text="    Cam2   ")
L2.place(x=650, y=174)
E2 = tkinter.Entry(initial, bd =2)
E2.place(x=710, y=174)
L3 = tkinter.Label(initial, text="   Cam3    ")
L3.place(x=650, y=198)
E3 = tkinter.Entry(initial, bd =2)
E3.place(x=710, y=198)
L4 = tkinter.Label(initial, text="   Cam4    ")
L4.place(x=650, y=222)
E4 = tkinter.Entry(initial, bd =2)
E4.place(x=710, y=222)
L5 = tkinter.Label(initial, text="   Cam5    ")
L5.place(x=650, y=246)
E5 = tkinter.Entry(initial, bd =2)
E5.place(x=710, y=246)
B = tkinter.Button(initial, text ="Siguiente/Next", command = callback)
B.place(x=650, y=270)
L6 = tkinter.Label(initial, text="Ingresa todas la direeciones IP/Please insert all IP directions")

L7 = tkinter.Label(initial, text="Bienvendo")
L7.config(fg="white", bg="midnightblue", font=("Times New Roman", 40))
L7.place(x=120, y=50)
L8 = tkinter.Message(initial, text="En la interfaz grafica puede configurar las camaras IP"
                     " para visualizar el stream de los robots", aspect=225)
L8.config(fg="white", bg="midnightblue", font=("Times New Roman", 20))
L8.place(x=120, y=120)

L9 = tkinter.Label(initial, text="Wellcome")
L9.config(fg="white", bg="midnightblue", font=("Times New Roman", 40))
L9.place(x=120, y=350)
L10 = tkinter.Message(initial, text="In the GUI you can configure the IP cameras"
                     " to view the stream of the robots", aspect=225)
L10.config(fg="white", bg="midnightblue", font=("Times New Roman", 20))
L10.place(x=120, y=420)

initial.mainloop()

# Crea una ventana y pásala al objeto Aplicacion
App(tkinter.Tk(),v1, v2, v3, v4, v5)
