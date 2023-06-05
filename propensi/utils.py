from employee.models import Employee

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
