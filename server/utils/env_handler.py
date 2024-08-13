import os

def get_env_variable(v):
    return os.environ.get(v)

def get_dynamodb_conf():
    return {
        "region": os.environ.get('DYNAMODB_REGION'),
        "host": os.environ.get('DYNAMODB_HOST')
    }