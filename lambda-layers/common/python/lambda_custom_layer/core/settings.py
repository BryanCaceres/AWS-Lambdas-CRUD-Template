import boto3

class Settings:
    def __init__(self):
        self.region_name = 'us-east-1'
        self.products_table = 'products'

settings = Settings()