import subprocess
import os

def build_layer():
    layer_path = "lambda-layers/flask-layer/python/lib/python3.8/site-packages"
    requirements_path = "lambda-layers/flask-layer/requirements.txt"

    os.makedirs(layer_path, exist_ok=True)
    subprocess.check_call([
        "pip",
        "install",
        "-r", requirements_path,
        "-t", layer_path
    ])

    print("Layer construida exitosamente")

if __name__ == "__main__":
    build_layer()