from shop import models
from django.contrib.auth.models import User

def create_user(request):
    user = User.objects.create_user(
        username=request.POST["username"],
        password=request.POST["password1"],
        email=request.POST["email"],
        # first_name=request.POST["firstName"],
        # last_name=request.POST["lastName"],
    )
    return user