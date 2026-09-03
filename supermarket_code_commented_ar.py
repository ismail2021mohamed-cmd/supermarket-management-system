# ============================================================
# نسخة مشروحة من كود Supermarket Management System
# التعليقات العربية مضافة للتوضيح والمذاكرة.
# ملاحظة: لم يتم وضع تعليقات داخل نصوص SQL متعددة الأسطر حتى لا يتغير الاستعلام.
# ============================================================

import tkinter as tk  # استيراد مكتبة Tkinter للواجهة الرسومية باسم مختصر tk
from tkinter import ttk, messagebox, filedialog  # استيراد عناصر جاهزة للواجهة مثل الجداول والرسائل واختيار الملفات
import sqlite3  # استيراد SQLite للتعامل مع قاعدة البيانات المحلية
from datetime import datetime, timedelta  # استيراد أدوات التاريخ والوقت وحساب الفترات
from reportlab.pdfgen import canvas  # استيراد أداة إنشاء ملفات PDF للفواتير
import matplotlib.pyplot as plt  # استيراد مكتبة الرسومات البيانية للتقارير
import os  # استيراد أدوات التعامل مع نظام الملفات
import platform  # معرفة نوع نظام التشغيل عند الطباعة
import subprocess  # تشغيل أوامر خارجية مثل أمر الطباعة في لينكس
import shutil  # نسخ الملفات لعمل Backup
import csv  # تصدير البيانات بصيغة CSV
import heapq  # استيراد Heap لاستخدام Min Heap و Max Heap
from collections import deque  # استيراد deque لاستخدامها كـ Queue سريع

# ================= DATA STRUCTURES REQUIRED BY PROJECT =================
class CartNode:  # تعريف Node تمثل عنصر واحد داخل Linked List للسلة
    def __init__(self, barcode, item):  # دالة البناء التي تجهز بيانات الكائن عند إنشائه
        self.barcode = barcode  # تخزين أو تحديث قيمة في المتغير self.barcode
        self.item = item  # تخزين أو تحديث قيمة في المتغير self.item
        self.next = None  # تخزين أو تحديث قيمة في المتغير self.next

class LinkedListCart:  # تعريف سلة المشتريات باستخدام Linked List مع Dictionary index
    # الشرح: سطر تنفيذي ضمن منطق البرنامج
    """Customer shopping cart implemented as a Linked List with an index for fast GUI access."""
    def __init__(self):  # دالة البناء التي تجهز بيانات الكائن عند إنشائه
        self.head = None  # تخزين أو تحديث قيمة في المتغير self.head
        self.index = {}  # تخزين أو تحديث قيمة في المتغير self.index

    def __contains__(self, barcode):  # تحدد هل الباركود موجود داخل السلة أم لا
        return barcode in self.index  # إرجاع النتيجة من الدالة

    def __getitem__(self, barcode):  # ترجع بيانات منتج من السلة باستخدام الباركود
        return self.index[barcode].item  # إرجاع النتيجة من الدالة

    def __setitem__(self, barcode, item):  # تضيف أو تعدل منتج داخل Linked List Cart
        if barcode in self.index:  # شرط للتحقق قبل تنفيذ الجزء التالي
            self.index[barcode].item = item  # تخزين أو تحديث قيمة في المتغير self.index[barcode].item
            return  # سطر تنفيذي ضمن منطق البرنامج
        node = CartNode(barcode, item)  # تخزين أو تحديث قيمة في المتغير node
        if self.head is None:  # شرط للتحقق قبل تنفيذ الجزء التالي
            self.head = node  # تخزين أو تحديث قيمة في المتغير self.head
        else:  # تنفيذ هذا الجزء لو الشروط السابقة لم تتحقق
            current = self.head  # تخزين أو تحديث قيمة في المتغير current
            while current.next:  # حلقة تستمر طالما الشرط صحيح
                current = current.next  # تخزين أو تحديث قيمة في المتغير current
            current.next = node  # تخزين أو تحديث قيمة في المتغير current.next
        self.index[barcode] = node  # تخزين أو تحديث قيمة في المتغير self.index[barcode]

    def __delitem__(self, barcode):  # تحذف منتج من Linked List Cart
        prev = None  # تخزين أو تحديث قيمة في المتغير prev
        current = self.head  # تخزين أو تحديث قيمة في المتغير current
        while current:  # حلقة تستمر طالما الشرط صحيح
            if current.barcode == barcode:  # شرط للتحقق قبل تنفيذ الجزء التالي
                if prev:  # شرط للتحقق قبل تنفيذ الجزء التالي
                    prev.next = current.next  # تخزين أو تحديث قيمة في المتغير prev.next
                else:  # تنفيذ هذا الجزء لو الشروط السابقة لم تتحقق
                    self.head = current.next  # تخزين أو تحديث قيمة في المتغير self.head
                self.index.pop(barcode, None)  # سطر تنفيذي ضمن منطق البرنامج
                return  # سطر تنفيذي ضمن منطق البرنامج
            prev = current  # تخزين أو تحديث قيمة في المتغير prev
            current = current.next  # تخزين أو تحديث قيمة في المتغير current

    def items(self):  # تمر على عناصر السلة واحدًا واحدًا
        current = self.head  # تخزين أو تحديث قيمة في المتغير current
        while current:  # حلقة تستمر طالما الشرط صحيح
            yield current.barcode, current.item  # سطر تنفيذي ضمن منطق البرنامج
            current = current.next  # تخزين أو تحديث قيمة في المتغير current

    def clear(self):  # تمسح محتويات الهيكل الحالي
        self.head = None  # تخزين أو تحديث قيمة في المتغير self.head
        self.index.clear()  # سطر تنفيذي ضمن منطق البرنامج

    def __bool__(self):  # تحدد هل السلة فيها عناصر أم فاضية
        return self.head is not None  # إرجاع النتيجة من الدالة

class Stack:  # تعريف Stack لتخزين عمليات Undo بطريقة LIFO
    """Stack used for undoing cart/billing mistakes."""  # سطر تنفيذي ضمن منطق البرنامج
    def __init__(self):  # دالة البناء التي تجهز بيانات الكائن عند إنشائه
        self.data = []  # تخزين أو تحديث قيمة في المتغير self.data

    def push(self, value):  # تضيف عنصر أعلى الـ Stack
        self.data.append(value)  # إضافة عملية جديدة أعلى الـ Stack

    def pop(self):  # تسحب آخر عنصر دخل الـ Stack
        return self.data.pop() if self.data else None  # إرجاع آخر عملية من الـ Stack

    def clear(self):  # تمسح محتويات الهيكل الحالي
        self.data.clear()  # سطر تنفيذي ضمن منطق البرنامج

class CashierQueue:  # تعريف Queue لطوابير الكاشير بطريقة FIFO
    """Queue for customers waiting at each cashier."""  # سطر تنفيذي ضمن منطق البرنامج
    def __init__(self, name):  # دالة البناء التي تجهز بيانات الكائن عند إنشائه
        self.name = name  # تخزين أو تحديث قيمة في المتغير self.name
        self.q = deque()  # إنشاء Queue فارغ باستخدام deque

    def enqueue(self, customer):  # تضيف عميل في آخر الطابور Queue
        self.q.append(customer)  # إدخال العميل في آخر الـ Queue

    def dequeue(self):  # تخرج أول عميل من الطابور Queue
        return self.q.popleft() if self.q else None  # إخراج أول عميل من الـ Queue

    def __len__(self):  # ترجع طول الطابور الحالي
        return len(self.q)  # إرجاع النتيجة من الدالة

def binary_search_products(products, keyword):  # دالة Binary Search للبحث السريع عن منتج
    """Binary search by exact barcode or exact product name."""  # سطر تنفيذي ضمن منطق البرنامج
    keyword = keyword.lower().strip()  # تخزين أو تحديث قيمة في المتغير keyword
    # الشرح: تخزين أو تحديث قيمة في المتغير sorted_products
    sorted_products = sorted(products, key=lambda r: (str(r[1]).lower(), str(r[0]).lower()))
    low, high = 0, len(sorted_products) - 1  # تخزين أو تحديث قيمة في المتغير low, high
    while low <= high:  # حلقة تستمر طالما الشرط صحيح
        mid = (low + high) // 2  # حساب منتصف المجال في Binary Search
        row = sorted_products[mid]  # تخزين أو تحديث قيمة في المتغير row
        key = str(row[1]).lower()  # تخزين أو تحديث قيمة في المتغير key
        if key == keyword or str(row[0]).lower() == keyword:  # شرط للتحقق قبل تنفيذ الجزء التالي
            return [row]  # إرجاع النتيجة من الدالة
        if key < keyword:  # شرط للتحقق قبل تنفيذ الجزء التالي
            low = mid + 1  # البحث في النصف اليمين
        else:  # تنفيذ هذا الجزء لو الشروط السابقة لم تتحقق
            high = mid - 1  # البحث في النصف الشمال
    return []  # إرجاع النتيجة من الدالة

def merge_sort_by_expiry(products):  # دالة Merge Sort لترتيب المنتجات حسب الصلاحية
    """Sort products by expiry date using Merge Sort."""  # سطر تنفيذي ضمن منطق البرنامج
    if len(products) <= 1:  # شرط للتحقق قبل تنفيذ الجزء التالي
        return products  # إرجاع النتيجة من الدالة
    mid = len(products) // 2  # تخزين أو تحديث قيمة في المتغير mid
    left = merge_sort_by_expiry(products[:mid])  # تقسيم الجزء الشمال في Merge Sort
    right = merge_sort_by_expiry(products[mid:])  # تقسيم الجزء اليمين في Merge Sort
    merged = []  # تخزين أو تحديث قيمة في المتغير merged
    i = j = 0  # تخزين أو تحديث قيمة في المتغير i
    def expiry_key(row):  # تعريف دالة expiry_key
        return row[6] if row[6] else "9999-12-31"  # إرجاع النتيجة من الدالة
    while i < len(left) and j < len(right):  # حلقة تستمر طالما الشرط صحيح
        if expiry_key(left[i]) <= expiry_key(right[j]):  # شرط للتحقق قبل تنفيذ الجزء التالي
            merged.append(left[i]); i += 1  # إضافة العنصر الأصغر للنتيجة أثناء الدمج
        else:  # تنفيذ هذا الجزء لو الشروط السابقة لم تتحقق
            merged.append(right[j]); j += 1  # إضافة العنصر الأصغر للنتيجة أثناء الدمج
    merged.extend(left[i:]); merged.extend(right[j:])  # سطر تنفيذي ضمن منطق البرنامج
    return merged  # إرجاع النتيجة من الدالة

def assign_to_shortest_cashier_queue(invoice_no):  # تستخدم Min Heap لاختيار أقصر طابور كاشير
    """Min Heap chooses the cashier queue with the smallest length."""  # سطر تنفيذي ضمن منطق البرنامج
    heap = [(len(q), name) for name, q in cashier_queues.items()]  # تخزين أو تحديث قيمة في المتغير heap
    heapq.heapify(heap)  # تحويل القائمة إلى Min Heap
    _, cashier_name = heapq.heappop(heap)  # إخراج أعلى عنصر أولوية من الـ Heap
    cashier_queues[cashier_name].enqueue(invoice_no)  # سطر تنفيذي ضمن منطق البرنامج
    return cashier_name  # إرجاع النتيجة من الدالة

def queue_status_text():  # ترجع نص يوضح حالة كل طابور كاشير
    return " | ".join(f"{name}: {len(q)}" for name, q in cashier_queues.items())  # إرجاع النتيجة من الدالة

# ================= DATABASE =================
DB_NAME = "supermarket_ai.db"  # تخزين أو تحديث قيمة في المتغير DB_NAME
BACKUP_FOLDER = "auto_backups"  # تخزين أو تحديث قيمة في المتغير BACKUP_FOLDER
LOW_STOCK_LIMIT = 5  # تخزين أو تحديث قيمة في المتغير LOW_STOCK_LIMIT
EXPIRY_ALERT_DAYS = 7  # تخزين أو تحديث قيمة في المتغير EXPIRY_ALERT_DAYS
CASHIER_MAX_DISCOUNT_PERCENT = 10  # تخزين أو تحديث قيمة في المتغير CASHIER_MAX_DISCOUNT_PERCENT

conn = sqlite3.connect(DB_NAME)  # تخزين أو تحديث قيمة في المتغير conn
c = conn.cursor()  # تخزين أو تحديث قيمة في المتغير c

# ================= TABLES =================
# الشرح: تنفيذ أمر SQL على قاعدة البيانات
c.execute("""
CREATE TABLE IF NOT EXISTS products(
    name TEXT NOT NULL,
    barcode TEXT PRIMARY KEY,
    cost_price REAL DEFAULT 0,
    price REAL NOT NULL,
    stock INTEGER NOT NULL,
    supplier TEXT,
    expiry_date TEXT
)
""")

# الشرح: تنفيذ أمر SQL على قاعدة البيانات
c.execute("""
CREATE TABLE IF NOT EXISTS sales(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_no TEXT,
    product TEXT,
    barcode TEXT,
    qty INTEGER,
    price REAL,
    cost_price REAL,
    total REAL,
    profit REAL,
    date TEXT
)
""")

# الشرح: تنفيذ أمر SQL على قاعدة البيانات
c.execute("""
CREATE TABLE IF NOT EXISTS invoices(
    invoice_no TEXT PRIMARY KEY,
    subtotal REAL,
    discount REAL,
    final_total REAL,
    profit REAL,
    payment_method TEXT,
    cashier TEXT,
    customer_id INTEGER,
    paid_amount REAL,
    debt_amount REAL,
    date TEXT,
    file_path TEXT
)
""")

# الشرح: تنفيذ أمر SQL على قاعدة البيانات
c.execute("""
CREATE TABLE IF NOT EXISTS returns(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_no TEXT,
    product TEXT,
    barcode TEXT,
    qty INTEGER,
    amount REAL,
    date TEXT
)
""")

# الشرح: تنفيذ أمر SQL على قاعدة البيانات
c.execute("""
CREATE TABLE IF NOT EXISTS customers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    debt REAL DEFAULT 0
)
""")

# الشرح: تنفيذ أمر SQL على قاعدة البيانات
c.execute("""
CREATE TABLE IF NOT EXISTS suppliers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    address TEXT
)
""")

# الشرح: تنفيذ أمر SQL على قاعدة البيانات
c.execute("""
CREATE TABLE IF NOT EXISTS purchases(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_name TEXT,
    product TEXT,
    barcode TEXT,
    qty INTEGER,
    cost_price REAL,
    total REAL,
    date TEXT
)
""")

# الشرح: تنفيذ أمر SQL على قاعدة البيانات
c.execute("""
CREATE TABLE IF NOT EXISTS user_logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    role TEXT,
    action TEXT,
    details TEXT,
    date TEXT
)
""")

conn.commit()  # حفظ التغييرات في قاعدة البيانات

# ================= MIGRATION =================
def safe_add_column(table, column, column_type):  # تضيف عمود للجدول لو غير موجود بدون كسر البرنامج
    try:  # محاولة تنفيذ كود قد يسبب خطأ
        c.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}")  # تنفيذ أمر SQL على قاعدة البيانات
        conn.commit()  # حفظ التغييرات في قاعدة البيانات
    except sqlite3.OperationalError:  # التعامل مع الخطأ بدل إيقاف البرنامج
        pass  # سطر تنفيذي ضمن منطق البرنامج

safe_add_column("products", "cost_price", "REAL DEFAULT 0")  # سطر تنفيذي ضمن منطق البرنامج
safe_add_column("products", "expiry_date", "TEXT")  # سطر تنفيذي ضمن منطق البرنامج
safe_add_column("sales", "invoice_no", "TEXT")  # سطر تنفيذي ضمن منطق البرنامج
safe_add_column("sales", "price", "REAL DEFAULT 0")  # سطر تنفيذي ضمن منطق البرنامج
safe_add_column("sales", "cost_price", "REAL DEFAULT 0")  # سطر تنفيذي ضمن منطق البرنامج
safe_add_column("sales", "profit", "REAL DEFAULT 0")  # سطر تنفيذي ضمن منطق البرنامج
safe_add_column("invoices", "payment_method", "TEXT")  # سطر تنفيذي ضمن منطق البرنامج
safe_add_column("invoices", "cashier", "TEXT")  # سطر تنفيذي ضمن منطق البرنامج
safe_add_column("invoices", "customer_id", "INTEGER")  # سطر تنفيذي ضمن منطق البرنامج
safe_add_column("invoices", "paid_amount", "REAL DEFAULT 0")  # سطر تنفيذي ضمن منطق البرنامج
safe_add_column("invoices", "debt_amount", "REAL DEFAULT 0")  # سطر تنفيذي ضمن منطق البرنامج

