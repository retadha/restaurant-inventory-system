from employee.models import Employee

def get_role(request):
    user = request.user
    if user.is_authenticated:
        employee = Employee.objects.get(user=user)
        return employee.role
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