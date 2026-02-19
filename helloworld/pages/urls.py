from django.urls import path
from django.views.generic import TemplateView

from .views import (
    AboutPageView,
    ContactPageView,
    HomePageView,
    ProductCreateView,
    ProductIndexView,
    ProductShowView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contact/", ContactPageView.as_view(), name="contact"),
    path("products/", ProductIndexView.as_view(), name="index"),
    path("products/create", ProductCreateView.as_view(), name="form"),
    path(
        "products/created",
        TemplateView.as_view(template_name="products/success.html"),
        name="product-created",
    ),
    path("products/<str:id>", ProductShowView.as_view(), name="show"),
]