# ================= USERS =================
users = {  # تخزين أو تحديث قيمة في المتغير users
    "ibrahim": {"password": "2612006", "role": "Admin"},  # سطر تنفيذي ضمن منطق البرنامج
    "manager": {"password": "1111", "role": "Manager"},  # سطر تنفيذي ضمن منطق البرنامج
    "cashier": {"password": "1234", "role": "Cashier"}  # سطر تنفيذي ضمن منطق البرنامج
}  # سطر تنفيذي ضمن منطق البرنامج

current_user = None  # تخزين أو تحديث قيمة في المتغير current_user
current_role = None  # تخزين أو تحديث قيمة في المتغير current_role
cart = LinkedListCart()  # تخزين أو تحديث قيمة في المتغير cart
undo_stack = Stack()  # تخزين أو تحديث قيمة في المتغير undo_stack
billing_error_stack = Stack()  # تخزين أو تحديث قيمة في المتغير billing_error_stack
cashier_queues = {  # تخزين أو تحديث قيمة في المتغير cashier_queues
    "Cashier 1": CashierQueue("Cashier 1"),  # سطر تنفيذي ضمن منطق البرنامج
    "Cashier 2": CashierQueue("Cashier 2"),  # سطر تنفيذي ضمن منطق البرنامج
    "Cashier 3": CashierQueue("Cashier 3")  # سطر تنفيذي ضمن منطق البرنامج
}  # سطر تنفيذي ضمن منطق البرنامج
last_invoice_file = None  # تخزين أو تحديث قيمة في المتغير last_invoice_file

# ================= LOGGING =================
def log_action(action, details=""):  # تسجل عملية المستخدم في جدول logs
    try:  # محاولة تنفيذ كود قد يسبب خطأ
        # الشرح: تنفيذ أمر SQL على قاعدة البيانات
        c.execute("""
            INSERT INTO user_logs(username, role, action, details, date)
            VALUES (?,?,?,?,?)
        """, (
            current_user or "system",  # سطر تنفيذي ضمن منطق البرنامج
            current_role or "system",  # سطر تنفيذي ضمن منطق البرنامج
            action,  # سطر تنفيذي ضمن منطق البرنامج
            details,  # سطر تنفيذي ضمن منطق البرنامج
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # الحصول على التاريخ والوقت الحالي
        ))  # سطر تنفيذي ضمن منطق البرنامج
        conn.commit()  # حفظ التغييرات في قاعدة البيانات
    except:  # التعامل مع الخطأ بدل إيقاف البرنامج
        pass  # سطر تنفيذي ضمن منطق البرنامج

# ================= BACKUP =================
def auto_backup_database():  # تعمل Backup تلقائي لقاعدة البيانات
    try:  # محاولة تنفيذ كود قد يسبب خطأ
        if not os.path.exists(BACKUP_FOLDER):  # شرط للتحقق قبل تنفيذ الجزء التالي
            os.makedirs(BACKUP_FOLDER)  # إنشاء مجلد جديد لو غير موجود

        backup_name = f"auto_backup_{datetime.now().strftime('%Y%m%d')}.db"  # الحصول على التاريخ والوقت الحالي
        backup_path = os.path.join(BACKUP_FOLDER, backup_name)  # تخزين أو تحديث قيمة في المتغير backup_path

        if not os.path.exists(backup_path):  # شرط للتحقق قبل تنفيذ الجزء التالي
            shutil.copy(DB_NAME, backup_path)  # نسخ ملف لاستخدامه كنسخة احتياطية
    except:  # التعامل مع الخطأ بدل إيقاف البرنامج
        pass  # سطر تنفيذي ضمن منطق البرنامج

auto_backup_database()  # سطر تنفيذي ضمن منطق البرنامج

# ================= PERMISSIONS =================
def is_admin():  # تتحقق هل المستخدم Admin
    return current_role == "Admin"  # إرجاع النتيجة من الدالة

def is_manager_or_admin():  # تتحقق هل المستخدم Manager أو Admin
    return current_role in ["Admin", "Manager"]  # إرجاع النتيجة من الدالة

def require_admin():  # تمنع العملية إلا لو المستخدم Admin
    if not is_admin():  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Permission", "Only Admin can do this")  # إظهار رسالة خطأ للمستخدم
        return False  # إرجاع النتيجة من الدالة
    return True  # إرجاع النتيجة من الدالة

def require_manager_or_admin():  # تمنع العملية إلا لو المستخدم Manager أو Admin
    if not is_manager_or_admin():  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Permission", "Only Admin or Manager can do this")  # إظهار رسالة خطأ للمستخدم
        return False  # إرجاع النتيجة من الدالة
    return True  # إرجاع النتيجة من الدالة

# ================= LOGIN =================
def login():  # تتحقق من بيانات الدخول وتفتح البرنامج الرئيسي
    global current_user, current_role  # تعريف المتغيرات كـ global لاستخدامها داخل الدالة

    username = username_entry.get().strip()  # تخزين أو تحديث قيمة في المتغير username
    password = password_entry.get().strip()  # تخزين أو تحديث قيمة في المتغير password

    if username in users and users[username]["password"] == password:  # شرط للتحقق قبل تنفيذ الجزء التالي
        current_user = username  # تخزين أو تحديث قيمة في المتغير current_user
        current_role = users[username]["role"]  # تخزين أو تحديث قيمة في المتغير current_role
        log_action("LOGIN", f"{username} logged in")  # سطر تنفيذي ضمن منطق البرنامج
        login_window.destroy()  # سطر تنفيذي ضمن منطق البرنامج
        open_main()  # سطر تنفيذي ضمن منطق البرنامج
    else:  # تنفيذ هذا الجزء لو الشروط السابقة لم تتحقق
        messagebox.showerror("Error", "Wrong username or password")  # إظهار رسالة خطأ للمستخدم

# ================= HELPERS =================
def clear_product_inputs():  # تمسح خانات إدخال بيانات المنتج
    name_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    barcode_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    cost_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    price_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    stock_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    supplier_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    expiry_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال

def validate_product_inputs():  # تراجع صحة بيانات المنتج قبل الحفظ
    name = name_entry.get().strip()  # تخزين أو تحديث قيمة في المتغير name
    barcode = barcode_entry.get().strip()  # تخزين أو تحديث قيمة في المتغير barcode
    supplier = supplier_entry.get().strip()  # تخزين أو تحديث قيمة في المتغير supplier
    expiry_date = expiry_entry.get().strip()  # تخزين أو تحديث قيمة في المتغير expiry_date

    if not name:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Product name is required")  # إظهار رسالة خطأ للمستخدم
        return None  # إرجاع النتيجة من الدالة

    if not barcode:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Barcode is required")  # إظهار رسالة خطأ للمستخدم
        return None  # إرجاع النتيجة من الدالة

    try:  # محاولة تنفيذ كود قد يسبب خطأ
        cost_price = float(cost_entry.get())  # تخزين أو تحديث قيمة في المتغير cost_price
        price = float(price_entry.get())  # تخزين أو تحديث قيمة في المتغير price
        stock = int(stock_entry.get())  # تخزين أو تحديث قيمة في المتغير stock
    except ValueError:  # التعامل مع الخطأ بدل إيقاف البرنامج
        messagebox.showerror("Error", "Cost, price and stock must be valid numbers")  # إظهار رسالة خطأ للمستخدم
        return None  # إرجاع النتيجة من الدالة

    if cost_price < 0 or price < 0 or stock < 0:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Numbers cannot be negative")  # إظهار رسالة خطأ للمستخدم
        return None  # إرجاع النتيجة من الدالة

    if expiry_date:  # شرط للتحقق قبل تنفيذ الجزء التالي
        try:  # محاولة تنفيذ كود قد يسبب خطأ
            datetime.strptime(expiry_date, "%Y-%m-%d")  # تحويل نص إلى تاريخ للتحقق منه
        except ValueError:  # التعامل مع الخطأ بدل إيقاف البرنامج
            messagebox.showerror("Error", "Expiry date must be YYYY-MM-DD")  # إظهار رسالة خطأ للمستخدم
            return None  # إرجاع النتيجة من الدالة

    return name, barcode, cost_price, price, stock, supplier, expiry_date  # إرجاع النتيجة من الدالة

def get_discount():  # تقرأ قيمة الخصم من الواجهة
    try:  # محاولة تنفيذ كود قد يسبب خطأ
        discount = float(discount_entry.get())  # تخزين أو تحديث قيمة في المتغير discount
    except:  # التعامل مع الخطأ بدل إيقاف البرنامج
        discount = 0  # تخزين أو تحديث قيمة في المتغير discount

    if discount < 0:  # شرط للتحقق قبل تنفيذ الجزء التالي
        discount = 0  # تخزين أو تحديث قيمة في المتغير discount

    return discount  # إرجاع النتيجة من الدالة

def get_selected_customer_id():  # تستخرج رقم العميل المختار من ComboBox
    value = customer_combo.get().strip()  # تخزين أو تحديث قيمة في المتغير value

    if not value or value == "No Customer":  # شرط للتحقق قبل تنفيذ الجزء التالي
        return None  # إرجاع النتيجة من الدالة

    try:  # محاولة تنفيذ كود قد يسبب خطأ
        return int(value.split(" - ")[0])  # إرجاع النتيجة من الدالة
    except:  # التعامل مع الخطأ بدل إيقاف البرنامج
        return None  # إرجاع النتيجة من الدالة

def refresh_all():  # تحدث كل الجداول والتقارير في الواجهة
    load_products()  # سطر تنفيذي ضمن منطق البرنامج
    load_low_stock()  # سطر تنفيذي ضمن منطق البرنامج
    load_expiry_alerts()  # سطر تنفيذي ضمن منطق البرنامج
    load_invoices()  # سطر تنفيذي ضمن منطق البرنامج
    load_customers()  # سطر تنفيذي ضمن منطق البرنامج
    load_suppliers()  # سطر تنفيذي ضمن منطق البرنامج
    load_logs()  # سطر تنفيذي ضمن منطق البرنامج
    dashboard()  # سطر تنفيذي ضمن منطق البرنامج
    forecast()  # سطر تنفيذي ضمن منطق البرنامج
    stock_intelligence()  # سطر تنفيذي ضمن منطق البرنامج

# ================= PRODUCTS =================
def load_products():  # تحميل المنتجات من قاعدة البيانات وعرضها في الجدول
    products_table.delete(*products_table.get_children())  # حذف بيانات من جدول أو خانة إدخال

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        SELECT name, barcode, cost_price, price, stock, supplier, expiry_date
        FROM products
        ORDER BY name
    """)
    rows = c.fetchall()  # جلب كل النتائج من قاعدة البيانات

    for row in rows:  # حلقة تكرار على مجموعة عناصر
        stock = row[4]  # تخزين أو تحديث قيمة في المتغير stock
        expiry = row[6]  # تخزين أو تحديث قيمة في المتغير expiry
        tag = "ok"  # تخزين أو تحديث قيمة في المتغير tag

        if stock <= LOW_STOCK_LIMIT:  # شرط للتحقق قبل تنفيذ الجزء التالي
            tag = "low"  # تخزين أو تحديث قيمة في المتغير tag

        if expiry:  # شرط للتحقق قبل تنفيذ الجزء التالي
            try:  # محاولة تنفيذ كود قد يسبب خطأ
                expiry_dt = datetime.strptime(expiry, "%Y-%m-%d")  # تحويل نص إلى تاريخ للتحقق منه
                # الشرح: شرط للتحقق قبل تنفيذ الجزء التالي
                if expiry_dt.date() <= datetime.now().date() + timedelta(days=EXPIRY_ALERT_DAYS):
                    tag = "expire"  # تخزين أو تحديث قيمة في المتغير tag
            except:  # التعامل مع الخطأ بدل إيقاف البرنامج
                pass  # سطر تنفيذي ضمن منطق البرنامج

        products_table.insert("", "end", values=row, tags=(tag,))  # إضافة بيانات داخل جدول أو خانة إدخال

def add_product():  # إضافة منتج جديد لقاعدة البيانات
    if not require_manager_or_admin():  # شرط للتحقق قبل تنفيذ الجزء التالي
        return  # سطر تنفيذي ضمن منطق البرنامج

    product = validate_product_inputs()  # تخزين أو تحديث قيمة في المتغير product
    if not product:  # شرط للتحقق قبل تنفيذ الجزء التالي
        return  # سطر تنفيذي ضمن منطق البرنامج

    try:  # محاولة تنفيذ كود قد يسبب خطأ
        c.execute("INSERT INTO products VALUES (?,?,?,?,?,?,?)", product)  # تنفيذ أمر SQL على قاعدة البيانات
        conn.commit()  # حفظ التغييرات في قاعدة البيانات
        log_action("ADD_PRODUCT", f"Added product {product[0]} barcode {product[1]}")  # سطر تنفيذي ضمن منطق البرنامج
        clear_product_inputs()  # سطر تنفيذي ضمن منطق البرنامج
        refresh_all()  # سطر تنفيذي ضمن منطق البرنامج
        messagebox.showinfo("Success", "Product added successfully")  # إظهار رسالة نجاح أو معلومة للمستخدم
    except sqlite3.IntegrityError:  # التعامل مع الخطأ بدل إيقاف البرنامج
        messagebox.showerror("Error", "Barcode already exists")  # إظهار رسالة خطأ للمستخدم

def update_product():  # تعديل بيانات منتج موجود
    if not require_manager_or_admin():  # شرط للتحقق قبل تنفيذ الجزء التالي
        return  # سطر تنفيذي ضمن منطق البرنامج

    product = validate_product_inputs()  # تخزين أو تحديث قيمة في المتغير product
    if not product:  # شرط للتحقق قبل تنفيذ الجزء التالي
        return  # سطر تنفيذي ضمن منطق البرنامج

    name, barcode, cost_price, price, stock, supplier, expiry_date = product  # تخزين أو تحديث قيمة في المتغير name, barcode, cost_price, price, stock, supplier, expiry_date

    c.execute("SELECT barcode FROM products WHERE barcode=?", (barcode,))  # تنفيذ أمر SQL على قاعدة البيانات
    exists = c.fetchone()  # جلب أول نتيجة من قاعدة البيانات

    if not exists:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Product not found")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        UPDATE products
        SET name=?, cost_price=?, price=?, stock=?, supplier=?, expiry_date=?
        WHERE barcode=?
    """, (name, cost_price, price, stock, supplier, expiry_date, barcode))

    conn.commit()  # حفظ التغييرات في قاعدة البيانات
    log_action("UPDATE_PRODUCT", f"Updated product {name} barcode {barcode}")  # سطر تنفيذي ضمن منطق البرنامج
    clear_product_inputs()  # سطر تنفيذي ضمن منطق البرنامج
    refresh_all()  # سطر تنفيذي ضمن منطق البرنامج
    messagebox.showinfo("Success", "Product updated successfully")  # إظهار رسالة نجاح أو معلومة للمستخدم

def delete_product():  # حذف منتج بشرط عدم وجود مبيعات عليه
    if not require_admin():  # شرط للتحقق قبل تنفيذ الجزء التالي
        return  # سطر تنفيذي ضمن منطق البرنامج

    barcode = barcode_entry.get().strip()  # تخزين أو تحديث قيمة في المتغير barcode

    if not barcode:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Enter barcode to delete product")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    c.execute("SELECT COUNT(*) FROM sales WHERE barcode=?", (barcode,))  # تنفيذ أمر SQL على قاعدة البيانات
    sold_count = c.fetchone()[0]  # جلب أول نتيجة من قاعدة البيانات

    if sold_count > 0:  # شرط للتحقق قبل تنفيذ الجزء التالي
        # الشرح: إظهار رسالة خطأ للمستخدم
        messagebox.showerror("Error", "Cannot delete product because it has sales history")
        return  # سطر تنفيذي ضمن منطق البرنامج

    # الشرح: تخزين أو تحديث قيمة في المتغير confirm
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this product?")
    if not confirm:  # شرط للتحقق قبل تنفيذ الجزء التالي
        return  # سطر تنفيذي ضمن منطق البرنامج

    c.execute("DELETE FROM products WHERE barcode=?", (barcode,))  # تنفيذ أمر SQL على قاعدة البيانات
    conn.commit()  # حفظ التغييرات في قاعدة البيانات

    if c.rowcount == 0:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Product not found")  # إظهار رسالة خطأ للمستخدم
    else:  # تنفيذ هذا الجزء لو الشروط السابقة لم تتحقق
        log_action("DELETE_PRODUCT", f"Deleted barcode {barcode}")  # سطر تنفيذي ضمن منطق البرنامج
        clear_product_inputs()  # سطر تنفيذي ضمن منطق البرنامج
        refresh_all()  # سطر تنفيذي ضمن منطق البرنامج
        messagebox.showinfo("Success", "Product deleted successfully")  # إظهار رسالة نجاح أو معلومة للمستخدم

