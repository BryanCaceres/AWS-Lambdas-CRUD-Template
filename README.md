# Template to create a Serverless API in Python using SAM serverless application model and AWS Lambdas

![Example Diagram](https://file.notion.so/f/f/ca222c1a-d0ee-480a-95c4-19cbd36ebe72/d8c47a51-89d7-42e5-969b-dfdbabeb417b/Lambda_Diagram-snippet.png?table=block&id=14a17ae1-a7a9-80f7-b773-e5cc88af5f75&spaceId=ca222c1a-d0ee-480a-95c4-19cbd36ebe72&expirationTimestamp=1732680000000&signature=m_WUD-i7Cq_d1Cs-CmniIgfWHz1P1yim3jUsj9HS86U&downloadName=Lambda+Diagram-snippet.png)

This template includes:

- A Lambda Layer with common dependencies shared across lambdas
- Centralized configuration for the lambda functions using SSM parameters
- Centralized API responde and error handling using a lambda_handler decorator
- Use of AWS X-Ray and Powertools to trace the requests and traces
- A lambda function to get all items from a DynamoDB table with pagination
- A lambda function to get a single item from a DynamoDB table
- A lambda function to create a new item in a DynamoDB table
- A lambda function to update an existing item in a DynamoDB table
- A lambda function to delete an existing item in a DynamoDB table
- A API Key validation using API Gateway
- Basic example of API Gateway models to validate the request body and parameters in POST and PATH methods

Prerequisites:
- AWS SDK installed
- AWS CLI installed
- AWS SAM Framework installed

# First, what is SAM?

AWS SAM (Serverless Application Model) is a user-friendly open-source framework that simplifies building, testing, and deploying serverless applications on AWS. 

With SAM, you can easily define resources like Lambda functions and API Gateway endpoints in a simple YAML file, allowing you to focus on your code. It integrates smoothly with AWS CloudFormation for features like versioning and rollback, ensuring your applications are reliable and scalable. Plus, you can test locally, making debugging a breeze. 

Overall, SAM streamlines serverless development and enhances team collaboration. For more info, check out the [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)


Associated Links:
[AWS SAM](https://docs.aws.amazon.com/es_es/serverless-application-model/latest/developerguide/serverless-getting-started.html)
[AWS SDK](https://aws.amazon.com/es/sdk-for-python/)
[AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions)

## Step by Step

### Build the Layer with Dependencies and custom code shared across all Lambdas

```bash
cd lambda-layers/common
pip install -r python/lambda_custom_layer/requirements.txt -t python/
```

### Build the Project in a Docker Container

```bash
sam build --use-container
```

### Start the Local Server with Endpoints Configured in template.yaml
This allows you to test the endpoints locally.

```bash
sam local start-api --port 3002
```

### Deploy the Project on AWS
Before deploying, it’s recommended to test any changes in your template.yaml locally to avoid syntax errors.

```bash
sam validate --lint
```

Once your template.yaml has been tested locally, you can deploy the project to AWS.

(Recommended for validating configurations during deployment)

```bash
sam deploy --guided
```
or directly:

bash
Copy code

```bash
sam deploy
```
# Disclaimer

This is a simple example to get you started quickly. You can expand it to include more features/services as needed and improve the code.

Points to consider for inclusion or modifications that may interest you:
- Implement validations not only with API Gateway models, but you should see if the additional weight added by the validation libraries is worth it.
- Improve the services that modify things in DynamoDB to incorporate transactions if your use case requires it.
- Replace DynamoDB with your database if needed, as this is an example with a products table.
- Add tests.
- Replace the use of API Key with authentication using Cognito or a custom authorizer.


# Useful additional Documentation

AWS Recommended Best Practices for Lambdas:
[Python recommendations](https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html)

