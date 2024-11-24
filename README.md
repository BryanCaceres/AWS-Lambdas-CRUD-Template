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

### Construir la capa con las dependencias compartidas por las lambdas

```bash
cd lambda-layers/common
pip install -r python/lambda_custom_layer/requirements.txt -t python/
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

Previo a desplegar recomiendo que cualquier cambio en tu template.yaml sea probado localmente para evitar errores de sintaxis.

```bash
sam validate --lint
```

Después de haber probado localmente tu template.yaml, puedes desplegar tu proyecto en AWS.

(Recomendado para validar configuraciones al desplegar)
```bash
sam deploy --guided
```
o 

```bash
sam deploy
```

# Documentación útil

Buenas prácticas recomendadas por AWS para lambdas:
[Recomendaciones para Python](https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html)