def search_product():  # البحث عن منتج باستخدام Binary Search ثم بحث جزئي
    keyword = search_entry.get().strip()  # تخزين أو تحديث قيمة في المتغير keyword

    products_table.delete(*products_table.get_children())  # حذف بيانات من جدول أو خانة إدخال

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        SELECT name, barcode, cost_price, price, stock, supplier, expiry_date
        FROM products
    """)
    all_products = c.fetchall()  # جلب كل النتائج من قاعدة البيانات

    # First: required Binary Search for exact barcode/product name
    rows = binary_search_products(all_products, keyword)  # تخزين أو تحديث قيمة في المتغير rows

    # Second: friendly partial search if exact binary search finds nothing
    if not rows:  # شرط للتحقق قبل تنفيذ الجزء التالي
        low_keyword = keyword.lower()  # تخزين أو تحديث قيمة في المتغير low_keyword
        rows = [row for row in all_products if low_keyword in str(row[0]).lower()  # تخزين أو تحديث قيمة في المتغير rows
                or low_keyword in str(row[1]).lower()  # سطر تنفيذي ضمن منطق البرنامج
                or low_keyword in str(row[5]).lower()  # سطر تنفيذي ضمن منطق البرنامج
                or low_keyword in str(row[3]).lower()]  # سطر تنفيذي ضمن منطق البرنامج
        rows = sorted(rows, key=lambda r: r[0])  # تخزين أو تحديث قيمة في المتغير rows

    for row in rows:  # حلقة تكرار على مجموعة عناصر
        tag = "low" if row[4] <= LOW_STOCK_LIMIT else "ok"  # تخزين أو تحديث قيمة في المتغير tag
        products_table.insert("", "end", values=row, tags=(tag,))  # إضافة بيانات داخل جدول أو خانة إدخال

def sort_products_by_expiry():  # ترتيب المنتجات حسب تاريخ الصلاحية باستخدام Merge Sort
    products_table.delete(*products_table.get_children())  # حذف بيانات من جدول أو خانة إدخال
    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        SELECT name, barcode, cost_price, price, stock, supplier, expiry_date
        FROM products
    """)
    rows = merge_sort_by_expiry(c.fetchall())  # جلب كل النتائج من قاعدة البيانات
    for row in rows:  # حلقة تكرار على مجموعة عناصر
        tag = "low" if row[4] <= LOW_STOCK_LIMIT else "ok"  # تخزين أو تحديث قيمة في المتغير tag
        products_table.insert("", "end", values=row, tags=(tag,))  # إضافة بيانات داخل جدول أو خانة إدخال

def select_product(event):  # نقل بيانات المنتج المحدد إلى خانات الإدخال
    selected = products_table.focus()  # تخزين أو تحديث قيمة في المتغير selected
    if not selected:  # شرط للتحقق قبل تنفيذ الجزء التالي
        return  # سطر تنفيذي ضمن منطق البرنامج

    values = products_table.item(selected, "values")  # تخزين أو تحديث قيمة في المتغير values
    clear_product_inputs()  # سطر تنفيذي ضمن منطق البرنامج

    name_entry.insert(0, values[0])  # إضافة بيانات داخل جدول أو خانة إدخال
    barcode_entry.insert(0, values[1])  # إضافة بيانات داخل جدول أو خانة إدخال
    cost_entry.insert(0, values[2])  # إضافة بيانات داخل جدول أو خانة إدخال
    price_entry.insert(0, values[3])  # إضافة بيانات داخل جدول أو خانة إدخال
    stock_entry.insert(0, values[4])  # إضافة بيانات داخل جدول أو خانة إدخال
    supplier_entry.insert(0, values[5])  # إضافة بيانات داخل جدول أو خانة إدخال
    expiry_entry.insert(0, values[6] if values[6] else "")  # إضافة بيانات داخل جدول أو خانة إدخال

def load_low_stock():  # عرض المنتجات ذات المخزون القليل
    low_stock_table.delete(*low_stock_table.get_children())  # حذف بيانات من جدول أو خانة إدخال

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        SELECT name, barcode, stock
        FROM products
        WHERE stock <= ?
        ORDER BY stock ASC
    """, (LOW_STOCK_LIMIT,))

    for row in c.fetchall():  # حلقة تكرار على مجموعة عناصر
        low_stock_table.insert("", "end", values=row)  # إضافة بيانات داخل جدول أو خانة إدخال

def load_expiry_alerts():  # عرض تنبيهات الصلاحية باستخدام Min Heap
    expiry_table.delete(*expiry_table.get_children())  # حذف بيانات من جدول أو خانة إدخال

    # الشرح: الحصول على التاريخ والوقت الحالي
    limit_date = (datetime.now() + timedelta(days=EXPIRY_ALERT_DAYS)).strftime("%Y-%m-%d")

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        SELECT name, barcode, expiry_date
        FROM products
        WHERE expiry_date IS NOT NULL
          AND expiry_date != ''
          AND expiry_date <= ?
    """, (limit_date,))

    # Required Min Heap: nearest expiry products are displayed first
    min_heap = []  # تخزين أو تحديث قيمة في المتغير min_heap
    for row in c.fetchall():  # حلقة تكرار على مجموعة عناصر
        heapq.heappush(min_heap, (row[2], row))  # إضافة عنصر داخل Heap

    while min_heap:  # حلقة تستمر طالما الشرط صحيح
        _, row = heapq.heappop(min_heap)  # إخراج أعلى عنصر أولوية من الـ Heap
        expiry_table.insert("", "end", values=row)  # إضافة بيانات داخل جدول أو خانة إدخال

