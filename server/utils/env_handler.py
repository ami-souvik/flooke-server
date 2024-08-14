import environ

env = environ.Env()

def get_env_variable(v):
    return env(v)

def get_dynamodb_conf():
    return {
        "region": env('DYNAMODB_REGION'),
        "host": "http://localhost:8000"
    }