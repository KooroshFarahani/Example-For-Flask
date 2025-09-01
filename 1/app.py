#import flask
from flask import Flask, render_template, request
import os
import json

# فایل و لیست مرکزی
FEEDBACK_FILE = "feedbacks.json"
feedbacks = []  # لیست سراسری

app = Flask(__name__)

# بارگذاری داده‌ها هنگام شروع
def load_feedbacks():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_feedbacks(data):
    with open(FEEDBACK_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# بارگذاری اولیه داده‌ها
feedbacks = load_feedbacks()

@app.route('/survey')
def show_survey():
    return render_template("survey.html")

@app.route('/result', methods=['POST'])
def result():
    global feedbacks  # ✅ حتماً اضافه کن

    name = request.form.get('name')
    age = int(request.form.get('age'))
    feedback = request.form.get('feedback')

    # اضافه کردن نظر جدید به لیست سراسری
    feedbacks.append({
        'name': name,
        'age': age,
        'feedback': feedback
    })

    # ذخیره در فایل
    save_feedbacks(feedbacks)

    # پیام شخصی‌سازی شده
    if age > 18:
        message = "نظر شما ارزشمند است."
    else:
        message = "نظر جوانان همیشه الهام‌بخش است!"

    feedback_html = f"<p><strong>نظر شما:</strong> {feedback}</p>" if feedback else ""

    return f"""
    <h1>ممنون از شرکت تو، {name}!</h1>
    <p>{message}</p>
    {feedback_html}
    <br>
    <a href="/survey">بازگشت به فرم</a> |
    <a href="/all">مشاهده همه نظرها</a>
    """

@app.route('/all')
def all_feedbacks():
    if not feedbacks:
        return "<h3>هنوز نظری ثبت نشده!</h3><a href='/survey'>اولین نظر رو ثبت کن!</a>"

    result = "<h2>همه نظرها:</h2><ul>"
    for fb in feedbacks:
        result += f"<li><strong>{fb['name']}</strong> ({fb['age']} سال) گفت: '{fb['feedback']}'</li>"
    result += "</ul>"
    result += "<br><a href='/survey'>بازگشت</a>"
    return result

# سایر routeها (hello, profile, form) هم می‌تونن بمونن
# ...

if __name__ == '__main__':
    app.run(debug=True)