# ================= CART =================
def add_cart(event=None):  # إضافة منتج إلى السلة
    barcode = scan_entry.get().strip()  # تخزين أو تحديث قيمة في المتغير barcode

    if not barcode:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Enter barcode")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    try:  # محاولة تنفيذ كود قد يسبب خطأ
        qty = int(qty_entry.get())  # تخزين أو تحديث قيمة في المتغير qty
    except ValueError:  # التعامل مع الخطأ بدل إيقاف البرنامج
        messagebox.showerror("Error", "Quantity must be an integer")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    if qty <= 0:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Quantity must be greater than zero")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        SELECT name, barcode, cost_price, price, stock, expiry_date
        FROM products
        WHERE barcode=?
    """, (barcode,))
    row = c.fetchone()  # جلب أول نتيجة من قاعدة البيانات

    if not row:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Product not found")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    name, barcode, cost_price, price, stock, expiry_date = row  # تخزين أو تحديث قيمة في المتغير name, barcode, cost_price, price, stock, expiry_date

    if expiry_date:  # شرط للتحقق قبل تنفيذ الجزء التالي
        try:  # محاولة تنفيذ كود قد يسبب خطأ
            if datetime.strptime(expiry_date, "%Y-%m-%d").date() < datetime.now().date():  # شرط للتحقق قبل تنفيذ الجزء التالي
                messagebox.showerror("Expired", "This product is expired")  # إظهار رسالة خطأ للمستخدم
                return  # سطر تنفيذي ضمن منطق البرنامج
        except:  # التعامل مع الخطأ بدل إيقاف البرنامج
            pass  # سطر تنفيذي ضمن منطق البرنامج

    old_qty = cart[barcode]["qty"] if barcode in cart else 0  # تخزين أو تحديث قيمة في المتغير old_qty
    undo_stack.push(("ADD", barcode, old_qty))  # سطر تنفيذي ضمن منطق البرنامج
    new_qty = old_qty + qty  # تخزين أو تحديث قيمة في المتغير new_qty

    if new_qty > stock:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showwarning("Stock", "Not enough stock")  # إظهار تحذير للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    cart[barcode] = {  # تخزين أو تحديث قيمة في المتغير cart[barcode]
        "name": name,  # سطر تنفيذي ضمن منطق البرنامج
        "cost_price": cost_price,  # سطر تنفيذي ضمن منطق البرنامج
        "price": price,  # سطر تنفيذي ضمن منطق البرنامج
        "qty": new_qty  # سطر تنفيذي ضمن منطق البرنامج
    }  # سطر تنفيذي ضمن منطق البرنامج

    scan_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    qty_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    qty_entry.insert(0, "1")  # إضافة بيانات داخل جدول أو خانة إدخال
    update_cart()  # سطر تنفيذي ضمن منطق البرنامج

def update_cart(event=None):  # تحديث جدول السلة وحساب الإجمالي
    cart_table.delete(*cart_table.get_children())  # حذف بيانات من جدول أو خانة إدخال

    total = 0  # تخزين أو تحديث قيمة في المتغير total

    for barcode, item in cart.items():  # حلقة تكرار على مجموعة عناصر
        subtotal = item["price"] * item["qty"]  # تخزين أو تحديث قيمة في المتغير subtotal
        total += subtotal  # تخزين أو تحديث قيمة في المتغير total +

        cart_table.insert(  # إضافة بيانات داخل جدول أو خانة إدخال
            "",  # سطر تنفيذي ضمن منطق البرنامج
            "end",  # سطر تنفيذي ضمن منطق البرنامج
            # الشرح: تخزين أو تحديث قيمة في المتغير values
            values=(barcode, item["name"], item["qty"], f"{item['price']:.2f}", f"{subtotal:.2f}")
        )  # سطر تنفيذي ضمن منطق البرنامج

    discount = get_discount()  # تخزين أو تحديث قيمة في المتغير discount
    final_total = total - discount  # تخزين أو تحديث قيمة في المتغير final_total

    if final_total < 0:  # شرط للتحقق قبل تنفيذ الجزء التالي
        final_total = 0  # تخزين أو تحديث قيمة في المتغير final_total

    total_label.config(  # تغيير خصائص عنصر موجود في الواجهة
        text=f"TOTAL: {total:.2f} | DISCOUNT: {discount:.2f} | FINAL: {final_total:.2f}"  # تخزين أو تحديث قيمة في المتغير text
    )  # سطر تنفيذي ضمن منطق البرنامج

def remove_from_cart():  # حذف منتج محدد من السلة مع حفظه للـ Undo
    selected = cart_table.focus()  # تخزين أو تحديث قيمة في المتغير selected

    if not selected:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Select item from cart")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    values = cart_table.item(selected, "values")  # تخزين أو تحديث قيمة في المتغير values
    barcode = values[0]  # تخزين أو تحديث قيمة في المتغير barcode

    if barcode in cart:  # شرط للتحقق قبل تنفيذ الجزء التالي
        undo_stack.push(("REMOVE", barcode, cart[barcode].copy()))  # سطر تنفيذي ضمن منطق البرنامج
        del cart[barcode]  # سطر تنفيذي ضمن منطق البرنامج

    update_cart()  # سطر تنفيذي ضمن منطق البرنامج

def reset_cart():  # تفريغ السلة وإعادة القيم الافتراضية
    cart.clear()  # سطر تنفيذي ضمن منطق البرنامج
    undo_stack.clear()  # سطر تنفيذي ضمن منطق البرنامج
    discount_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    discount_entry.insert(0, "0")  # إضافة بيانات داخل جدول أو خانة إدخال
    paid_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    paid_entry.insert(0, "0")  # إضافة بيانات داخل جدول أو خانة إدخال
    update_cart()  # سطر تنفيذي ضمن منطق البرنامج

def undo_last_cart_action():  # إرجاع آخر عملية تمت على السلة باستخدام Stack
    action = undo_stack.pop()  # تخزين أو تحديث قيمة في المتغير action
    if not action:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showinfo("Undo", "No action to undo")  # إظهار رسالة نجاح أو معلومة للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    if action[0] == "ADD":  # شرط للتحقق قبل تنفيذ الجزء التالي
        _, barcode, old_qty = action  # تخزين أو تحديث قيمة في المتغير _, barcode, old_qty
        if old_qty == 0:  # شرط للتحقق قبل تنفيذ الجزء التالي
            if barcode in cart:  # شرط للتحقق قبل تنفيذ الجزء التالي
                del cart[barcode]  # سطر تنفيذي ضمن منطق البرنامج
        else:  # تنفيذ هذا الجزء لو الشروط السابقة لم تتحقق
            cart[barcode]["qty"] = old_qty  # تخزين أو تحديث قيمة في المتغير cart[barcode]["qty"]
    elif action[0] == "REMOVE":  # شرط بديل لو الشرط السابق لم يتحقق
        _, barcode, old_item = action  # تخزين أو تحديث قيمة في المتغير _, barcode, old_item
        cart[barcode] = old_item  # تخزين أو تحديث قيمة في المتغير cart[barcode]

    update_cart()  # سطر تنفيذي ضمن منطق البرنامج

# ================= CHECKOUT =================
def checkout():  # إتمام عملية البيع وتسجيل الفاتورة وتحديث المخزون
    global last_invoice_file  # تعريف المتغيرات كـ global لاستخدامها داخل الدالة

    if not cart:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Cart is empty")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    payment_method = payment_combo.get().strip()  # تخزين أو تحديث قيمة في المتغير payment_method
    customer_id = get_selected_customer_id()  # تخزين أو تحديث قيمة في المتغير customer_id

    if not payment_method:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Choose payment method")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    discount = get_discount()  # تخزين أو تحديث قيمة في المتغير discount
    invoice_items = list(cart.items())  # تخزين أو تحديث قيمة في المتغير invoice_items
    invoice_no = datetime.now().strftime("%Y%m%d%H%M%S")  # الحصول على التاريخ والوقت الحالي
    assigned_cashier_queue = assign_to_shortest_cashier_queue(invoice_no)  # تخزين أو تحديث قيمة في المتغير assigned_cashier_queue
    try:  # محاولة تنفيذ كود قد يسبب خطأ
        cashier_queue_label.config(text="Cashier Queues: " + queue_status_text())  # تغيير خصائص عنصر موجود في الواجهة
    except:  # التعامل مع الخطأ بدل إيقاف البرنامج
        pass  # سطر تنفيذي ضمن منطق البرنامج

    subtotal = 0  # تخزين أو تحديث قيمة في المتغير subtotal
    total_profit = 0  # تخزين أو تحديث قيمة في المتغير total_profit

    for barcode, item in invoice_items:  # حلقة تكرار على مجموعة عناصر
        item_total = item["price"] * item["qty"]  # تخزين أو تحديث قيمة في المتغير item_total
        item_profit = (item["price"] - item["cost_price"]) * item["qty"]  # تخزين أو تحديث قيمة في المتغير item_profit
        subtotal += item_total  # تخزين أو تحديث قيمة في المتغير subtotal +
        total_profit += item_profit  # تخزين أو تحديث قيمة في المتغير total_profit +

    if current_role == "Cashier":  # شرط للتحقق قبل تنفيذ الجزء التالي
        max_discount = subtotal * CASHIER_MAX_DISCOUNT_PERCENT / 100  # تخزين أو تحديث قيمة في المتغير max_discount
        if discount > max_discount:  # شرط للتحقق قبل تنفيذ الجزء التالي
            messagebox.showerror(  # إظهار رسالة خطأ للمستخدم
                "Discount Blocked",  # سطر تنفيذي ضمن منطق البرنامج
                # الشرح: سطر تنفيذي ضمن منطق البرنامج
                f"Cashier cannot discount more than {CASHIER_MAX_DISCOUNT_PERCENT}%.\nMax discount: {max_discount:.2f}"
            )  # سطر تنفيذي ضمن منطق البرنامج
            return  # سطر تنفيذي ضمن منطق البرنامج

    final_total = subtotal - discount  # تخزين أو تحديث قيمة في المتغير final_total
    if final_total < 0:  # شرط للتحقق قبل تنفيذ الجزء التالي
        final_total = 0  # تخزين أو تحديث قيمة في المتغير final_total

    try:  # محاولة تنفيذ كود قد يسبب خطأ
        paid_amount = float(paid_entry.get())  # تخزين أو تحديث قيمة في المتغير paid_amount
    except:  # التعامل مع الخطأ بدل إيقاف البرنامج
        paid_amount = final_total  # تخزين أو تحديث قيمة في المتغير paid_amount

    if paid_amount < 0:  # شرط للتحقق قبل تنفيذ الجزء التالي
        paid_amount = 0  # تخزين أو تحديث قيمة في المتغير paid_amount

    debt_amount = 0  # تخزين أو تحديث قيمة في المتغير debt_amount

    if payment_method == "Debt":  # شرط للتحقق قبل تنفيذ الجزء التالي
        if customer_id is None:  # شرط للتحقق قبل تنفيذ الجزء التالي
            messagebox.showerror("Error", "Debt payment requires customer")  # إظهار رسالة خطأ للمستخدم
            return  # سطر تنفيذي ضمن منطق البرنامج

        debt_amount = final_total - paid_amount  # تخزين أو تحديث قيمة في المتغير debt_amount
        if debt_amount < 0:  # شرط للتحقق قبل تنفيذ الجزء التالي
            debt_amount = 0  # تخزين أو تحديث قيمة في المتغير debt_amount

    total_profit_after_discount = total_profit - discount  # تخزين أو تحديث قيمة في المتغير total_profit_after_discount

    for barcode, item in invoice_items:  # حلقة تكرار على مجموعة عناصر
        item_total = item["price"] * item["qty"]  # تخزين أو تحديث قيمة في المتغير item_total
        item_profit = (item["price"] - item["cost_price"]) * item["qty"]  # تخزين أو تحديث قيمة في المتغير item_profit

        c.execute(  # تنفيذ أمر SQL على قاعدة البيانات
            "UPDATE products SET stock = stock - ? WHERE barcode=?",  # تخزين أو تحديث قيمة في المتغير "UPDATE products SET stock
            (item["qty"], barcode)  # سطر تنفيذي ضمن منطق البرنامج
        )  # سطر تنفيذي ضمن منطق البرنامج

        # الشرح: تنفيذ أمر SQL على قاعدة البيانات
        c.execute("""
            INSERT INTO sales(invoice_no, product, barcode, qty, price, cost_price, total, profit, date)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (
            invoice_no,  # سطر تنفيذي ضمن منطق البرنامج
            item["name"],  # سطر تنفيذي ضمن منطق البرنامج
            barcode,  # سطر تنفيذي ضمن منطق البرنامج
            item["qty"],  # سطر تنفيذي ضمن منطق البرنامج
            item["price"],  # سطر تنفيذي ضمن منطق البرنامج
            item["cost_price"],  # سطر تنفيذي ضمن منطق البرنامج
            item_total,  # سطر تنفيذي ضمن منطق البرنامج
            item_profit,  # سطر تنفيذي ضمن منطق البرنامج
            datetime.now().strftime("%Y-%m-%d")  # الحصول على التاريخ والوقت الحالي
        ))  # سطر تنفيذي ضمن منطق البرنامج

    if debt_amount > 0 and customer_id:  # شرط للتحقق قبل تنفيذ الجزء التالي
        # الشرح: تنفيذ أمر SQL على قاعدة البيانات
        c.execute("UPDATE customers SET debt = debt + ? WHERE id=?", (debt_amount, customer_id))

    invoice_file = generate_invoice(  # تخزين أو تحديث قيمة في المتغير invoice_file
        invoice_no,  # سطر تنفيذي ضمن منطق البرنامج
        invoice_items,  # سطر تنفيذي ضمن منطق البرنامج
        subtotal,  # سطر تنفيذي ضمن منطق البرنامج
        discount,  # سطر تنفيذي ضمن منطق البرنامج
        final_total,  # سطر تنفيذي ضمن منطق البرنامج
        total_profit_after_discount,  # سطر تنفيذي ضمن منطق البرنامج
        payment_method,  # سطر تنفيذي ضمن منطق البرنامج
        paid_amount,  # سطر تنفيذي ضمن منطق البرنامج
        debt_amount,  # سطر تنفيذي ضمن منطق البرنامج
        customer_id  # سطر تنفيذي ضمن منطق البرنامج
    )  # سطر تنفيذي ضمن منطق البرنامج

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        INSERT INTO invoices(
            invoice_no, subtotal, discount, final_total, profit,
            payment_method, cashier, customer_id, paid_amount, debt_amount,
            date, file_path
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        invoice_no,  # سطر تنفيذي ضمن منطق البرنامج
        subtotal,  # سطر تنفيذي ضمن منطق البرنامج
        discount,  # سطر تنفيذي ضمن منطق البرنامج
        final_total,  # سطر تنفيذي ضمن منطق البرنامج
        total_profit_after_discount,  # سطر تنفيذي ضمن منطق البرنامج
        payment_method,  # سطر تنفيذي ضمن منطق البرنامج
        current_user,  # سطر تنفيذي ضمن منطق البرنامج
        customer_id,  # سطر تنفيذي ضمن منطق البرنامج
        paid_amount,  # سطر تنفيذي ضمن منطق البرنامج
        debt_amount,  # سطر تنفيذي ضمن منطق البرنامج
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # الحصول على التاريخ والوقت الحالي
        invoice_file  # سطر تنفيذي ضمن منطق البرنامج
    ))  # سطر تنفيذي ضمن منطق البرنامج

    conn.commit()  # حفظ التغييرات في قاعدة البيانات
    # الشرح: الحصول على التاريخ والوقت الحالي
    billing_error_stack.push((invoice_no, final_total, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    # الشرح: سطر تنفيذي ضمن منطق البرنامج
    log_action("CHECKOUT", f"Invoice {invoice_no} total {final_total:.2f} payment {payment_method}; queue {assigned_cashier_queue}")
    cashier_queues[assigned_cashier_queue].dequeue()  # سطر تنفيذي ضمن منطق البرنامج

    cart.clear()  # سطر تنفيذي ضمن منطق البرنامج
    update_cart()  # سطر تنفيذي ضمن منطق البرنامج
    refresh_all()  # سطر تنفيذي ضمن منطق البرنامج

    try:  # محاولة تنفيذ كود قد يسبب خطأ
        cashier_queue_label.config(text="Cashier Queues: " + queue_status_text())  # تغيير خصائص عنصر موجود في الواجهة
    except:  # التعامل مع الخطأ بدل إيقاف البرنامج
        pass  # سطر تنفيذي ضمن منطق البرنامج
    # الشرح: إظهار رسالة نجاح أو معلومة للمستخدم
    messagebox.showinfo("Success", f"Checkout completed\nInvoice: {invoice_no}\nQueue: {assigned_cashier_queue}")

# ================= INVOICE PDF =================
# الشرح: إنشاء فاتورة PDF
def generate_invoice(invoice_no, invoice_items, subtotal, discount, final_total, profit, payment_method, paid_amount, debt_amount, customer_id):
    global last_invoice_file  # تعريف المتغيرات كـ global لاستخدامها داخل الدالة

    filename = f"invoice_{invoice_no}.pdf"  # تخزين أو تحديث قيمة في المتغير filename
    last_invoice_file = filename  # تخزين أو تحديث قيمة في المتغير last_invoice_file

    customer_name = "No Customer"  # تخزين أو تحديث قيمة في المتغير customer_name

    if customer_id:  # شرط للتحقق قبل تنفيذ الجزء التالي
        c.execute("SELECT name, phone FROM customers WHERE id=?", (customer_id,))  # تنفيذ أمر SQL على قاعدة البيانات
        customer = c.fetchone()  # جلب أول نتيجة من قاعدة البيانات
        if customer:  # شرط للتحقق قبل تنفيذ الجزء التالي
            customer_name = f"{customer[0]} - {customer[1]}"  # تخزين أو تحديث قيمة في المتغير customer_name

    pdf = canvas.Canvas(filename)  # تخزين أو تحديث قيمة في المتغير pdf
    pdf.setTitle("Supermarket Invoice")  # أمر لكتابة أو إعداد ملف PDF

    y = 780  # تخزين أو تحديث قيمة في المتغير y

    pdf.drawString(170, 820, "IBRAHIM SUPERMARKET INVOICE")  # أمر لكتابة أو إعداد ملف PDF
    pdf.drawString(50, 800, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")  # الحصول على التاريخ والوقت الحالي
    pdf.drawString(50, 785, f"Invoice No: {invoice_no}")  # أمر لكتابة أو إعداد ملف PDF
    pdf.drawString(50, 770, f"Cashier: {current_user}")  # أمر لكتابة أو إعداد ملف PDF
    pdf.drawString(250, 770, f"Payment: {payment_method}")  # أمر لكتابة أو إعداد ملف PDF
    pdf.drawString(50, 755, f"Customer: {customer_name}")  # أمر لكتابة أو إعداد ملف PDF
    pdf.drawString(420, 785, "Tax No: 000000000")  # أمر لكتابة أو إعداد ملف PDF
    pdf.drawString(420, 770, f"QR: INV-{invoice_no}")  # أمر لكتابة أو إعداد ملف PDF

    pdf.drawString(50, 725, "Product")  # أمر لكتابة أو إعداد ملف PDF
    pdf.drawString(250, 725, "Qty")  # أمر لكتابة أو إعداد ملف PDF
    pdf.drawString(320, 725, "Price")  # أمر لكتابة أو إعداد ملف PDF
    pdf.drawString(420, 725, "Subtotal")  # أمر لكتابة أو إعداد ملف PDF

    y = 705  # تخزين أو تحديث قيمة في المتغير y

    for barcode, item in invoice_items:  # حلقة تكرار على مجموعة عناصر
        item_total = item["price"] * item["qty"]  # تخزين أو تحديث قيمة في المتغير item_total

        pdf.drawString(50, y, str(item["name"])[:28])  # أمر لكتابة أو إعداد ملف PDF
        pdf.drawString(250, y, str(item["qty"]))  # أمر لكتابة أو إعداد ملف PDF
        pdf.drawString(320, y, f"{item['price']:.2f}")  # أمر لكتابة أو إعداد ملف PDF
        pdf.drawString(420, y, f"{item_total:.2f}")  # أمر لكتابة أو إعداد ملف PDF

        y -= 20  # تخزين أو تحديث قيمة في المتغير y -

        if y < 120:  # شرط للتحقق قبل تنفيذ الجزء التالي
            pdf.showPage()  # أمر لكتابة أو إعداد ملف PDF
            y = 780  # تخزين أو تحديث قيمة في المتغير y

    pdf.drawString(50, y - 20, "-" * 70)  # أمر لكتابة أو إعداد ملف PDF
    pdf.drawString(50, y - 40, f"SUBTOTAL: {subtotal:.2f}")  # أمر لكتابة أو إعداد ملف PDF
    pdf.drawString(50, y - 60, f"DISCOUNT: {discount:.2f}")  # أمر لكتابة أو إعداد ملف PDF
    pdf.drawString(50, y - 80, f"FINAL TOTAL: {final_total:.2f}")  # أمر لكتابة أو إعداد ملف PDF
    pdf.drawString(50, y - 100, f"PAID: {paid_amount:.2f}")  # أمر لكتابة أو إعداد ملف PDF
    pdf.drawString(50, y - 120, f"DEBT: {debt_amount:.2f}")  # أمر لكتابة أو إعداد ملف PDF

    if is_manager_or_admin():  # شرط للتحقق قبل تنفيذ الجزء التالي
        pdf.drawString(50, y - 140, f"PROFIT: {profit:.2f}")  # أمر لكتابة أو إعداد ملف PDF

    pdf.save()  # أمر لكتابة أو إعداد ملف PDF
    return filename  # إرجاع النتيجة من الدالة

# ================= PRINT =================
def print_invoice():  # طباعة آخر فاتورة تم إنشاؤها
    if not last_invoice_file:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "No invoice to print")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    if not os.path.exists(last_invoice_file):  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Invoice file not found")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    try:  # محاولة تنفيذ كود قد يسبب خطأ
        system = platform.system()  # تخزين أو تحديث قيمة في المتغير system

        if system == "Windows":  # شرط للتحقق قبل تنفيذ الجزء التالي
            os.startfile(last_invoice_file, "print")  # سطر تنفيذي ضمن منطق البرنامج
        else:  # تنفيذ هذا الجزء لو الشروط السابقة لم تتحقق
            subprocess.run(["lp", last_invoice_file])  # سطر تنفيذي ضمن منطق البرنامج

        log_action("PRINT_INVOICE", last_invoice_file)  # سطر تنفيذي ضمن منطق البرنامج
        messagebox.showinfo("Print", "Invoice sent to printer")  # إظهار رسالة نجاح أو معلومة للمستخدم

    except Exception as e:  # التعامل مع الخطأ بدل إيقاف البرنامج
        messagebox.showerror("Print Error", str(e))  # إظهار رسالة خطأ للمستخدم

def print_selected_invoice():  # طباعة فاتورة محددة من جدول الفواتير
    global last_invoice_file  # تعريف المتغيرات كـ global لاستخدامها داخل الدالة

    selected = invoices_table.focus()  # تخزين أو تحديث قيمة في المتغير selected
    if not selected:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Select invoice first")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    values = invoices_table.item(selected, "values")  # تخزين أو تحديث قيمة في المتغير values
    invoice_file = values[8]  # تخزين أو تحديث قيمة في المتغير invoice_file

    if not invoice_file or not os.path.exists(invoice_file):  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Invoice PDF not found")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    last_invoice_file = invoice_file  # تخزين أو تحديث قيمة في المتغير last_invoice_file
    print_invoice()  # سطر تنفيذي ضمن منطق البرنامج

# ================= INVOICES =================
def load_invoices():  # تحميل آخر الفواتير في جدول الفواتير
    invoices_table.delete(*invoices_table.get_children())  # حذف بيانات من جدول أو خانة إدخال

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        SELECT invoice_no, subtotal, discount, final_total, payment_method,
               cashier, paid_amount, debt_amount, file_path, date
        FROM invoices
        ORDER BY date DESC
        LIMIT 200
    """)

    for row in c.fetchall():  # حلقة تكرار على مجموعة عناصر
        invoices_table.insert("", "end", values=row)  # إضافة بيانات داخل جدول أو خانة إدخال

def show_invoice_details():  # عرض تفاصيل فاتورة محددة
    selected = invoices_table.focus()  # تخزين أو تحديث قيمة في المتغير selected
    if not selected:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Select invoice first")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    values = invoices_table.item(selected, "values")  # تخزين أو تحديث قيمة في المتغير values
    invoice_no = values[0]  # تخزين أو تحديث قيمة في المتغير invoice_no

    details_window = tk.Toplevel()  # إنشاء نافذة فرعية جديدة
    details_window.title(f"Invoice {invoice_no}")  # سطر تنفيذي ضمن منطق البرنامج
    details_window.geometry("800x420")  # سطر تنفيذي ضمن منطق البرنامج

    table = ttk.Treeview(  # إنشاء جدول لعرض البيانات في الواجهة
        details_window,  # سطر تنفيذي ضمن منطق البرنامج
        columns=("Product", "Barcode", "Qty", "Price", "Total", "Profit"),  # تخزين أو تحديث قيمة في المتغير columns
        show="headings"  # تخزين أو تحديث قيمة في المتغير show
    )  # سطر تنفيذي ضمن منطق البرنامج

    for col in ("Product", "Barcode", "Qty", "Price", "Total", "Profit"):  # حلقة تكرار على مجموعة عناصر
        table.heading(col, text=col)  # تخزين أو تحديث قيمة في المتغير table.heading(col, text
        table.column(col, width=120)  # تخزين أو تحديث قيمة في المتغير table.column(col, width

    table.pack(fill="both", expand=True)  # ترتيب العنصر داخل الواجهة باستخدام pack

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        SELECT product, barcode, qty, price, total, profit
        FROM sales
        WHERE invoice_no=?
    """, (invoice_no,))

    for row in c.fetchall():  # حلقة تكرار على مجموعة عناصر
        if not is_manager_or_admin():  # شرط للتحقق قبل تنفيذ الجزء التالي
            row = row[:5] + ("Hidden",)  # تخزين أو تحديث قيمة في المتغير row
        table.insert("", "end", values=row)  # إضافة بيانات داخل جدول أو خانة إدخال

# ================= RETURNS =================
def return_product():  # تنفيذ مرتجع منتج من فاتورة
    invoice_no = return_invoice_entry.get().strip()  # تخزين أو تحديث قيمة في المتغير invoice_no
    barcode = return_barcode_entry.get().strip()  # تخزين أو تحديث قيمة في المتغير barcode

    try:  # محاولة تنفيذ كود قد يسبب خطأ
        qty = int(return_qty_entry.get())  # تخزين أو تحديث قيمة في المتغير qty
    except ValueError:  # التعامل مع الخطأ بدل إيقاف البرنامج
        messagebox.showerror("Error", "Return quantity must be a number")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    if not invoice_no or not barcode or qty <= 0:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Enter valid invoice, barcode and quantity")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        SELECT product, qty, price
        FROM sales
        WHERE invoice_no=? AND barcode=?
    """, (invoice_no, barcode))

    sale = c.fetchone()  # جلب أول نتيجة من قاعدة البيانات

    if not sale:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Sale item not found")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    product, sold_qty, price = sale  # تخزين أو تحديث قيمة في المتغير product, sold_qty, price

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        SELECT SUM(qty)
        FROM returns
        WHERE invoice_no=? AND barcode=?
    """, (invoice_no, barcode))

    already_returned = c.fetchone()[0] or 0  # جلب أول نتيجة من قاعدة البيانات

    if qty + already_returned > sold_qty:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Return quantity is more than sold quantity")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    amount = qty * price  # تخزين أو تحديث قيمة في المتغير amount

    c.execute("UPDATE products SET stock = stock + ? WHERE barcode=?", (qty, barcode))  # تنفيذ أمر SQL على قاعدة البيانات

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        INSERT INTO returns(invoice_no, product, barcode, qty, amount, date)
        VALUES (?,?,?,?,?,?)
    """, (
        invoice_no,  # سطر تنفيذي ضمن منطق البرنامج
        product,  # سطر تنفيذي ضمن منطق البرنامج
        barcode,  # سطر تنفيذي ضمن منطق البرنامج
        qty,  # سطر تنفيذي ضمن منطق البرنامج
        amount,  # سطر تنفيذي ضمن منطق البرنامج
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # الحصول على التاريخ والوقت الحالي
    ))  # سطر تنفيذي ضمن منطق البرنامج

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        UPDATE invoices
        SET final_total = final_total - ?
        WHERE invoice_no=?
    """, (amount, invoice_no))

    conn.commit()  # حفظ التغييرات في قاعدة البيانات
    log_action("RETURN_PRODUCT", f"Invoice {invoice_no}, barcode {barcode}, qty {qty}")  # سطر تنفيذي ضمن منطق البرنامج

    return_invoice_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    return_barcode_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    return_qty_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال

    refresh_all()  # سطر تنفيذي ضمن منطق البرنامج
    messagebox.showinfo("Success", "Return completed")  # إظهار رسالة نجاح أو معلومة للمستخدم

