from propensi.utils import get_role
from employee.models import Employee

def role_processor(request):
    if (request.user.is_authenticated):
        try:
            employee = Employee.objects.get(user=request.user)
        except:
            employee = None
            return {}
        role = get_role(request)
        context = {
            'username':employee.nama,
            'role': role,
            'gedung':employee.id_gedung.status,
        }
        return context
    return {}