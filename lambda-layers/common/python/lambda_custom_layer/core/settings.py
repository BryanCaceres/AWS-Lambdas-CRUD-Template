
class Settings:
    def __init__(self):
        self.dynamodb_region_name = 'us-east-1'
        self.products_table = 'products'
        self.default_error_code = '500'
        self.default_error_message = 'Internal server error. Please try again later.'

settings = Settings()