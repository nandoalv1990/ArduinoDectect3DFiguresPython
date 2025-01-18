#Demo
#Fernando Alvarez Delgadillo
#Programa que detecta movimiento e imprime el nombre de la figura en base a sus dimensiones captadas (cubo, piramide y cilindro) con numpy
import cv2
import numpy as np
import time
import os
os.environ['OPENCV_LOG_LEVEL'] = 'SILENT'


try:
     import serial
     arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
     time.sleep(2)
     arduino_conectado = True
except (serial.SerialException, ModuleNotFoundError):
    print("No se detectó arduino")
    arduino_conectado = False
    
def enviar_a_arduino(mensaje):
    """Conected."""
    if arduino_conectado:
        try:
            arduino.write(f"{mensaje}\n".encode())
        except Exception as e:
            print(f"Error al enviar al Arduino:{e}")
    
def detectar_figura(contorno):
    """Identifica figuras en 3D"""
    epsilon = 0.04 * cv2.arcLength(contorno, True)
    aprox = cv2.approxPolyDP(contorno, epsilon, True)
    vertices = len(aprox)
    
    if vertices == 4:
        return "cubo"
    elif vertices == 3:
        return "Piramide"
    else:
        area = cv2.contourArea(contorno)
        (x,y), radio = cv2.minEnclosingCircle(contorno)
        area_circulo = np.pi*(radio**2)
        
        if 0.8 < area/area_circulo < 1.2:
            return "cilindro"
    return None

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

if not cap.isOpened():
    print("Error al abrir la cámara")
    exit()
    
    print("Teclea 'q' para salir")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar")
            break
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        desenfoque = cv2.GaussianBlur(gris, (5,5), 0)
        _, umbral = cv2.threshold(desenfoque, 60, 255, cv2.THRESH_BINARY_INV)
        
        contornos, _=cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contorno in contornos:
            if cv2.contourArea(contorno) > 500:
                figura = dectectar_figura(contorno)
                if figura:
                    x, y, w, h = cv2.boundingRect(contorno)
                    cv2.reactangle(frame, (x,y), (x+w,y+h), (0,255,0),2)
                    cv2.putText(frame, figura, (x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
                    
                    enviar_a_arduino(figura)
                    print(f"Figura dectectada: {figura}")
                    
            cv2.imshow("Dectección de figuras", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
    cap.realease()
    cv2.destroyAllWindows()
    if arduino_conectado:
        arduino.close()