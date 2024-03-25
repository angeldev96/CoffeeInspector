from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenido a la aplicación Inspeccion de Cafe!"

@app.route('/register_detection', methods=['POST'])
def register_detection():
    try:
        # Extraer información de la detección
        detection = request.get_json()
        object = detection.get('object')
        confidence = detection.get('confidence')

        if not object or not confidence:
            return jsonify({"error": "Missing object or confidence in request"}), 400

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

        return jsonify({"message": "Detected object registered successfully!"}), 200

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run()