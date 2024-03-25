# Project Title: Coffee Inspection Application

This project is a Flask-based web application designed to inspect coffee using object detection. It uses SQLite for data persistence.

## Key Files

- `server/app.py`: This is the main file that runs the Flask application. It contains two routes: the home route (`/`) and the `register_detection` route.
- `services/detect.py`: This file is responsible for the detection service (not shown in the provided excerpts).

## Main Features

- **Home Route (`/`)**: This route returns a welcome message to the user: "Bienvenido a la aplicación Inspeccion de Cafe!".
- **Register Detection Route (`/register_detection`)**: This route accepts POST requests with JSON data containing the detected object and its confidence level. It connects to a SQLite database (`detections.db`), inserts the detection data into the `detections` table, and then closes the database connection. It returns a success message upon successful registration of the detected object.

## Ignored Files

The `.gitignore` file indicates that the following files and directories are not tracked by Git:

- `ai_env`
- `/runs`
- `yolov8l.pt`
- `server/yolov8n.pt`
- `services/yolov8n.pt`
- `services/yolov5su.pt`

These files are likely related to the AI model and environment used for object detection.

## Installation

To install the necessary dependencies, run the following command:
```sh
pip install -r requirements.txt
```

## How to Run

To run the server, navigate to the `server` directory and run `app.py`:

```sh
cd server
python app.py
```

The server will start in debug mode.

