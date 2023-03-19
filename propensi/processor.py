from propensi.utils import get_role
from employee.models import Employee

def role_processor(request):
    if (request.user.is_authenticated):
        employee = Employee.objects.get(user=request.user)
        role = get_role(request)
        context = {
            'username':employee.nama,
            'role': role,
        }
        return context
    return {}