import time, random, os
from instagrapi import Client

# 1. جلب بيانات الدخول من المتغيرات البيئية
USERNAME = os.environ.get('IG_USERNAME')
PASSWORD = os.environ.get('IG_PASSWORD')

# 2. جلب الحسابات المستهدفة (سيتم إدخالها في المنصة مفصولة بفاصلة، وسيقوم الكود بتحويلها لقائمة)
targets_env = os.environ.get('IG_TARGETS', '')
TARGETS = [t.strip() for t in targets_env.split(',') if t.strip()]

# 3. جلب أوقات التوقف (مع وضع 10 و 30 كقيم افتراضية في حال لم تقم بإضافتها)
SLEEP_MIN = int(os.environ.get('SLEEP_MIN', 10))
SLEEP_MAX = int(os.environ.get('SLEEP_MAX', 30))

# 4. فحص أمان للتأكد من وجود بيانات الدخول قبل تشغيل البوت
if not USERNAME or not PASSWORD:
    print("خطأ: يرجى التأكد من إضافة IG_USERNAME و IG_PASSWORD في إعدادات المنصة السحابية.")
    exit()

if not TARGETS:
    print("تنبيه: لم يتم العثور على أهداف (IG_TARGETS) للعمل عليها.")

# 5. تهيئة البوت وتسجيل الدخول
cl = Client()
cl.set_user_agent("Instagram 219.0.0.12.117 Android (29/10; 320dpi; 720x1280; Xiaomi; Redmi 7A; pine; qcom; ar_EG)")

if os.path.exists("session.json"):
    print("تم العثور على جلسة سابقة، جاري تسجيل الدخول...")
    cl.load_settings("session.json")
    cl.login(USERNAME, PASSWORD)
else:
    print("لا توجد جلسة سابقة، جاري إنشاء جلسة جديدة...")
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings("session.json")

print("البوت يعمل بوضع الأتمتة...")

# 6. بدء عملية المتابعة
for target in TARGETS:
    print(f"جاري فحص حساب: {target}")
    try:
        user_id = cl.user_id_from_username(target)
        users = cl.user_followers(user_id, amount=5)
        
        for u_id, u_info in users.items():
            sleep_time = random.randint(SLEEP_MIN, SLEEP_MAX)
            time.sleep(sleep_time)
            cl.user_follow(u_id)
            print(f"تمت متابعة: {u_info.username} (بعد انتظار {sleep_time} ثانية)")
            
    except Exception as e:
        print(f"حدث خطأ أثناء فحص {target}: {e}")