# ================= CUSTOMERS =================
def load_customers():  # تحميل العملاء وعرضهم وتحديث ComboBox
    customers_table.delete(*customers_table.get_children())  # حذف بيانات من جدول أو خانة إدخال

    c.execute("SELECT id, name, phone, debt FROM customers ORDER BY name")  # تنفيذ أمر SQL على قاعدة البيانات
    rows = c.fetchall()  # جلب كل النتائج من قاعدة البيانات

    customer_values = ["No Customer"]  # تخزين أو تحديث قيمة في المتغير customer_values

    for row in rows:  # حلقة تكرار على مجموعة عناصر
        customers_table.insert("", "end", values=row)  # إضافة بيانات داخل جدول أو خانة إدخال
        customer_values.append(f"{row[0]} - {row[1]} - {row[2]}")  # سطر تنفيذي ضمن منطق البرنامج

    try:  # محاولة تنفيذ كود قد يسبب خطأ
        customer_combo["values"] = customer_values  # تخزين أو تحديث قيمة في المتغير customer_combo["values"]
        if not customer_combo.get():  # شرط للتحقق قبل تنفيذ الجزء التالي
            customer_combo.set("No Customer")  # سطر تنفيذي ضمن منطق البرنامج
    except:  # التعامل مع الخطأ بدل إيقاف البرنامج
        pass  # سطر تنفيذي ضمن منطق البرنامج

def add_customer():  # إضافة عميل جديد
    name = customer_name_entry.get().strip()  # تخزين أو تحديث قيمة في المتغير name
    phone = customer_phone_entry.get().strip()  # تخزين أو تحديث قيمة في المتغير phone

    if not name:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Customer name is required")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    c.execute("INSERT INTO customers(name, phone, debt) VALUES (?,?,0)", (name, phone))  # تنفيذ أمر SQL على قاعدة البيانات
    conn.commit()  # حفظ التغييرات في قاعدة البيانات
    log_action("ADD_CUSTOMER", name)  # سطر تنفيذي ضمن منطق البرنامج

    customer_name_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    customer_phone_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    load_customers()  # سطر تنفيذي ضمن منطق البرنامج

def pay_customer_debt():  # تسديد جزء من مديونية العميل
    selected = customers_table.focus()  # تخزين أو تحديث قيمة في المتغير selected
    if not selected:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Select customer")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    values = customers_table.item(selected, "values")  # تخزين أو تحديث قيمة في المتغير values
    customer_id = values[0]  # تخزين أو تحديث قيمة في المتغير customer_id

    try:  # محاولة تنفيذ كود قد يسبب خطأ
        amount = float(customer_pay_entry.get())  # تخزين أو تحديث قيمة في المتغير amount
    except:  # التعامل مع الخطأ بدل إيقاف البرنامج
        messagebox.showerror("Error", "Enter valid amount")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    if amount <= 0:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Amount must be positive")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    c.execute("UPDATE customers SET debt = debt - ? WHERE id=?", (amount, customer_id))  # تنفيذ أمر SQL على قاعدة البيانات
    c.execute("UPDATE customers SET debt = 0 WHERE debt < 0")  # تنفيذ أمر SQL على قاعدة البيانات
    conn.commit()  # حفظ التغييرات في قاعدة البيانات
    log_action("CUSTOMER_DEBT_PAYMENT", f"Customer {customer_id}, amount {amount}")  # سطر تنفيذي ضمن منطق البرنامج

    customer_pay_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    load_customers()  # سطر تنفيذي ضمن منطق البرنامج
    dashboard()  # سطر تنفيذي ضمن منطق البرنامج

# ================= SUPPLIERS & PURCHASES =================
def load_suppliers():  # تحميل الموردين من قاعدة البيانات
    suppliers_table.delete(*suppliers_table.get_children())  # حذف بيانات من جدول أو خانة إدخال

    c.execute("SELECT id, name, phone, address FROM suppliers ORDER BY name")  # تنفيذ أمر SQL على قاعدة البيانات
    rows = c.fetchall()  # جلب كل النتائج من قاعدة البيانات

    supplier_values = []  # تخزين أو تحديث قيمة في المتغير supplier_values

    for row in rows:  # حلقة تكرار على مجموعة عناصر
        suppliers_table.insert("", "end", values=row)  # إضافة بيانات داخل جدول أو خانة إدخال
        supplier_values.append(row[1])  # سطر تنفيذي ضمن منطق البرنامج

    try:  # محاولة تنفيذ كود قد يسبب خطأ
        purchase_supplier_combo["values"] = supplier_values  # تخزين أو تحديث قيمة في المتغير purchase_supplier_combo["values"]
    except:  # التعامل مع الخطأ بدل إيقاف البرنامج
        pass  # سطر تنفيذي ضمن منطق البرنامج

def add_supplier():  # إضافة مورد جديد
    if not require_manager_or_admin():  # شرط للتحقق قبل تنفيذ الجزء التالي
        return  # سطر تنفيذي ضمن منطق البرنامج

    name = supplier_name_entry.get().strip()  # تخزين أو تحديث قيمة في المتغير name
    phone = supplier_phone_entry.get().strip()  # تخزين أو تحديث قيمة في المتغير phone
    address = supplier_address_entry.get().strip()  # تخزين أو تحديث قيمة في المتغير address

    if not name:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Supplier name is required")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("INSERT INTO suppliers(name, phone, address) VALUES (?,?,?)", (name, phone, address))
    conn.commit()  # حفظ التغييرات في قاعدة البيانات
    log_action("ADD_SUPPLIER", name)  # سطر تنفيذي ضمن منطق البرنامج

    supplier_name_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    supplier_phone_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    supplier_address_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    load_suppliers()  # سطر تنفيذي ضمن منطق البرنامج

def add_purchase():  # تسجيل عملية شراء من مورد وتحديث المخزون
    if not require_manager_or_admin():  # شرط للتحقق قبل تنفيذ الجزء التالي
        return  # سطر تنفيذي ضمن منطق البرنامج

    supplier_name = purchase_supplier_combo.get().strip()  # تخزين أو تحديث قيمة في المتغير supplier_name
    barcode = purchase_barcode_entry.get().strip()  # تخزين أو تحديث قيمة في المتغير barcode

    try:  # محاولة تنفيذ كود قد يسبب خطأ
        qty = int(purchase_qty_entry.get())  # تخزين أو تحديث قيمة في المتغير qty
        cost_price = float(purchase_cost_entry.get())  # تخزين أو تحديث قيمة في المتغير cost_price
    except:  # التعامل مع الخطأ بدل إيقاف البرنامج
        messagebox.showerror("Error", "Qty and cost must be valid")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    if not supplier_name or not barcode or qty <= 0 or cost_price < 0:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Enter valid purchase data")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    c.execute("SELECT name FROM products WHERE barcode=?", (barcode,))  # تنفيذ أمر SQL على قاعدة البيانات
    product = c.fetchone()  # جلب أول نتيجة من قاعدة البيانات

    if not product:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showerror("Error", "Product not found")  # إظهار رسالة خطأ للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    product_name = product[0]  # تخزين أو تحديث قيمة في المتغير product_name
    total = qty * cost_price  # تخزين أو تحديث قيمة في المتغير total

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("UPDATE products SET stock = stock + ?, cost_price=? WHERE barcode=?", (qty, cost_price, barcode))

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        INSERT INTO purchases(supplier_name, product, barcode, qty, cost_price, total, date)
        VALUES (?,?,?,?,?,?,?)
    """, (
        supplier_name,  # سطر تنفيذي ضمن منطق البرنامج
        product_name,  # سطر تنفيذي ضمن منطق البرنامج
        barcode,  # سطر تنفيذي ضمن منطق البرنامج
        qty,  # سطر تنفيذي ضمن منطق البرنامج
        cost_price,  # سطر تنفيذي ضمن منطق البرنامج
        total,  # سطر تنفيذي ضمن منطق البرنامج
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # الحصول على التاريخ والوقت الحالي
    ))  # سطر تنفيذي ضمن منطق البرنامج

    conn.commit()  # حفظ التغييرات في قاعدة البيانات
    log_action("ADD_PURCHASE", f"{product_name}, qty {qty}, supplier {supplier_name}")  # سطر تنفيذي ضمن منطق البرنامج

    purchase_barcode_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    purchase_qty_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال
    purchase_cost_entry.delete(0, tk.END)  # حذف بيانات من جدول أو خانة إدخال

    refresh_all()  # سطر تنفيذي ضمن منطق البرنامج
    messagebox.showinfo("Success", "Purchase added and stock updated")  # إظهار رسالة نجاح أو معلومة للمستخدم

# ================= DASHBOARD =================
def get_date_range():  # قراءة تاريخ بداية ونهاية التقرير
    start = report_start_entry.get().strip()  # تخزين أو تحديث قيمة في المتغير start
    end = report_end_entry.get().strip()  # تخزين أو تحديث قيمة في المتغير end

    if not start:  # شرط للتحقق قبل تنفيذ الجزء التالي
        start = datetime.now().strftime("%Y-%m-%d")  # الحصول على التاريخ والوقت الحالي

    if not end:  # شرط للتحقق قبل تنفيذ الجزء التالي
        end = datetime.now().strftime("%Y-%m-%d")  # الحصول على التاريخ والوقت الحالي

    try:  # محاولة تنفيذ كود قد يسبب خطأ
        datetime.strptime(start, "%Y-%m-%d")  # تحويل نص إلى تاريخ للتحقق منه
        datetime.strptime(end, "%Y-%m-%d")  # تحويل نص إلى تاريخ للتحقق منه
    except:  # التعامل مع الخطأ بدل إيقاف البرنامج
        messagebox.showerror("Error", "Dates must be YYYY-MM-DD")  # إظهار رسالة خطأ للمستخدم
        return None, None  # إرجاع النتيجة من الدالة

    return start, end  # إرجاع النتيجة من الدالة

def dashboard():  # عرض ملخص المبيعات والأرباح والديون
    today_date = datetime.now().strftime("%Y-%m-%d")  # الحصول على التاريخ والوقت الحالي

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("SELECT SUM(final_total) FROM invoices WHERE date LIKE ?", (f"{today_date}%",))
    today_sales = c.fetchone()[0] or 0  # جلب أول نتيجة من قاعدة البيانات

    c.execute("SELECT SUM(final_total) FROM invoices")  # تنفيذ أمر SQL على قاعدة البيانات
    total_sales = c.fetchone()[0] or 0  # جلب أول نتيجة من قاعدة البيانات

    c.execute("SELECT SUM(profit) FROM invoices WHERE date LIKE ?", (f"{today_date}%",))  # تنفيذ أمر SQL على قاعدة البيانات
    today_profit = c.fetchone()[0] or 0  # جلب أول نتيجة من قاعدة البيانات

    c.execute("SELECT SUM(profit) FROM invoices")  # تنفيذ أمر SQL على قاعدة البيانات
    total_profit = c.fetchone()[0] or 0  # جلب أول نتيجة من قاعدة البيانات

    c.execute("SELECT SUM(debt) FROM customers")  # تنفيذ أمر SQL على قاعدة البيانات
    total_debts = c.fetchone()[0] or 0  # جلب أول نتيجة من قاعدة البيانات

    if is_manager_or_admin():  # شرط للتحقق قبل تنفيذ الجزء التالي
        dash_label.config(  # تغيير خصائص عنصر موجود في الواجهة
            text=f"Today Sales: {today_sales:.2f} | Total Sales: {total_sales:.2f}\n"  # تخزين أو تحديث قيمة في المتغير text
                 f"Today Profit: {today_profit:.2f} | Total Profit: {total_profit:.2f}\n"  # سطر تنفيذي ضمن منطق البرنامج
                 f"Customer Debts: {total_debts:.2f}"  # سطر تنفيذي ضمن منطق البرنامج
        )  # سطر تنفيذي ضمن منطق البرنامج
    else:  # تنفيذ هذا الجزء لو الشروط السابقة لم تتحقق
        dash_label.config(  # تغيير خصائص عنصر موجود في الواجهة
            text=f"Today Sales: {today_sales:.2f} | Total Sales: {total_sales:.2f}"  # تخزين أو تحديث قيمة في المتغير text
        )  # سطر تنفيذي ضمن منطق البرنامج

def forecast():  # توقع بسيط للمبيعات باستخدام متوسط آخر أيام
    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        SELECT substr(date, 1, 10), SUM(final_total)
        FROM invoices
        GROUP BY substr(date, 1, 10)
        ORDER BY substr(date, 1, 10)
    """)

    data = c.fetchall()  # جلب كل النتائج من قاعدة البيانات

    if len(data) < 2:  # شرط للتحقق قبل تنفيذ الجزء التالي
        forecast_label.config(text="Sales Estimate: Not enough data")  # تغيير خصائص عنصر موجود في الواجهة
        return  # سطر تنفيذي ضمن منطق البرنامج

    values = [row[1] for row in data]  # تخزين أو تحديث قيمة في المتغير values
    avg = sum(values[-3:]) / min(3, len(values))  # تخزين أو تحديث قيمة في المتغير avg

    forecast_label.config(  # تغيير خصائص عنصر موجود في الواجهة
        # الشرح: تخزين أو تحديث قيمة في المتغير text
        text=f"Sales Estimate\nTomorrow: {avg:.2f}\nWeek: {avg * 7:.2f}\nMonth: {avg * 30:.2f}"
    )  # سطر تنفيذي ضمن منطق البرنامج

def stock_intelligence():  # عرض أعلى المنتجات مبيعًا باستخدام Max Heap
    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        SELECT product, SUM(qty)
        FROM sales
        GROUP BY product
    """)

    # Required Max Heap: highest selling products appear first
    max_heap = []  # تخزين أو تحديث قيمة في المتغير max_heap
    for product, qty in c.fetchall():  # حلقة تكرار على مجموعة عناصر
        heapq.heappush(max_heap, (-qty, product))  # إضافة المنتج للـ Max Heap باستخدام الكمية بالسالب

    top = []  # تخزين أو تحديث قيمة في المتغير top
    for _ in range(min(5, len(max_heap))):  # حلقة تكرار على مجموعة عناصر
        qty_neg, product = heapq.heappop(max_heap)  # إخراج أعلى عنصر أولوية من الـ Heap
        top.append((product, -qty_neg))  # سطر تنفيذي ضمن منطق البرنامج

    if not top:  # شرط للتحقق قبل تنفيذ الجزء التالي
        intel_label.config(text="Top Selling: No sales yet")  # تغيير خصائص عنصر موجود في الواجهة
        return  # سطر تنفيذي ضمن منطق البرنامج

    # الشرح: تخزين أو تحديث قيمة في المتغير msg
    msg = "Top Selling Using Max Heap:\n" + "\n".join([f"{product} ({qty})" for product, qty in top])
    intel_label.config(text=msg)  # تغيير خصائص عنصر موجود في الواجهة

# ================= CHARTS =================
def show_sales_chart():  # رسم تقرير المبيعات
    start, end = get_date_range()  # تخزين أو تحديث قيمة في المتغير start, end
    if not start:  # شرط للتحقق قبل تنفيذ الجزء التالي
        return  # سطر تنفيذي ضمن منطق البرنامج

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        SELECT substr(date, 1, 10), SUM(final_total)
        FROM invoices
        WHERE substr(date, 1, 10) BETWEEN ? AND ?
        GROUP BY substr(date, 1, 10)
        ORDER BY substr(date, 1, 10)
    """, (start, end))

    data = c.fetchall()  # جلب كل النتائج من قاعدة البيانات

    if not data:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showinfo("Chart", "No sales data")  # إظهار رسالة نجاح أو معلومة للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    dates = [row[0] for row in data]  # تخزين أو تحديث قيمة في المتغير dates
    values = [row[1] for row in data]  # تخزين أو تحديث قيمة في المتغير values

    plt.figure(figsize=(8, 5))  # أمر خاص برسم الرسم البياني
    plt.plot(dates, values, marker="o")  # أمر خاص برسم الرسم البياني
    plt.title(f"Sales Chart from {start} to {end}")  # أمر خاص برسم الرسم البياني
    plt.xlabel("Date")  # أمر خاص برسم الرسم البياني
    plt.ylabel("Sales")  # أمر خاص برسم الرسم البياني
    plt.xticks(rotation=45)  # أمر خاص برسم الرسم البياني
    plt.tight_layout()  # أمر خاص برسم الرسم البياني
    plt.show()  # أمر خاص برسم الرسم البياني

