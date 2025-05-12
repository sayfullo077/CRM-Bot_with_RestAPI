from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
BOT_USERNAME = env.str('BOT_USERNAME')
ADMINS = env.list('ADMINS')
HMAC_SECRET_KEY = env.str('HMAC_SECRET_KEY')
BASE_URL = env.str('BASE_URL')