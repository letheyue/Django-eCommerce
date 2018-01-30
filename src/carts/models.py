from django.db import models

# Create your models here.
def cart_home(request):
	return render(request, "carts/home.html", {})