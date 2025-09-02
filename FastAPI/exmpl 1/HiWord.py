from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import os

# مسیر فایل JSON
path = os.getcwd()
pat = os.path.join(path, 'users.json')

# بارگذاری کاربران از فایل JSON
users = []
try:
    if os.path.exists(pat):
        with open(pat, 'r') as f:
            users_data = json.load(f)
            # تبدیل دیکشنری‌ها به اشیاء User
            users = [User(**user_data) for user_data in users_data]
except (FileNotFoundError, json.JSONDecodeError):
    # اگر فایل وجود ندارد یا خالی است، لیست خالی نگه داشته می‌شود
    users = []

# تعریف مدل کاربر
class User(BaseModel):
    name: str
    email: str
    age: int

app = FastAPI()

# تمرین ۱: Hello World به فارسی
@app.get('/')
def hello_world():
    return "Hello World"

# تمرین ۲: دریافت اسم از URL
@app.get('/{name}/hi')
def hi_name(name: str):
    return {"message": f"hi {name}"}

# تمرین ۳: دریافت اطلاعات با کوئری
@app.get('/info')
def info(name: str, age: int = None):
    if age:
        return {"message": f"name = {name}, age = {age}"}
    return {"message": f"name = {name}"}

# تمرین ۴: عدد بعدی
@app.get('/{number}/number')
def number(number: int):
    result = number + 1
    return {"message": f"your next NUMBER is {result}"}

# تمرین ۵: جمع دو عدد
@app.get('/sum')
def sum(num1: float = None, num2: float = None):
    if num1 is not None and num2 is not None:
        result = num1 + num2
        return {"message": f"SUM: {result}"}
    elif num1 is None:
        return {"error": "number1 is not correct"}
    return {"error": "number2 is not correct"}

# تمرین: ایجاد کاربر
@app.post('/user')
def create_user(user: User):
    # بررسی وجود ایمیل در لیست کاربران
    for exist_user in users:
        if exist_user.email == user.email:
            raise HTTPException(status_code=400, detail="This email already exists")
    # بررسی سن کاربر
    if user.age < 13:
        raise HTTPException(status_code=400, detail="User must be older than 13")
    # افزودن کاربر به لیست
    users.append(user)
    # ذخیره لیست کاربران در فایل JSON
    with open(pat, 'w') as f:
        # تبدیل اشیاء User به دیکشنری برای ذخیره در JSON
        json.dump([user.dict() for user in users], f, indent=2)
    return {
        "message": "User created successfully",
        "name": user.name,
        "email": user.email,
        "age": user.age
    }

# تمرین: جستجوی کاربران
@app.get('/search')
def search():
    users_output = [
        {
            "نام": usr.name,
            "ایمیل": usr.email,
            "سن": usr.age
        } for usr in users
    ]
    return {"users": users_output}

# تمرین: به‌روزرسانی نام یا سن کاربر با ایمیل
@app.put('/user/{email}')
def update_user(email: str, user: User):
    for index, usr in enumerate(users):
        if usr.email == email:
            users[index] = user
            # ذخیره تغییرات در فایل JSON
            with open(pat, 'w') as f:
                json.dump([user.dict() for user in users], f, indent=2)
            return {
                "message": "User updated successfully",
                "name": user.name,
                "email": user.email,
                "age": user.age
            }
    raise HTTPException(status_code=404, detail=f"User with email {email} not found")

# تمرین: حذف کاربر
@app.delete('/user/{email}')
def delete_user(email: str):
    for index, usr in enumerate(users):
        if usr.email == email:
            users.pop(index)
            # ذخیره تغییرات در فایل JSON
            with open(pat, 'w') as f:
                json.dump([user.dict() for user in users], f, indent=2)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail=f"User with email {email} not found")