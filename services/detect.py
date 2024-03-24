import cv2
import requests
from ultralytics import YOLO

# Cargar el modelo YOLOv8
model = YOLO('yolov8n.pt')

# Inicializar la captura de video desde la webcam
cap = cv2.VideoCapture(0)

while True:
    # Leer un frame de la webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Realizar la detección de objetos en el frame
    results = model(frame)

    # Visualizar los resultados en el frame
    annotated_frame = results[0].plot()

    # Iterar sobre las detecciones
    for result in results[0]:
        class_id = result.boxes.cls.item()
        confidence = result.boxes.conf.item()

        # Enviar los datos de la detección al servidor Flask
        data = {
            'object': model.names[class_id],
            'confidence': confidence
        }

        try:
            response = requests.post('http://localhost:5000/register_detection', json=data)
            print(response.text)
        except requests.exceptions.RequestException as e:
            print(f'Error al enviar los datos al servidor: {e}')

    # Mostrar el frame con las detecciones
    cv2.imshow('YOLOv8 Detection', annotated_frame)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos
cap.release()
cv2.destroyAllWindows()