def show_profit_chart():  # رسم تقرير الأرباح
    if not require_manager_or_admin():  # شرط للتحقق قبل تنفيذ الجزء التالي
        return  # سطر تنفيذي ضمن منطق البرنامج

    start, end = get_date_range()  # تخزين أو تحديث قيمة في المتغير start, end
    if not start:  # شرط للتحقق قبل تنفيذ الجزء التالي
        return  # سطر تنفيذي ضمن منطق البرنامج

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        SELECT substr(date, 1, 10), SUM(profit)
        FROM invoices
        WHERE substr(date, 1, 10) BETWEEN ? AND ?
        GROUP BY substr(date, 1, 10)
        ORDER BY substr(date, 1, 10)
    """, (start, end))

    data = c.fetchall()  # جلب كل النتائج من قاعدة البيانات

    if not data:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showinfo("Chart", "No profit data")  # إظهار رسالة نجاح أو معلومة للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    dates = [row[0] for row in data]  # تخزين أو تحديث قيمة في المتغير dates
    values = [row[1] for row in data]  # تخزين أو تحديث قيمة في المتغير values

    plt.figure(figsize=(8, 5))  # أمر خاص برسم الرسم البياني
    plt.plot(dates, values, marker="o")  # أمر خاص برسم الرسم البياني
    plt.title(f"Profit Chart from {start} to {end}")  # أمر خاص برسم الرسم البياني
    plt.xlabel("Date")  # أمر خاص برسم الرسم البياني
    plt.ylabel("Profit")  # أمر خاص برسم الرسم البياني
    plt.xticks(rotation=45)  # أمر خاص برسم الرسم البياني
    plt.tight_layout()  # أمر خاص برسم الرسم البياني
    plt.show()  # أمر خاص برسم الرسم البياني

def show_product_sales_report():  # رسم مبيعات المنتجات
    start, end = get_date_range()  # تخزين أو تحديث قيمة في المتغير start, end
    if not start:  # شرط للتحقق قبل تنفيذ الجزء التالي
        return  # سطر تنفيذي ضمن منطق البرنامج

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        SELECT product, SUM(total)
        FROM sales
        WHERE date BETWEEN ? AND ?
        GROUP BY product
        ORDER BY SUM(total) DESC
    """, (start, end))

    data = c.fetchall()  # جلب كل النتائج من قاعدة البيانات

    if not data:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showinfo("Chart", "No product sales data")  # إظهار رسالة نجاح أو معلومة للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    products = [row[0] for row in data]  # تخزين أو تحديث قيمة في المتغير products
    values = [row[1] for row in data]  # تخزين أو تحديث قيمة في المتغير values

    plt.figure(figsize=(10, 6))  # أمر خاص برسم الرسم البياني
    plt.bar(products, values)  # أمر خاص برسم الرسم البياني
    plt.title(f"Product Sales from {start} to {end}")  # أمر خاص برسم الرسم البياني
    plt.xlabel("Products")  # أمر خاص برسم الرسم البياني
    plt.ylabel("Sales")  # أمر خاص برسم الرسم البياني
    plt.xticks(rotation=45)  # أمر خاص برسم الرسم البياني
    plt.tight_layout()  # أمر خاص برسم الرسم البياني
    plt.show()  # أمر خاص برسم الرسم البياني

