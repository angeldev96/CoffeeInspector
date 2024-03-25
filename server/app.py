from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenido a la aplicación Inspeccion de Cafe!"

@app.route('/register_detection', methods=['POST'])
def register_detection():
    # Extraer información de la detección
    detection = request.get_json()
    object = detection['object']
    confidence = detection['confidence']

    # Conectar a la base de datos
    conn = sqlite3.connect('detections.db')
    c = conn.cursor()

    print("Database connection successful!")  # Mensaje en consola

    # Insertar la detección en la base de datos
    c.execute("""
        INSERT INTO detections (object, confidence)
        VALUES (?, ?)
    """, (object, confidence))

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

    print("Database connection closed.")  # Mensaje en consola

    return "Detected object registered successfully!"

if __name__ == '__main__':
    app.run()

