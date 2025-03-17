# 설치하기 _ pip install pymongo python-dotenv
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# .env 파일이 있는 위치를 명시적으로 지정
load_dotenv(dotenv_path="C:/Users/병록/cat_jump/Jumpgame/.venv/Scripts/.env")

MONGO_URI = os.getenv("MONGO_URI")
print('dd',MONGO_URI)
# MongoDB 연결
client = MongoClient(MONGO_URI)
db = client["game_database"]
collection = db["users"]

# 데이터 삽입 테스트
def insert_mongo(id,pw):
    new_user = {"username": id, "password": pw}
    collection.insert_one(new_user)

print("회원가입 성공!")