def show_monthly_yearly_report():  # رسم التقرير الشهري للمبيعات والأرباح
    if not require_manager_or_admin():  # شرط للتحقق قبل تنفيذ الجزء التالي
        return  # سطر تنفيذي ضمن منطق البرنامج

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        SELECT substr(date, 1, 7), SUM(final_total), SUM(profit)
        FROM invoices
        GROUP BY substr(date, 1, 7)
        ORDER BY substr(date, 1, 7)
    """)

    data = c.fetchall()  # جلب كل النتائج من قاعدة البيانات

    if not data:  # شرط للتحقق قبل تنفيذ الجزء التالي
        messagebox.showinfo("Report", "No data")  # إظهار رسالة نجاح أو معلومة للمستخدم
        return  # سطر تنفيذي ضمن منطق البرنامج

    months = [row[0] for row in data]  # تخزين أو تحديث قيمة في المتغير months
    sales = [row[1] for row in data]  # تخزين أو تحديث قيمة في المتغير sales
    profits = [row[2] for row in data]  # تخزين أو تحديث قيمة في المتغير profits

    plt.figure(figsize=(10, 6))  # أمر خاص برسم الرسم البياني
    plt.plot(months, sales, marker="o", label="Sales")  # أمر خاص برسم الرسم البياني
    plt.plot(months, profits, marker="o", label="Profit")  # أمر خاص برسم الرسم البياني
    plt.title("Monthly Sales and Profit")  # أمر خاص برسم الرسم البياني
    plt.xlabel("Month")  # أمر خاص برسم الرسم البياني
    plt.ylabel("Amount")  # أمر خاص برسم الرسم البياني
    plt.xticks(rotation=45)  # أمر خاص برسم الرسم البياني
    plt.legend()  # أمر خاص برسم الرسم البياني
    plt.tight_layout()  # أمر خاص برسم الرسم البياني
    plt.show()  # أمر خاص برسم الرسم البياني

# ================= EXPORT & BACKUP =================
def export_excel():  # تصدير الجداول إلى ملفات CSV
    if not require_manager_or_admin():  # شرط للتحقق قبل تنفيذ الجزء التالي
        return  # سطر تنفيذي ضمن منطق البرنامج

    folder = filedialog.askdirectory()  # تخزين أو تحديث قيمة في المتغير folder
    if not folder:  # شرط للتحقق قبل تنفيذ الجزء التالي
        return  # سطر تنفيذي ضمن منطق البرنامج

    files = {  # تخزين أو تحديث قيمة في المتغير files
        "products.csv": "SELECT * FROM products",  # سطر تنفيذي ضمن منطق البرنامج
        "sales.csv": "SELECT * FROM sales",  # سطر تنفيذي ضمن منطق البرنامج
        "invoices.csv": "SELECT * FROM invoices",  # سطر تنفيذي ضمن منطق البرنامج
        "returns.csv": "SELECT * FROM returns",  # سطر تنفيذي ضمن منطق البرنامج
        "customers.csv": "SELECT * FROM customers",  # سطر تنفيذي ضمن منطق البرنامج
        "suppliers.csv": "SELECT * FROM suppliers",  # سطر تنفيذي ضمن منطق البرنامج
        "purchases.csv": "SELECT * FROM purchases",  # سطر تنفيذي ضمن منطق البرنامج
        "user_logs.csv": "SELECT * FROM user_logs"  # سطر تنفيذي ضمن منطق البرنامج
    }  # سطر تنفيذي ضمن منطق البرنامج

    for filename, query in files.items():  # حلقة تكرار على مجموعة عناصر
        path = os.path.join(folder, filename)  # تخزين أو تحديث قيمة في المتغير path
        c.execute(query)  # تنفيذ أمر SQL على قاعدة البيانات
        rows = c.fetchall()  # جلب كل النتائج من قاعدة البيانات
        headers = [description[0] for description in c.description]  # تخزين أو تحديث قيمة في المتغير headers

        with open(path, "w", newline="", encoding="utf-8-sig") as f:  # فتح ملف للكتابة أو القراءة مع إغلاقه تلقائيًا
            writer = csv.writer(f)  # تخزين أو تحديث قيمة في المتغير writer
            writer.writerow(headers)  # سطر تنفيذي ضمن منطق البرنامج
            writer.writerows(rows)  # سطر تنفيذي ضمن منطق البرنامج

    log_action("EXPORT_CSV", folder)  # سطر تنفيذي ضمن منطق البرنامج
    messagebox.showinfo("Export", "Data exported successfully as CSV files")  # إظهار رسالة نجاح أو معلومة للمستخدم

def backup_database():  # عمل نسخة احتياطية من قاعدة البيانات
    if not require_manager_or_admin():  # شرط للتحقق قبل تنفيذ الجزء التالي
        return  # سطر تنفيذي ضمن منطق البرنامج

    folder = filedialog.askdirectory()  # تخزين أو تحديث قيمة في المتغير folder
    if not folder:  # شرط للتحقق قبل تنفيذ الجزء التالي
        return  # سطر تنفيذي ضمن منطق البرنامج

    backup_name = f"backup_supermarket_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"  # الحصول على التاريخ والوقت الحالي
    backup_path = os.path.join(folder, backup_name)  # تخزين أو تحديث قيمة في المتغير backup_path

    shutil.copy(DB_NAME, backup_path)  # نسخ ملف لاستخدامه كنسخة احتياطية
    log_action("BACKUP_DB", backup_path)  # سطر تنفيذي ضمن منطق البرنامج

    messagebox.showinfo("Backup", f"Backup created:\n{backup_path}")  # إظهار رسالة نجاح أو معلومة للمستخدم

# ================= LOGS =================
def load_logs():  # تحميل سجل العمليات للـ Admin
    try:  # محاولة تنفيذ كود قد يسبب خطأ
        logs_table.delete(*logs_table.get_children())  # حذف بيانات من جدول أو خانة إدخال
    except:  # التعامل مع الخطأ بدل إيقاف البرنامج
        return  # سطر تنفيذي ضمن منطق البرنامج

    if not is_admin():  # شرط للتحقق قبل تنفيذ الجزء التالي
        return  # سطر تنفيذي ضمن منطق البرنامج

    # الشرح: تنفيذ أمر SQL على قاعدة البيانات
    c.execute("""
        SELECT username, role, action, details, date
        FROM user_logs
        ORDER BY date DESC
        LIMIT 300
    """)

    for row in c.fetchall():  # حلقة تكرار على مجموعة عناصر
        logs_table.insert("", "end", values=row)  # إضافة بيانات داخل جدول أو خانة إدخال

# ================= UI =================
def open_main():  # بناء وفتح الواجهة الرئيسية للبرنامج
    global products_table, low_stock_table, expiry_table, invoices_table, logs_table  # تعريف المتغيرات كـ global لاستخدامها داخل الدالة
    # الشرح: تعريف المتغيرات كـ global لاستخدامها داخل الدالة
    global name_entry, barcode_entry, cost_entry, price_entry, stock_entry, supplier_entry, expiry_entry
    global search_entry, scan_entry, qty_entry, discount_entry, paid_entry  # تعريف المتغيرات كـ global لاستخدامها داخل الدالة
    # الشرح: تعريف المتغيرات كـ global لاستخدامها داخل الدالة
    global cart_table, total_label, dash_label, forecast_label, intel_label, cashier_queue_label
    global return_invoice_entry, return_barcode_entry, return_qty_entry  # تعريف المتغيرات كـ global لاستخدامها داخل الدالة
    global customer_combo, payment_combo  # تعريف المتغيرات كـ global لاستخدامها داخل الدالة
    global customers_table, customer_name_entry, customer_phone_entry, customer_pay_entry  # تعريف المتغيرات كـ global لاستخدامها داخل الدالة
    # الشرح: تعريف المتغيرات كـ global لاستخدامها داخل الدالة
    global suppliers_table, supplier_name_entry, supplier_phone_entry, supplier_address_entry
    # الشرح: تعريف المتغيرات كـ global لاستخدامها داخل الدالة
    global purchase_supplier_combo, purchase_barcode_entry, purchase_qty_entry, purchase_cost_entry
    global report_start_entry, report_end_entry  # تعريف المتغيرات كـ global لاستخدامها داخل الدالة

    root = tk.Tk()  # إنشاء نافذة رئيسية جديدة
    root.title("IBRAHIM SUPERMARKET AI")  # سطر تنفيذي ضمن منطق البرنامج
    root.geometry("1550x880")  # سطر تنفيذي ضمن منطق البرنامج
    root.configure(bg="#0f172a")  # تخزين أو تحديث قيمة في المتغير root.configure(bg

    style = ttk.Style()  # تخزين أو تحديث قيمة في المتغير style
    style.theme_use("clam")  # سطر تنفيذي ضمن منطق البرنامج

    title = tk.Label(  # إنشاء نص Label في الواجهة
        root,  # سطر تنفيذي ضمن منطق البرنامج
        text=f"IBRAHIM SUPERMARKET AI - User: {current_user} | Role: {current_role}",  # تخزين أو تحديث قيمة في المتغير text
        bg="#0f172a",  # تخزين أو تحديث قيمة في المتغير bg
        fg="white",  # تخزين أو تحديث قيمة في المتغير fg
        font=("Arial", 20, "bold")  # تخزين أو تحديث قيمة في المتغير font
    )  # سطر تنفيذي ضمن منطق البرنامج
    title.pack(pady=8)  # ترتيب العنصر داخل الواجهة باستخدام pack

    notebook = ttk.Notebook(root)  # تخزين أو تحديث قيمة في المتغير notebook
    notebook.pack(fill="both", expand=True, padx=10, pady=10)  # ترتيب العنصر داخل الواجهة باستخدام pack

    main_tab = tk.Frame(notebook, bg="#0f172a")  # تخزين أو تحديث قيمة في المتغير main_tab
    invoices_tab = tk.Frame(notebook, bg="#0f172a")  # تخزين أو تحديث قيمة في المتغير invoices_tab
    customers_tab = tk.Frame(notebook, bg="#0f172a")  # تخزين أو تحديث قيمة في المتغير customers_tab
    suppliers_tab = tk.Frame(notebook, bg="#0f172a")  # تخزين أو تحديث قيمة في المتغير suppliers_tab
    reports_tab = tk.Frame(notebook, bg="#0f172a")  # تخزين أو تحديث قيمة في المتغير reports_tab
    alerts_tab = tk.Frame(notebook, bg="#0f172a")  # تخزين أو تحديث قيمة في المتغير alerts_tab
    logs_tab = tk.Frame(notebook, bg="#0f172a")  # تخزين أو تحديث قيمة في المتغير logs_tab

    notebook.add(main_tab, text="Sales")  # تخزين أو تحديث قيمة في المتغير notebook.add(main_tab, text
    notebook.add(invoices_tab, text="Invoices / Returns")  # تخزين أو تحديث قيمة في المتغير notebook.add(invoices_tab, text
    notebook.add(customers_tab, text="Customers / Debts")  # تخزين أو تحديث قيمة في المتغير notebook.add(customers_tab, text
    notebook.add(suppliers_tab, text="Suppliers / Purchases")  # تخزين أو تحديث قيمة في المتغير notebook.add(suppliers_tab, text
    notebook.add(reports_tab, text="Reports")  # تخزين أو تحديث قيمة في المتغير notebook.add(reports_tab, text
    notebook.add(alerts_tab, text="Alerts")  # تخزين أو تحديث قيمة في المتغير notebook.add(alerts_tab, text

    if is_admin():  # شرط للتحقق قبل تنفيذ الجزء التالي
        notebook.add(logs_tab, text="User Logs")  # تخزين أو تحديث قيمة في المتغير notebook.add(logs_tab, text

    # ================= SALES TAB =================
    main_frame = tk.Frame(main_tab, bg="#0f172a")  # تخزين أو تحديث قيمة في المتغير main_frame
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)  # ترتيب العنصر داخل الواجهة باستخدام pack

    left_frame = tk.Frame(main_frame, bg="#0f172a")  # تخزين أو تحديث قيمة في المتغير left_frame
    left_frame.pack(side="left", fill="both", expand=True, padx=10)  # ترتيب العنصر داخل الواجهة باستخدام pack

    right_frame = tk.Frame(main_frame, bg="#0f172a")  # تخزين أو تحديث قيمة في المتغير right_frame
    right_frame.pack(side="right", fill="both", expand=True, padx=10)  # ترتيب العنصر داخل الواجهة باستخدام pack

    products_table = ttk.Treeview(  # إنشاء جدول لعرض البيانات في الواجهة
        left_frame,  # سطر تنفيذي ضمن منطق البرنامج
        columns=("Name", "Barcode", "Cost", "Price", "Stock", "Supplier", "Expiry"),  # تخزين أو تحديث قيمة في المتغير columns
        show="headings",  # تخزين أو تحديث قيمة في المتغير show
        height=15  # تخزين أو تحديث قيمة في المتغير height
    )  # سطر تنفيذي ضمن منطق البرنامج

    for col in ("Name", "Barcode", "Cost", "Price", "Stock", "Supplier", "Expiry"):  # حلقة تكرار على مجموعة عناصر
        products_table.heading(col, text=col)  # تخزين أو تحديث قيمة في المتغير products_table.heading(col, text
        products_table.column(col, width=100)  # تخزين أو تحديث قيمة في المتغير products_table.column(col, width

    products_table.tag_configure("low", background="#ff9999")  # تخزين أو تحديث قيمة في المتغير products_table.tag_configure("low", background
    products_table.tag_configure("expire", background="#ffd966")  # تخزين أو تحديث قيمة في المتغير products_table.tag_configure("expire", background
    products_table.tag_configure("ok", background="white")  # تخزين أو تحديث قيمة في المتغير products_table.tag_configure("ok", background
    products_table.pack(fill="both", expand=True)  # ترتيب العنصر داخل الواجهة باستخدام pack
    products_table.bind("<<TreeviewSelect>>", select_product)  # ربط حدث من المستخدم بدالة معينة

    search_frame = tk.Frame(left_frame, bg="#0f172a")  # تخزين أو تحديث قيمة في المتغير search_frame
    search_frame.pack(fill="x", pady=8)  # ترتيب العنصر داخل الواجهة باستخدام pack

    tk.Label(search_frame, text="Search", bg="#0f172a", fg="white").pack(side="left")  # إنشاء نص Label في الواجهة
    search_entry = tk.Entry(search_frame, width=30)  # إنشاء خانة إدخال في الواجهة
    search_entry.pack(side="left", padx=5)  # ترتيب العنصر داخل الواجهة باستخدام pack

    # الشرح: إنشاء زر في الواجهة
    tk.Button(search_frame, text="Search", command=search_product).pack(side="left", padx=5)
    # الشرح: إنشاء زر في الواجهة
    tk.Button(search_frame, text="Show All", command=load_products).pack(side="left", padx=5)
    # الشرح: إنشاء زر في الواجهة
    tk.Button(search_frame, text="Sort by Expiry", command=sort_products_by_expiry).pack(side="left", padx=5)

    # الشرح: إنشاء نص Label في الواجهة
    product_frame = tk.LabelFrame(left_frame, text="Product Management", bg="#0f172a", fg="white", padx=10, pady=10)
    product_frame.pack(fill="x", pady=8)  # ترتيب العنصر داخل الواجهة باستخدام pack

    # الشرح: تخزين أو تحديث قيمة في المتغير labels
    labels = ["Product Name", "Barcode", "Cost Price", "Selling Price", "Stock", "Supplier", "Expiry YYYY-MM-DD"]
    entries = []  # تخزين أو تحديث قيمة في المتغير entries

    for i, label in enumerate(labels):  # حلقة تكرار على مجموعة عناصر
        # الشرح: إنشاء نص Label في الواجهة
        tk.Label(product_frame, text=label, bg="#0f172a", fg="white").grid(row=i, column=0, sticky="w")
        ent = tk.Entry(product_frame, width=30)  # إنشاء خانة إدخال في الواجهة
        ent.grid(row=i, column=1, padx=5, pady=2)  # ترتيب العنصر داخل الواجهة باستخدام grid
        entries.append(ent)  # سطر تنفيذي ضمن منطق البرنامج

    # الشرح: تخزين أو تحديث قيمة في المتغير name_entry, barcode_entry, cost_entry, price_entry, stock_entry, supplier_entry, expiry_entry
    name_entry, barcode_entry, cost_entry, price_entry, stock_entry, supplier_entry, expiry_entry = entries

    buttons_frame = tk.Frame(product_frame, bg="#0f172a")  # تخزين أو تحديث قيمة في المتغير buttons_frame
    buttons_frame.grid(row=7, column=0, columnspan=2, pady=8)  # ترتيب العنصر داخل الواجهة باستخدام grid

    add_btn = tk.Button(buttons_frame, text="Add", width=10, command=add_product)  # إنشاء زر في الواجهة
    # الشرح: إنشاء زر في الواجهة
    update_btn = tk.Button(buttons_frame, text="Update", width=10, command=update_product)
    # الشرح: إنشاء زر في الواجهة
    delete_btn = tk.Button(buttons_frame, text="Delete", width=10, command=delete_product)

    add_btn.pack(side="left", padx=3)  # ترتيب العنصر داخل الواجهة باستخدام pack
    update_btn.pack(side="left", padx=3)  # ترتيب العنصر داخل الواجهة باستخدام pack
    delete_btn.pack(side="left", padx=3)  # ترتيب العنصر داخل الواجهة باستخدام pack
    # الشرح: إنشاء زر في الواجهة
    tk.Button(buttons_frame, text="Clear", width=10, command=clear_product_inputs).pack(side="left", padx=3)

    if current_role == "Cashier":  # شرط للتحقق قبل تنفيذ الجزء التالي
        add_btn.config(state="disabled")  # تغيير خصائص عنصر موجود في الواجهة
        update_btn.config(state="disabled")  # تغيير خصائص عنصر موجود في الواجهة
        delete_btn.config(state="disabled")  # تغيير خصائص عنصر موجود في الواجهة
    elif current_role == "Manager":  # شرط بديل لو الشرط السابق لم يتحقق
        delete_btn.config(state="disabled")  # تغيير خصائص عنصر موجود في الواجهة

    # الشرح: إنشاء نص Label في الواجهة
    cart_frame = tk.LabelFrame(right_frame, text="Cart", bg="#0f172a", fg="white", padx=10, pady=10)
    cart_frame.pack(fill="x")  # ترتيب العنصر داخل الواجهة باستخدام pack

    # الشرح: إنشاء نص Label في الواجهة
    tk.Label(cart_frame, text="Barcode", bg="#0f172a", fg="white").grid(row=0, column=0, sticky="w")
    scan_entry = tk.Entry(cart_frame, width=30)  # إنشاء خانة إدخال في الواجهة
    scan_entry.grid(row=0, column=1, padx=5, pady=3)  # ترتيب العنصر داخل الواجهة باستخدام grid
    scan_entry.bind("<Return>", add_cart)  # ربط حدث من المستخدم بدالة معينة

    # الشرح: إنشاء نص Label في الواجهة
    tk.Label(cart_frame, text="Quantity", bg="#0f172a", fg="white").grid(row=1, column=0, sticky="w")
    qty_entry = tk.Entry(cart_frame, width=30)  # إنشاء خانة إدخال في الواجهة
    qty_entry.grid(row=1, column=1, padx=5, pady=3)  # ترتيب العنصر داخل الواجهة باستخدام grid
    qty_entry.insert(0, "1")  # إضافة بيانات داخل جدول أو خانة إدخال

    # الشرح: إنشاء نص Label في الواجهة
    tk.Label(cart_frame, text="Discount", bg="#0f172a", fg="white").grid(row=2, column=0, sticky="w")
    discount_entry = tk.Entry(cart_frame, width=30)  # إنشاء خانة إدخال في الواجهة
    discount_entry.grid(row=2, column=1, padx=5, pady=3)  # ترتيب العنصر داخل الواجهة باستخدام grid
    discount_entry.insert(0, "0")  # إضافة بيانات داخل جدول أو خانة إدخال
    discount_entry.bind("<KeyRelease>", update_cart)  # ربط حدث من المستخدم بدالة معينة

    # الشرح: إنشاء نص Label في الواجهة
    tk.Label(cart_frame, text="Payment", bg="#0f172a", fg="white").grid(row=3, column=0, sticky="w")
    # الشرح: إنشاء قائمة اختيار في الواجهة
    payment_combo = ttk.Combobox(cart_frame, values=["Cash", "Visa", "Vodafone Cash", "Debt"], width=27, state="readonly")
    payment_combo.grid(row=3, column=1, padx=5, pady=3)  # ترتيب العنصر داخل الواجهة باستخدام grid
    payment_combo.set("Cash")  # سطر تنفيذي ضمن منطق البرنامج

    # الشرح: إنشاء نص Label في الواجهة
    tk.Label(cart_frame, text="Paid Amount", bg="#0f172a", fg="white").grid(row=4, column=0, sticky="w")
    paid_entry = tk.Entry(cart_frame, width=30)  # إنشاء خانة إدخال في الواجهة
    paid_entry.grid(row=4, column=1, padx=5, pady=3)  # ترتيب العنصر داخل الواجهة باستخدام grid
    paid_entry.insert(0, "0")  # إضافة بيانات داخل جدول أو خانة إدخال

    # الشرح: إنشاء نص Label في الواجهة
    tk.Label(cart_frame, text="Customer", bg="#0f172a", fg="white").grid(row=5, column=0, sticky="w")
    customer_combo = ttk.Combobox(cart_frame, width=27, state="readonly")  # إنشاء قائمة اختيار في الواجهة
    customer_combo.grid(row=5, column=1, padx=5, pady=3)  # ترتيب العنصر داخل الواجهة باستخدام grid
    customer_combo.set("No Customer")  # سطر تنفيذي ضمن منطق البرنامج

    # الشرح: إنشاء زر في الواجهة
    tk.Button(cart_frame, text="Add To Cart", command=add_cart).grid(row=6, column=0, pady=8)
    # الشرح: إنشاء زر في الواجهة
    tk.Button(cart_frame, text="Remove Item", command=remove_from_cart).grid(row=6, column=1, pady=8)
    # الشرح: إنشاء زر في الواجهة
    tk.Button(cart_frame, text="Undo Last", command=undo_last_cart_action).grid(row=7, column=0, pady=8)

    cart_table = ttk.Treeview(  # إنشاء جدول لعرض البيانات في الواجهة
        right_frame,  # سطر تنفيذي ضمن منطق البرنامج
        columns=("Barcode", "Product", "Qty", "Price", "Subtotal"),  # تخزين أو تحديث قيمة في المتغير columns
        show="headings",  # تخزين أو تحديث قيمة في المتغير show
        height=9  # تخزين أو تحديث قيمة في المتغير height
    )  # سطر تنفيذي ضمن منطق البرنامج

    for col in ("Barcode", "Product", "Qty", "Price", "Subtotal"):  # حلقة تكرار على مجموعة عناصر
        cart_table.heading(col, text=col)  # تخزين أو تحديث قيمة في المتغير cart_table.heading(col, text
        cart_table.column(col, width=100)  # تخزين أو تحديث قيمة في المتغير cart_table.column(col, width

    cart_table.pack(fill="both", expand=True, pady=8)  # ترتيب العنصر داخل الواجهة باستخدام pack

    total_label = tk.Label(  # إنشاء نص Label في الواجهة
        right_frame,  # سطر تنفيذي ضمن منطق البرنامج
        text="TOTAL: 0.00 | DISCOUNT: 0.00 | FINAL: 0.00",  # تخزين أو تحديث قيمة في المتغير text
        bg="#0f172a",  # تخزين أو تحديث قيمة في المتغير bg
        fg="white",  # تخزين أو تحديث قيمة في المتغير fg
        font=("Arial", 14, "bold")  # تخزين أو تحديث قيمة في المتغير font
    )  # سطر تنفيذي ضمن منطق البرنامج
    total_label.pack(pady=5)  # ترتيب العنصر داخل الواجهة باستخدام pack

    cashier_queue_label = tk.Label(  # إنشاء نص Label في الواجهة
        right_frame,  # سطر تنفيذي ضمن منطق البرنامج
        text="Cashier Queues: " + queue_status_text(),  # تخزين أو تحديث قيمة في المتغير text
        bg="#0f172a",  # تخزين أو تحديث قيمة في المتغير bg
        fg="orange",  # تخزين أو تحديث قيمة في المتغير fg
        font=("Arial", 11, "bold")  # تخزين أو تحديث قيمة في المتغير font
    )  # سطر تنفيذي ضمن منطق البرنامج
    cashier_queue_label.pack(pady=3)  # ترتيب العنصر داخل الواجهة باستخدام pack

    cart_buttons = tk.Frame(right_frame, bg="#0f172a")  # تخزين أو تحديث قيمة في المتغير cart_buttons
    cart_buttons.pack(pady=5)  # ترتيب العنصر داخل الواجهة باستخدام pack

    # الشرح: إنشاء زر في الواجهة
    tk.Button(cart_buttons, text="Checkout", width=15, command=checkout).pack(side="left", padx=5)
    # الشرح: إنشاء زر في الواجهة
    tk.Button(cart_buttons, text="Print Invoice", width=15, command=print_invoice).pack(side="left", padx=5)
    # الشرح: إنشاء زر في الواجهة
    tk.Button(cart_buttons, text="Reset Cart", width=15, command=reset_cart).pack(side="left", padx=5)

    # ================= INVOICES TAB =================
    invoices_table = ttk.Treeview(  # إنشاء جدول لعرض البيانات في الواجهة
        invoices_tab,  # سطر تنفيذي ضمن منطق البرنامج
        # الشرح: تخزين أو تحديث قيمة في المتغير columns
        columns=("Invoice", "Subtotal", "Discount", "Final", "Payment", "Cashier", "Paid", "Debt", "File", "Date"),
        show="headings",  # تخزين أو تحديث قيمة في المتغير show
        height=17  # تخزين أو تحديث قيمة في المتغير height
    )  # سطر تنفيذي ضمن منطق البرنامج

    # الشرح: حلقة تكرار على مجموعة عناصر
    for col in ("Invoice", "Subtotal", "Discount", "Final", "Payment", "Cashier", "Paid", "Debt", "File", "Date"):
        invoices_table.heading(col, text=col)  # تخزين أو تحديث قيمة في المتغير invoices_table.heading(col, text
        invoices_table.column(col, width=130)  # تخزين أو تحديث قيمة في المتغير invoices_table.column(col, width

    invoices_table.pack(fill="both", expand=True, padx=10, pady=10)  # ترتيب العنصر داخل الواجهة باستخدام pack

    invoice_buttons = tk.Frame(invoices_tab, bg="#0f172a")  # تخزين أو تحديث قيمة في المتغير invoice_buttons
    invoice_buttons.pack(pady=5)  # ترتيب العنصر داخل الواجهة باستخدام pack

    # الشرح: إنشاء زر في الواجهة
    tk.Button(invoice_buttons, text="Refresh", width=18, command=load_invoices).pack(side="left", padx=5)
    # الشرح: إنشاء زر في الواجهة
    tk.Button(invoice_buttons, text="Invoice Details", width=18, command=show_invoice_details).pack(side="left", padx=5)
    # الشرح: إنشاء زر في الواجهة
    tk.Button(invoice_buttons, text="Print Selected", width=18, command=print_selected_invoice).pack(side="left", padx=5)

    # الشرح: إنشاء نص Label في الواجهة
    returns_frame = tk.LabelFrame(invoices_tab, text="Return Product", bg="#0f172a", fg="white", padx=10, pady=10)
    returns_frame.pack(fill="x", padx=10, pady=10)  # ترتيب العنصر داخل الواجهة باستخدام pack

    # الشرح: إنشاء نص Label في الواجهة
    tk.Label(returns_frame, text="Invoice No", bg="#0f172a", fg="white").grid(row=0, column=0)
    return_invoice_entry = tk.Entry(returns_frame, width=25)  # إنشاء خانة إدخال في الواجهة
    return_invoice_entry.grid(row=0, column=1, padx=5)  # ترتيب العنصر داخل الواجهة باستخدام grid

    # الشرح: إنشاء نص Label في الواجهة
    tk.Label(returns_frame, text="Barcode", bg="#0f172a", fg="white").grid(row=0, column=2)
    return_barcode_entry = tk.Entry(returns_frame, width=25)  # إنشاء خانة إدخال في الواجهة
    return_barcode_entry.grid(row=0, column=3, padx=5)  # ترتيب العنصر داخل الواجهة باستخدام grid

    tk.Label(returns_frame, text="Qty", bg="#0f172a", fg="white").grid(row=0, column=4)  # إنشاء نص Label في الواجهة
    return_qty_entry = tk.Entry(returns_frame, width=10)  # إنشاء خانة إدخال في الواجهة
    return_qty_entry.grid(row=0, column=5, padx=5)  # ترتيب العنصر داخل الواجهة باستخدام grid

    # الشرح: إنشاء زر في الواجهة
    tk.Button(returns_frame, text="Return", width=15, command=return_product).grid(row=0, column=6, padx=10)

    # ================= CUSTOMERS TAB =================
    # الشرح: إنشاء جدول لعرض البيانات في الواجهة
    customers_table = ttk.Treeview(customers_tab, columns=("ID", "Name", "Phone", "Debt"), show="headings", height=16)

    for col in ("ID", "Name", "Phone", "Debt"):  # حلقة تكرار على مجموعة عناصر
        customers_table.heading(col, text=col)  # تخزين أو تحديث قيمة في المتغير customers_table.heading(col, text
        customers_table.column(col, width=160)  # تخزين أو تحديث قيمة في المتغير customers_table.column(col, width

    customers_table.pack(fill="both", expand=True, padx=10, pady=10)  # ترتيب العنصر داخل الواجهة باستخدام pack

    # الشرح: إنشاء نص Label في الواجهة
    customer_frame = tk.LabelFrame(customers_tab, text="Customer", bg="#0f172a", fg="white", padx=10, pady=10)
    customer_frame.pack(fill="x", padx=10, pady=10)  # ترتيب العنصر داخل الواجهة باستخدام pack

    tk.Label(customer_frame, text="Name", bg="#0f172a", fg="white").grid(row=0, column=0)  # إنشاء نص Label في الواجهة
    customer_name_entry = tk.Entry(customer_frame, width=25)  # إنشاء خانة إدخال في الواجهة
    customer_name_entry.grid(row=0, column=1, padx=5)  # ترتيب العنصر داخل الواجهة باستخدام grid

    # الشرح: إنشاء نص Label في الواجهة
    tk.Label(customer_frame, text="Phone", bg="#0f172a", fg="white").grid(row=0, column=2)
    customer_phone_entry = tk.Entry(customer_frame, width=25)  # إنشاء خانة إدخال في الواجهة
    customer_phone_entry.grid(row=0, column=3, padx=5)  # ترتيب العنصر داخل الواجهة باستخدام grid

    # الشرح: إنشاء زر في الواجهة
    tk.Button(customer_frame, text="Add Customer", width=15, command=add_customer).grid(row=0, column=4, padx=5)

    # الشرح: إنشاء نص Label في الواجهة
    tk.Label(customer_frame, text="Pay Debt", bg="#0f172a", fg="white").grid(row=1, column=0, pady=8)
    customer_pay_entry = tk.Entry(customer_frame, width=25)  # إنشاء خانة إدخال في الواجهة
    customer_pay_entry.grid(row=1, column=1, padx=5)  # ترتيب العنصر داخل الواجهة باستخدام grid

    # الشرح: إنشاء زر في الواجهة
    tk.Button(customer_frame, text="Pay", width=15, command=pay_customer_debt).grid(row=1, column=2, padx=5)

    # ================= SUPPLIERS TAB =================
    # الشرح: إنشاء جدول لعرض البيانات في الواجهة
    suppliers_table = ttk.Treeview(suppliers_tab, columns=("ID", "Name", "Phone", "Address"), show="headings", height=10)

    for col in ("ID", "Name", "Phone", "Address"):  # حلقة تكرار على مجموعة عناصر
        suppliers_table.heading(col, text=col)  # تخزين أو تحديث قيمة في المتغير suppliers_table.heading(col, text
        suppliers_table.column(col, width=180)  # تخزين أو تحديث قيمة في المتغير suppliers_table.column(col, width

    suppliers_table.pack(fill="both", expand=True, padx=10, pady=10)  # ترتيب العنصر داخل الواجهة باستخدام pack

    # الشرح: إنشاء نص Label في الواجهة
    supplier_frame = tk.LabelFrame(suppliers_tab, text="Supplier", bg="#0f172a", fg="white", padx=10, pady=10)
    supplier_frame.pack(fill="x", padx=10, pady=8)  # ترتيب العنصر داخل الواجهة باستخدام pack

    tk.Label(supplier_frame, text="Name", bg="#0f172a", fg="white").grid(row=0, column=0)  # إنشاء نص Label في الواجهة
    supplier_name_entry = tk.Entry(supplier_frame, width=25)  # إنشاء خانة إدخال في الواجهة
    supplier_name_entry.grid(row=0, column=1, padx=5)  # ترتيب العنصر داخل الواجهة باستخدام grid

    # الشرح: إنشاء نص Label في الواجهة
    tk.Label(supplier_frame, text="Phone", bg="#0f172a", fg="white").grid(row=0, column=2)
    supplier_phone_entry = tk.Entry(supplier_frame, width=25)  # إنشاء خانة إدخال في الواجهة
    supplier_phone_entry.grid(row=0, column=3, padx=5)  # ترتيب العنصر داخل الواجهة باستخدام grid

    # الشرح: إنشاء نص Label في الواجهة
    tk.Label(supplier_frame, text="Address", bg="#0f172a", fg="white").grid(row=0, column=4)
    supplier_address_entry = tk.Entry(supplier_frame, width=30)  # إنشاء خانة إدخال في الواجهة
    supplier_address_entry.grid(row=0, column=5, padx=5)  # ترتيب العنصر داخل الواجهة باستخدام grid

    # الشرح: إنشاء زر في الواجهة
    tk.Button(supplier_frame, text="Add Supplier", width=15, command=add_supplier).grid(row=0, column=6, padx=5)

    # الشرح: إنشاء نص Label في الواجهة
    purchase_frame = tk.LabelFrame(suppliers_tab, text="Purchase Invoice", bg="#0f172a", fg="white", padx=10, pady=10)
    purchase_frame.pack(fill="x", padx=10, pady=8)  # ترتيب العنصر داخل الواجهة باستخدام pack

    # الشرح: إنشاء نص Label في الواجهة
    tk.Label(purchase_frame, text="Supplier", bg="#0f172a", fg="white").grid(row=0, column=0)
    purchase_supplier_combo = ttk.Combobox(purchase_frame, width=25)  # إنشاء قائمة اختيار في الواجهة
    purchase_supplier_combo.grid(row=0, column=1, padx=5)  # ترتيب العنصر داخل الواجهة باستخدام grid

    # الشرح: إنشاء نص Label في الواجهة
    tk.Label(purchase_frame, text="Product Barcode", bg="#0f172a", fg="white").grid(row=0, column=2)
    purchase_barcode_entry = tk.Entry(purchase_frame, width=25)  # إنشاء خانة إدخال في الواجهة
    purchase_barcode_entry.grid(row=0, column=3, padx=5)  # ترتيب العنصر داخل الواجهة باستخدام grid

    tk.Label(purchase_frame, text="Qty", bg="#0f172a", fg="white").grid(row=0, column=4)  # إنشاء نص Label في الواجهة
    purchase_qty_entry = tk.Entry(purchase_frame, width=10)  # إنشاء خانة إدخال في الواجهة
    purchase_qty_entry.grid(row=0, column=5, padx=5)  # ترتيب العنصر داخل الواجهة باستخدام grid

    tk.Label(purchase_frame, text="Cost", bg="#0f172a", fg="white").grid(row=0, column=6)  # إنشاء نص Label في الواجهة
    purchase_cost_entry = tk.Entry(purchase_frame, width=10)  # إنشاء خانة إدخال في الواجهة
    purchase_cost_entry.grid(row=0, column=7, padx=5)  # ترتيب العنصر داخل الواجهة باستخدام grid

    # الشرح: إنشاء زر في الواجهة
    tk.Button(purchase_frame, text="Add Purchase", width=15, command=add_purchase).grid(row=0, column=8, padx=5)

    # ================= REPORTS TAB =================
    # الشرح: إنشاء نص Label في الواجهة
    dashboard_frame = tk.LabelFrame(reports_tab, text="Dashboard", bg="#0f172a", fg="white", padx=10, pady=10)
    dashboard_frame.pack(fill="x", padx=10, pady=10)  # ترتيب العنصر داخل الواجهة باستخدام pack

    # الشرح: إنشاء نص Label في الواجهة
    dash_label = tk.Label(dashboard_frame, bg="#0f172a", fg="cyan", font=("Arial", 13, "bold"))
    dash_label.pack()  # ترتيب العنصر داخل الواجهة باستخدام pack

    # الشرح: إنشاء نص Label في الواجهة
    forecast_label = tk.Label(dashboard_frame, bg="#0f172a", fg="yellow", font=("Arial", 12))
    forecast_label.pack(pady=5)  # ترتيب العنصر داخل الواجهة باستخدام pack

    # الشرح: إنشاء نص Label في الواجهة
    intel_label = tk.Label(dashboard_frame, bg="#0f172a", fg="lightgreen", font=("Arial", 12))
    intel_label.pack(pady=5)  # ترتيب العنصر داخل الواجهة باستخدام pack

    date_frame = tk.Frame(reports_tab, bg="#0f172a")  # تخزين أو تحديث قيمة في المتغير date_frame
    date_frame.pack(pady=8)  # ترتيب العنصر داخل الواجهة باستخدام pack

    # الشرح: إنشاء نص Label في الواجهة
    tk.Label(date_frame, text="From YYYY-MM-DD", bg="#0f172a", fg="white").pack(side="left")
    report_start_entry = tk.Entry(date_frame, width=15)  # إنشاء خانة إدخال في الواجهة
    report_start_entry.pack(side="left", padx=5)  # ترتيب العنصر داخل الواجهة باستخدام pack
    report_start_entry.insert(0, datetime.now().strftime("%Y-%m-01"))  # إضافة بيانات داخل جدول أو خانة إدخال

    # الشرح: إنشاء نص Label في الواجهة
    tk.Label(date_frame, text="To YYYY-MM-DD", bg="#0f172a", fg="white").pack(side="left")
    report_end_entry = tk.Entry(date_frame, width=15)  # إنشاء خانة إدخال في الواجهة
    report_end_entry.pack(side="left", padx=5)  # ترتيب العنصر داخل الواجهة باستخدام pack
    report_end_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))  # إضافة بيانات داخل جدول أو خانة إدخال

    report_buttons = tk.Frame(reports_tab, bg="#0f172a")  # تخزين أو تحديث قيمة في المتغير report_buttons
    report_buttons.pack(pady=10)  # ترتيب العنصر داخل الواجهة باستخدام pack

    # الشرح: إنشاء زر في الواجهة
    tk.Button(report_buttons, text="Sales Chart", width=18, command=show_sales_chart).pack(side="left", padx=5)
    # الشرح: إنشاء زر في الواجهة
    tk.Button(report_buttons, text="Products Report", width=18, command=show_product_sales_report).pack(side="left", padx=5)
    # الشرح: إنشاء زر في الواجهة
    tk.Button(report_buttons, text="Profit Chart", width=18, command=show_profit_chart).pack(side="left", padx=5)
    # الشرح: إنشاء زر في الواجهة
    tk.Button(report_buttons, text="Monthly Report", width=18, command=show_monthly_yearly_report).pack(side="left", padx=5)
    # الشرح: إنشاء زر في الواجهة
    tk.Button(report_buttons, text="Export CSV", width=18, command=export_excel).pack(side="left", padx=5)
    # الشرح: إنشاء زر في الواجهة
    tk.Button(report_buttons, text="Backup DB", width=18, command=backup_database).pack(side="left", padx=5)

    # ================= ALERTS TAB =================
    # الشرح: إنشاء نص Label في الواجهة
    low_stock_frame = tk.LabelFrame(alerts_tab, text="Low Stock", bg="#0f172a", fg="white", padx=10, pady=10)
    low_stock_frame.pack(fill="both", expand=True, padx=10, pady=10)  # ترتيب العنصر داخل الواجهة باستخدام pack

    # الشرح: إنشاء جدول لعرض البيانات في الواجهة
    low_stock_table = ttk.Treeview(low_stock_frame, columns=("Name", "Barcode", "Stock"), show="headings", height=8)
    for col in ("Name", "Barcode", "Stock"):  # حلقة تكرار على مجموعة عناصر
        low_stock_table.heading(col, text=col)  # تخزين أو تحديث قيمة في المتغير low_stock_table.heading(col, text
        low_stock_table.column(col, width=180)  # تخزين أو تحديث قيمة في المتغير low_stock_table.column(col, width
    low_stock_table.pack(fill="both", expand=True)  # ترتيب العنصر داخل الواجهة باستخدام pack

    # الشرح: إنشاء نص Label في الواجهة
    expiry_frame = tk.LabelFrame(alerts_tab, text="Expiry Alerts", bg="#0f172a", fg="white", padx=10, pady=10)
    expiry_frame.pack(fill="both", expand=True, padx=10, pady=10)  # ترتيب العنصر داخل الواجهة باستخدام pack

    # الشرح: إنشاء جدول لعرض البيانات في الواجهة
    expiry_table = ttk.Treeview(expiry_frame, columns=("Name", "Barcode", "Expiry"), show="headings", height=8)
    for col in ("Name", "Barcode", "Expiry"):  # حلقة تكرار على مجموعة عناصر
        expiry_table.heading(col, text=col)  # تخزين أو تحديث قيمة في المتغير expiry_table.heading(col, text
        expiry_table.column(col, width=180)  # تخزين أو تحديث قيمة في المتغير expiry_table.column(col, width
    expiry_table.pack(fill="both", expand=True)  # ترتيب العنصر داخل الواجهة باستخدام pack

    # ================= LOGS TAB =================
    if is_admin():  # شرط للتحقق قبل تنفيذ الجزء التالي
        logs_table = ttk.Treeview(  # إنشاء جدول لعرض البيانات في الواجهة
            logs_tab,  # سطر تنفيذي ضمن منطق البرنامج
            columns=("Username", "Role", "Action", "Details", "Date"),  # تخزين أو تحديث قيمة في المتغير columns
            show="headings",  # تخزين أو تحديث قيمة في المتغير show
            height=20  # تخزين أو تحديث قيمة في المتغير height
        )  # سطر تنفيذي ضمن منطق البرنامج

        for col in ("Username", "Role", "Action", "Details", "Date"):  # حلقة تكرار على مجموعة عناصر
            logs_table.heading(col, text=col)  # تخزين أو تحديث قيمة في المتغير logs_table.heading(col, text
            logs_table.column(col, width=180)  # تخزين أو تحديث قيمة في المتغير logs_table.column(col, width

        logs_table.pack(fill="both", expand=True, padx=10, pady=10)  # ترتيب العنصر داخل الواجهة باستخدام pack

    refresh_all()  # سطر تنفيذي ضمن منطق البرنامج
    root.mainloop()  # سطر تنفيذي ضمن منطق البرنامج

# ================= LOGIN UI =================
login_window = tk.Tk()  # إنشاء نافذة رئيسية جديدة
login_window.title("LOGIN")  # سطر تنفيذي ضمن منطق البرنامج
login_window.geometry("360x260")  # سطر تنفيذي ضمن منطق البرنامج
login_window.configure(bg="#0f172a")  # تخزين أو تحديث قيمة في المتغير login_window.configure(bg

tk.Label(  # إنشاء نص Label في الواجهة
    login_window,  # سطر تنفيذي ضمن منطق البرنامج
    text="Login",  # تخزين أو تحديث قيمة في المتغير text
    bg="#0f172a",  # تخزين أو تحديث قيمة في المتغير bg
    fg="white",  # تخزين أو تحديث قيمة في المتغير fg
    font=("Arial", 18, "bold")  # تخزين أو تحديث قيمة في المتغير font
).pack(pady=10)  # ترتيب العنصر داخل الواجهة باستخدام pack

tk.Label(login_window, text="Username", bg="#0f172a", fg="white").pack()  # إنشاء نص Label في الواجهة
username_entry = tk.Entry(login_window, width=30)  # إنشاء خانة إدخال في الواجهة
username_entry.pack(pady=5)  # ترتيب العنصر داخل الواجهة باستخدام pack

tk.Label(login_window, text="Password", bg="#0f172a", fg="white").pack()  # إنشاء نص Label في الواجهة
password_entry = tk.Entry(login_window, show="*", width=30)  # إنشاء خانة إدخال في الواجهة
password_entry.pack(pady=5)  # ترتيب العنصر داخل الواجهة باستخدام pack

tk.Button(login_window, text="Login", width=15, command=login).pack(pady=15)  # إنشاء زر في الواجهة

tk.Label(  # إنشاء نص Label في الواجهة
    login_window,  # سطر تنفيذي ضمن منطق البرنامج
    text="Admin: ibrahim / 2612006\nManager: manager / 1111\nCashier: cashier / 1234",  # تخزين أو تحديث قيمة في المتغير text
    bg="#0f172a",  # تخزين أو تحديث قيمة في المتغير bg
    fg="gray"  # تخزين أو تحديث قيمة في المتغير fg
).pack()  # ترتيب العنصر داخل الواجهة باستخدام pack

login_window.mainloop()  # سطر تنفيذي ضمن منطق البرنامج




