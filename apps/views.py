import csv
import io
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_GET
from django.views.generic import DeleteView, DetailView, ListView, UpdateView
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, get_object_or_404

from .forms import CategoryForm, LoginForm, ProductForm
from .models import Category, Product
from .serializers import ProductSerializer
from .utils import (generate_code128_png_bytes, generate_sticker_58x40,
                    generate_sticker_70x40, generate_sticker_100x50)


def landing_view(request):
    return render(request, "app/landing_page.html")


@login_required
@require_GET
def check_category_exists(request):
    name = request.GET.get("name", "").strip()
    exists = Category.objects.filter(user=request.user, name__iexact=name).exists()
    return JsonResponse({"exists": exists})


class LoginView(View):
    template_name = "app/login.html"
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user:
                if not user.check_subscription():
                    print(f"{request.user} eskirgan user")
                    return redirect("subscription_expired")
                login(request, user)
                return redirect("dashboard")
            # faqat authenticate None qaytarganda error qo‘yamiz
            messages.error(request, "Email yoki parol noto‘g‘ri!")
        return render(request, self.template_name, {"form": form})


def logout_user(request):
    logout(request)
    return redirect('login_page')


class DashboardView(LoginRequiredMixin, ListView):
    template_name = "app/category_dashboard.html"
    model = Category
    context_object_name = "categories"

    def get_queryset(self):
        query_set = Category.objects.filter(user=self.request.user)
        search = self.request.GET.get("search")
        if search:
            query_set = query_set.filter(name__icontains=search)
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["email"] = self.request.user.email
        return context


class SubscriptionExpiredView(View):
    template_name = "app/expired.html"

    def get(self, request):
        context = {
            "admin_phone": "+998 90 123 45 67",
            "admin_email": "admin@example.com",
        }
        return render(request, self.template_name, context)


class AddCategoryView(LoginRequiredMixin, View):
    success_url = reverse_lazy("dashboard")

    def post(self, request):
        form = CategoryForm(request.POST, user=request.user)  # userni formaga beramiz
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, "Kategoriya muvaffaqiyatli qo‘shildi!")
            return redirect(self.success_url)
        else:
            messages.error(request, "Xatolik: " + str(form.errors))
            return redirect("category-add")


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "app/category_dashboard.html"
    success_url = reverse_lazy("dashboard")

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "app/category_dashboard.html"
    context_object_name = "category"

    def get_success_url(self):
        return reverse_lazy("dashboard")

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryProductListView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = "app/category_products.html"
    context_object_name = "category"

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = self.object.products.filter(user=self.request.user)
        return context


class AddProductView(LoginRequiredMixin, View):
    template_name = "app/product_form.html"

    def get(self, request, pk):
        form = ProductForm()
        category = get_object_or_404(Category, id=pk, user=request.user)
        return render(request,
                      self.template_name,
                      {"form": form, "category_id": pk, "category": category},
                      )

    def post(self, request, pk):
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user

            category = get_object_or_404(Category, id=pk, user=request.user)
            product.category = category

            product.save()
            messages.success(request, "Mahsulot muvaffaqiyatli qo‘shildi!")
            return redirect('category-detail', pk=category.pk)

        messages.error(request, "Iltimos, formadagi xatolarni tekshiring.")
        return render(request, self.template_name, {"form": form, "category_id": pk})


class ProductCreateView(LoginRequiredMixin, CreateAPIView):
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        category = serializer.validated_data.get("category")
        if category.user != self.request.user:
            raise PermissionDenied("Bunday kategoriya sizga tegishli emas")
        serializer.save(user=self.request.user)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "app/product-update.html"
    context_object_name = "product"

    def get_success_url(self):
        return reverse_lazy("category-detail", kwargs={"pk": self.object.category.pk})

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.object.category
        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "app/product-update.html"
    success_url = reverse_lazy("dashboard")

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)


class GenerateStickersFromCSVView(LoginRequiredMixin, View):

    def post(self, request, id, sticker_type, *args, **kwargs):

        uploaded_csv = request.FILES.get("csv_file")
        if not uploaded_csv:
            return JsonResponse({"error": "CSV file is required"}, status=400)
        product = get_object_or_404(Product, id=id, user=request.user)
        # PDF folderAPIView
        stickers_dir = os.path.join(settings.MEDIA_ROOT, "stickers")
        os.makedirs(stickers_dir, exist_ok=True)
        pdf_path = os.path.join(stickers_dir, f"stickers_product_{product.id}.pdf")
        # Sticker size selection
        sticker_type = sticker_type.upper()
        if sticker_type == "100X50MM":
            width, height = 100 * mm, 50 * mm
            generate_func = generate_sticker_100x50
        elif sticker_type == "58X40MM":
            width, height = 58 * mm, 40 * mm
            generate_func = generate_sticker_58x40
        elif sticker_type == "70X40MM":
            width, height = 70 * mm, 40 * mm
            generate_func = generate_sticker_70x40
        else:
            return JsonResponse({"error": "Invalid sticker type"}, status=400)
        c = canvas.Canvas(pdf_path, pagesize=(width, height))
        # Barcode generated once
        barcode_buf = generate_code128_png_bytes(
            product.barcode,
            module_width=12,
            module_height=28,
            quiet_zone=4,
            font_size=8,
        )
        barcode_img = ImageReader(barcode_buf)
        # Read CSV rows
        reader = csv.reader(io.StringIO(uploaded_csv.read().decode("utf-8")))
        for idx, row in enumerate(reader, start=1):
            if not row:
                continue
            gs1_code = row[0].strip()
            generate_func(c, product, gs1_code, idx, barcode_img, width, height)
        c.save()
        return FileResponse(open(pdf_path, "rb"), as_attachment=True, filename=f"stickers_{product.id}.pdf")


class StickerGenerateView(View):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id, user=request.user)
        return render(request, "app/sticker_generator.html", {"product": product})
