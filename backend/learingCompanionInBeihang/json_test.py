import json
import os

# 从 env.json 文件中加载环境变量
with open('env.json') as env_file:
    ENV = json.load(env_file)

# 从 ENV 中获取具体的环境变量
SECRET_KEY = ENV['SECRET_KEY']
JWT_LIFETIME = ENV['JWT_LIFETIME']
JWT_KEY = ENV['JWT_KEY']

# 打印环境变量以验证是否正确加载
print(f"SECRET_KEY: {SECRET_KEY}")
print(f"JWT_LIFETIME: {JWT_LIFETIME}")
print(f"JWT_KEY: {JWT_KEY}")