from employee.models import Employee
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from urllib.parse import quote

def get_role(request):
    user = request.user
    if user.is_authenticated:
        try:
            employee = Employee.objects.get(user=user)
            return employee.role
        except:
            return "2"  # role admin
    return ""


def is_manager(request):
    if (get_role(request) == '0'):
        return True
    return False

def is_staff(request):
    if (get_role(request) == '1'):
        return True
    return False

def is_admin(request):
    if (get_role(request) == '2'):
        return True
    return False

def get_gedung(request):
    user = request.user
    if user.is_authenticated:
        try:
            employee = Employee.objects.get(user=user)
            return employee.id_gedung.status
        except:
            return ""
    return ""


def is_gudang_pusat(request):
    if (get_gedung(request) == '0'):
        return True
    return False


def is_restoran(request):
    if (get_gedung(request) == '1'):
        return True
    return False


def send_to_whatsapp(phone, msg):
    ccphone = "+62" + phone[1:]
    try:
        url = f"https://wa.me/{ccphone}?text={quote(msg)}&type=phone_number&app_absent=0"
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()))
        driver.get(url)
        time.sleep(10)
    except:
        print("error")
    finally:
        driver.close()
        driver.quit()
