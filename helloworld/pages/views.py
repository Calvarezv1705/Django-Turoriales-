from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, TemplateView

from .models import Product


# Create your views here.
class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "About us - Online Store",
                "subtitle": "About us",
                "description": "This is an about page ...",
                "author": "Developed by: Your Name",
            }
        )
        return context


class ProductIndexView(View):
    template_name = "products/index.html"

    def get(self, request):
        view_data = {}
        view_data["title"] = "Products - Online Store"
        view_data["subtitle"] = "List of products"
        view_data["products"] = Product.objects.all()
        return render(request, self.template_name, view_data)


class ProductShowView(View):
    template_name = "products/show.html"

    def get(self, request, id):
        # Check if product id is valid
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            # If the product id is not valid, redirect to the home page
            return HttpResponseRedirect(reverse("home"))

        view_data = {}
        view_data["title"] = product.name + " - Online Store"
        view_data["subtitle"] = product.name + " - Product information"
        view_data["product"] = product
        return render(request, self.template_name, view_data)


class ContactPageView(TemplateView):
    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "Contact - Online Store",
                "subtitle": "Contact",
                "email": "info@onlinestore.test",
                "address": "123 Main Street, Springfield",
                "phone": "+1 (555) 123-4567",
            }
        )
        return context


class ProductForm(forms.ModelForm):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    class Meta:
        model = Product
        fields = ["name", "price"]

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price <= 0:
            raise ValidationError("Price must be greater than zero.")
        return price


class ProductCreateView(View):
    template_name = "products/create.html"

    def get(self, request):
        form = ProductForm()
        view_data = {}
        view_data["title"] = "Create product"
        view_data["form"] = form
        return render(request, self.template_name, view_data)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product-created")
        else:
            view_data = {}
            view_data["title"] = "Create product"
            view_data["form"] = form
            return render(request, self.template_name, view_data)


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Products - Online Store"
        context["subtitle"] = "List of products"
        return context
