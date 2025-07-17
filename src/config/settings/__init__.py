import os

import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

DJANGO_ENV = env("DJANGO_ENV", default="dev").lower()

if DJANGO_ENV == "prod":
    from .prod import *
else:
    from .dev import *
