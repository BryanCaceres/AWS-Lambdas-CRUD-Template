import subprocess
import os
import shutil
import platform

def build_layer():
    layer_path = "lambda-layers/flask-layer/python"
    if os.path.exists(layer_path):
        shutil.rmtree(layer_path)
    
    os.makedirs(layer_path, exist_ok=True)
    
    # Base command
    pip_args = [
        "pip",
        "install",
        "-r", "lambda-layers/flask-layer/requirements.txt",
        "-t", layer_path,
        "--upgrade"
    ]
    
    # Si estamos en ARM64 (M1/M2 Mac), agregamos flags especiales
    if platform.machine() == "arm64":
        pip_args.extend([
            "--platform", "manylinux2014_x86_64",
            "--only-binary=:all:",
            "--implementation", "cp",
            "--python-version", "38",
            "--no-deps"
        ])
        
        # Primero instalamos las dependencias base
        subprocess.check_call(pip_args)
        
        # Luego instalamos las dependencias secundarias sin restricciones de plataforma
        subprocess.check_call([
            "pip",
            "install",
            "-r", "lambda-layers/flask-layer/requirements.txt",
            "-t", layer_path,
            "--upgrade"
        ])
    else:
        # En x86_64, instalación normal
        subprocess.check_call(pip_args)

    print("Layer construida exitosamente")

if __name__ == "__main__":
    build_layer()