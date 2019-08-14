from django.contrib.auth.models import User

############# login Form ############
class loginform():
    class Meta:
        model = User
        fields =  ("username","password")