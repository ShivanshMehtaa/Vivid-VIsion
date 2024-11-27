import cv2 as cv
import mediapipe
import pyautogui
import tkinter as tk
from PIL import Image, ImageTk  # Import Pillow for image conversion
from threading import Thread

class EyeMouseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Super Head Control")
        self.root.geometry("800x600")

        self.canvas = tk.Canvas(root, width=800, height=400)
        self.canvas.pack()

        self.status_label = tk.Label(root, text="Estado: Iniciando...", font=("Helvetica", 14))
        self.status_label.pack(pady=10)

        self.faceMesh = mediapipe.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        self.fr = cv.VideoCapture(0)

        self.screenWidth, self.screenHeight = pyautogui.size()

        self.update_frame()

    def update_frame(self):
        ret, image = self.fr.read()
        if not ret:
            print("No se pudo capturar la imagen")
            self.status_label.config(text="Estado: No se pudo capturar la imagen")
            self.root.after(10, self.update_frame)
            return

        image = cv.flip(image, 1)
        windowHieght, windowWidth, _ = image.shape

        rgbImage = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        processImage = self.faceMesh.process(rgbImage)
        allFaces = processImage.multi_face_landmarks

        if allFaces:
            oneFacePoints = allFaces[0].landmark

            rightEye = [oneFacePoints[374], oneFacePoints[386]]
            for id, landMark in enumerate(rightEye):
                x = int(landMark.x * windowWidth)
                y = int(landMark.y * windowHieght)

                if id == 1:
                    mouseX = int(self.screenWidth / windowWidth * x)
                    mouseY = int(self.screenHeight / windowHieght * y)
                    pyautogui.moveTo(mouseX, mouseY)

                cv.circle(image, (x, y), 2, (0, 255, 0))

            leftEye = [oneFacePoints[145], oneFacePoints[159]]
            for landMark in leftEye:
                x = int(landMark.x * windowWidth)
                y = int(landMark.y * windowHieght)
                cv.circle(image, (x, y), 2, (0, 0, 255))

            nose_landmark = oneFacePoints[1]
            nose_x = int(nose_landmark.x * windowWidth)
            nose_y = int(nose_landmark.y * windowHieght)


            rightEyeClosed = (rightEye[0].y - rightEye[1].y) < 0.01
            leftEyeClosed = (leftEye[0].y - leftEye[1].y) < 0.01

            if rightEyeClosed and leftEyeClosed:
                print("Both Eyes Closed -> Scrolling down")
                self.status_label.config(text="Estado: Ambos Ojos Cerrados -> Scroll abajo")
                pyautogui.scroll(-100)
            elif rightEyeClosed:
                print("Right Eye Closed -> Mouse clicked")
                self.status_label.config(text="Estado: Ojo Derecho Cerrado -> Click")
                pyautogui.rightClick()
                pyautogui.sleep(1)
            elif leftEyeClosed:
                print("Left Eye Closed -> Mouse clicked")
                self.status_label.config(text="Estado: Ojo Izquierdo Cerrado -> Click")
                pyautogui.click()
                pyautogui.sleep(1)
            else:
                self.status_label.config(text="Estado: Ojos abiertos")

        self.display_image(image)
        self.root.after(10, self.update_frame)

    def display_image(self, image):
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image = cv.resize(image, (800, 400))
        image = Image.fromarray(image)  # Convert OpenCV image to PIL image
        photo = ImageTk.PhotoImage(image)  # Convert PIL image to ImageTk.PhotoImage
        self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.canvas.image = photo  # Keep a reference to avoid garbage collection
        self.root.update_idletasks()

    def on_closing(self):
        self.fr.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EyeMouseApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
