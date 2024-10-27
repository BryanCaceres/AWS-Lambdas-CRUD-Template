# Esto es una plantilla para crear una API Serverless en Python

## Para iniciar el servidor local

Con este comando se construye el proyecto en un contenedor de Docker
```bash
sam build --use-container
```

Con este comando se inicia el servidor local con los endpoints configurados en el template.yaml
```bash
sam local start-api
```
