from envparse import Env
from dotenv import find_dotenv

env = Env()
APP_ENV = env.str("APP_ENV", default="LOCAL")

if APP_ENV == "TESTING":
    env_filename = ".env.testing"
elif APP_ENV == "LOCAL":
    env_filename = ".env.local"
else:
    env_filename = ".env.local"

env_path = find_dotenv(filename=env_filename, raise_error_if_not_found=True)
env.read_envfile(env_path)