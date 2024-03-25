import subprocess
import time

# Iniciar el servidor
subprocess.Popen(["python", "server/app.py"])

# Esperar 10 segundos
time.sleep(10)

# Iniciar el script de detección
subprocess.Popen(["python", "model/detect.py"])