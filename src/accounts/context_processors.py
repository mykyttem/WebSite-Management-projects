from .models import Accounts

"""
Added global variable in context
In order to don't write always in context functions
"""

def global_variables(request):
    idUser_session = request.session.get('user-id')
    user_account = Accounts.objects.filter(id=idUser_session).values()

    return {
        'user_account': user_account,
    }