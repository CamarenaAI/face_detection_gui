import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import threading
import time

# ------------------- Global Variables ------------------- #
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# ------------------- Video capture class ------------------- #
class MyVideoCapture:
    def __init__(self, source, controller):
        self.controller = controller
        self.video = cv2.VideoCapture(source)
        self.ret = False
        self.frame = None
        self.running = True
        self.lock = threading.Lock()
        threading.Thread(target=self.update, daemon=True).start()

    def update(self):
        while self.running:
            ret, frame = self.video.read()
            if ret:
                frame = cv2.resize(frame, (360, 310))
                if self.controller.face_detection_enabled:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = faceClassif.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                with self.lock:
                    self.ret = ret
                    self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                time.sleep(0.01)

    def get_frame(self):
        with self.lock:
            return self.ret, self.frame.copy() if self.frame is not None else None

    def release(self):
        self.running = False
        self.video.release()

# ------------------- Main view with view control ------------------- #
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Face Detector")
        self.iconbitmap('cam.ico')
        self.state('zoomed')
        self.configure(bg='midnightblue')
        self.face_detection_enabled = True
        self.video_sources = []
        self.frames = {}

        container = tk.Frame(self, bg='midnightblue')
        container.pack(fill="both", expand=True)

        for F in (LoginPage, MainMenu, CameraView):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# ------------------- Login Page ------------------- #
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='midnightblue')
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        # Text in Spanish above left
        top_left = tk.Frame(self, bg='midnightblue')
        top_left.grid(row=0, column=0, sticky="nw", padx=150, pady=100)
        tk.Label(top_left, text="Bienvendo", font=("Times New Roman", 40), bg='midnightblue', fg='white').pack(anchor='w')
        tk.Label(top_left, text="En la interfaz grafica puede configurar las\ncamaras IP para visualizar\nel stream de los robots",
                 font=("Times New Roman", 20), bg='midnightblue', fg='white', justify='left').pack(anchor='w')

        # Text in English above left
        bottom_left = tk.Frame(self, bg='midnightblue')
        bottom_left.grid(row=1, column=0, sticky="sw", padx=150, pady=100)
        tk.Label(bottom_left, text="Welcome", font=("Times New Roman", 40), bg='midnightblue', fg='white').pack(anchor='w')
        tk.Label(bottom_left, text="In the GUI you can configure the IP cameras\nto view the stream of the robots",
                 font=("Times New Roman", 20), bg='midnightblue', fg='white', justify='left').pack(anchor='w')

        # Centered form
        center = tk.Frame(self, bg='midnightblue')
        center.grid(row=0, column=1, rowspan=2)

        tk.Message(center, text="Ingresa las direcciones IP en el siguiente formato: IP:PORT/video\nInput the IP directions in the next format: IP:PORT/video",
                   font=("Times New Roman", 13), bg='midnightblue', fg='white', aspect=900).pack(pady=10)

        self.entries = []
        for i in range(5):
            row = tk.Frame(center, bg='midnightblue')
            row.pack(pady=5)
            tk.Label(row, text=f"Cam{i+1}", bg='midnightblue', fg='white').pack(side='left')
            entry = tk.Entry(row, width=35)
            entry.pack(side='left')
            self.entries.append(entry)

        tk.Button(center, text="Siguiente/Next", command=self.procesar).pack(pady=15)

    def procesar(self):
        ips = [e.get() for e in self.entries]
        if not any(ips):
            messagebox.showwarning("Advertencia", "Debes ingresar al menos una dirección IP")
            return
        self.controller.video_sources = ips
        self.controller.show_frame(MainMenu)

# ------------------- Main menu ------------------- #
class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='midnightblue')
        self.controller = controller

        tk.Label(self, text="Menú Principal/Main Menu", bg='midnightblue', fg='white', font=("Arial", 50)).pack(pady=20)
        tk.Button(self, text="Ver Cámaras IP/Show IP Cameras", bg='green', fg='white', command=lambda: controller.show_frame(CameraView)).pack(pady=10)

        self.toggle = tk.IntVar(value=1)
        tk.Checkbutton(self, text="Detección facial/Facial Detection", bg='midnightblue', variable=self.toggle, command=self.actualizar_toggle).pack()

        tk.Button(self, text="Cerrar sesión/Exit", bg='red', fg='white', command=lambda: controller.show_frame(LoginPage)).pack(pady=20)

    def actualizar_toggle(self):
        self.controller.face_detection_enabled = bool(self.toggle.get())

# ------------------- Show IP Cameras ------------------- #
class CameraView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='midnightblue')
        self.controller = controller
        self.labels = []
        self.videos = []
        self.running = False

        tk.Label(self, bg='midnightblue', fg="white", text="Vista de Cámaras/Camera View", font=("Arial", 25)).pack(padx=10)
        tk.Button(self, bg="red", fg="white", text="Volver/Return", command=self.detener_y_volver).pack(padx=10)

        self.grid_frame = tk.Frame(self, bg="midnightblue")
        self.grid_frame.pack()

        for i in range(5):
            label = tk.Label(self.grid_frame)
            label.grid(row=i//3, column=i%3, padx=10, pady=10)
            self.labels.append(label)

    def tkraise(self):
        super().tkraise()
        if not self.running:
            self.iniciar_videos()

    def iniciar_videos(self):
        self.videos.clear()
        self.running = True
        for src in self.controller.video_sources:
            if src:
                self.videos.append(MyVideoCapture(src, self.controller))
            else:
                self.videos.append(None)
        self.actualizar()

    def actualizar(self):
        for i, cap in enumerate(self.videos):
            if cap:
                ret, frame = cap.get_frame()
                if ret:
                    img = ImageTk.PhotoImage(Image.fromarray(frame))
                    self.labels[i].configure(image=img)
                    self.labels[i].image = img
        if self.running:
            self.after(33, self.actualizar)

    def detener_y_volver(self):
        self.running = False
        for cap in self.videos:
            if cap:
                cap.release()
        self.controller.show_frame(MainMenu)

# ------------------- Launch ------------------- #
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()