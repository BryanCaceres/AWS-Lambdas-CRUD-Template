# Esto es una plantilla para crear una API Serverless en Python con Flask

Prerequisitos:
- Tener instalado el SDK de AWS
- Tener instalado el CLI de AWS
- Tener instalado el framework de AWS SAM

Link asociados:
[AWS SAM](https://docs.aws.amazon.com/es_es/serverless-application-model/latest/developerguide/serverless-getting-started.html)
[AWS SDK](https://aws.amazon.com/es/sdk-for-python/)
[AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions)

## Paso a Paso

### Construir la capa con las dependencias de Flask

```bash
python build_layer.py
```

### Construir el proyecto en un contenedor de Docker
```bash
sam build --use-container
```

### Iniciar el servidor local con los endpoints configurados en el template.yaml

Esto te permitirá probar los endpoints en tu máquina local

```bash
sam local start-api
```

### Desplegar el proyecto en AWS

```bash
sam deploy --guided
```
