from fastapi import FastAPI
from pydantic import BaseModel

users=[]
#یه کلاس کاربر بساز با دو فیلد: نام و ایمیل
class user(BaseModel):
    name:str
    email:str
    age:int

app=FastAPI()
# تمرین ۱: Hello World به فارسی
@app.get('/')
def Hello_World():
    return "Hello World"

# تمرین ۲: دریافت اسم از URL
@app.get('/{name}/hi')
def hi_name(name:str):
    return {"massage" :f" hi {name}"}

#تمرین ۳: دریافت اطلاعات با کوئری
@app.get('/info')
def info(name:str,age:int=None):
    if age:
        return{
            "massage": f"name = {name} , age = {age}"
        }
    else:
        return{f"{name}"}

#تمرین ۴: عدد بعدی
@app.get('/{number}/number')
def Number(number:int):
    result=number+1
    return{f"your next NUMBER is {result}"}

# تمرین ۵: جمع دو عدد
@app.get('/sum')
def Sum(num1:float=None,num2:float=None):
    result=0
    if num1:
        if num2:
            result=num1+num2
            return{f"SUM:{result}"}
        else:
            return{f"number2 is not corect"}
    else:
        return{f"number1 is not corect"}

@app.post('/user')
def create_user(user:user):
    # بررسی وجود ایمیل در لیست کاربران
    for exist_user in users:
        if exist_user.email == user.email:
            return {"ERROR":"this email is exist"}
    # بررسی سن کاربر
    if user.age<13:
        return{"ERROR":"User most older than 13"}
    # افزودن کاربر به لیست
    else:
        users.append(user)
        return {
        "massage ": "user create success full",
        "NAME" :  user.name,
        "Email" : user.email,
        "Age" : user.age,
        }
    
@app.get('/search')
def search():
    users_output = []
    for usr in users:
            users_output.append({
            "نام": usr.name,
            "ایمیل": usr.email,
            "سن": usr.age
        })
    return {"users " : users_output}

    
