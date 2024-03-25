from flask import Flask, request, jsonify
import sqlite3
import threading
import cv2
import requests
from ultralytics import YOLO
import time

# Inicialización del servidor Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenido a la aplicación de Inspección de Café!"

@app.route('/register_detection', methods=['POST'])
def register_detection():
    try:
        detection = request.get_json()
        object_ = detection.get('object')
        confidence = detection.get('confidence')

        if not object_ or not confidence:
            return jsonify({"error": "Missing object or confidence in request"}), 400

        conn = sqlite3.connect('detections.db')
        c = conn.cursor()

        c.execute("""
            INSERT INTO detections (object, confidence)
            VALUES (?, ?)
        """, (object_, confidence))

        conn.commit()
        conn.close()

        return jsonify({"message": "Detected object registered successfully!"}), 200

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

def run_flask_app():
    app.run(debug=False)  # Cambia debug a False para producción

# Función para manejar la detección y envío de datos
def run_detection():
    model = YOLO('yolov8n.pt')
    cap = cv2.VideoCapture(0)
    last_request_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        annotated_frame = results[0].plot()
        current_time = time.time()

        if current_time - last_request_time >= 5:
            for result in results[0]:
                class_id = result.boxes.cls.item()
                confidence = result.boxes.conf.item()
                data = {
                    'object': model.names[class_id],
                    'confidence': confidence
                }
                try:
                    response = requests.post('http://localhost:5000/register_detection', json=data)
                    print(response.text)
                except requests.exceptions.RequestException as e:
                    print(f'Error al enviar los datos al servidor: {e}')

            last_request_time = current_time

        cv2.imshow('YOLOv8 Detection', annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Crear e iniciar el hilo del servidor Flask
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    # Ejecutar la detección en el hilo principal
    run_detection()
