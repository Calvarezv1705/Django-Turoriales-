from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

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


class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": 500},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 999},
        {
            "id": "3",
            "name": "Chromecast",
            "description": "Best Chromecast",
            "price": 99,
        },
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 199},
    ]


class ProductIndexView(View):
    template_name = "products/index.html"

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = "products/show.html"

    def get(self, request, id):
        if not str(id).isdigit():
            return HttpResponseRedirect(reverse("home"))
        if int(id) < 1 or int(id) > len(Product.products):
            return HttpResponseRedirect(reverse("home"))
        viewData = {}
        product = Product.products[int(id) - 1]
        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)


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


class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero")
        return price


class ProductCreateView(View):
    template_name = "products/create.html"
    success_template = "products/success.html"

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            # Crear nuevo producto y agregarlo a la lista
            new_id = str(len(Product.products) + 1)
            new_product = {
                "id": new_id,
                "name": form.cleaned_data["name"],
                "description": "New product",
                "price": form.cleaned_data["price"],
            }
            Product.products.append(new_product)
            
            viewData = {}
            viewData["title"] = "Product created"
            viewData["message"] = "Product created successfully!"
            return render(request, self.success_template, viewData)
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)