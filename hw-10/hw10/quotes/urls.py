from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.get_quotes, name="main"),
    path("<int:page>", views.get_quotes, name="quotes_pagination"),
    path("author/<str:fullname>", views.get_author, name="author"),
    path("create-author", views.create_author, name="create_author"),
    path("create-quote", views.create_quote, name="create_quote"),
]
