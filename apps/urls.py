from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.views import (AddCategoryView, AddProductView, CategoryDeleteView,
                        CategoryProductListView, CategoryUpdateView,
                        DashboardView, GenerateStickersFromCSVView, LoginView,
                        ProductDeleteView, ProductUpdateView,
                        StickerGenerateView, SubscriptionExpiredView,
                        check_category_exists, landing_view, logout_user)

urlpatterns = [
#     ================== -- Login  ===============
    path("", landing_view, name="landing"),
    path("login/", csrf_exempt(LoginView.as_view()), name="login_page"),
    path("logout/", csrf_exempt(logout_user), name="logout"),
    path("dashboard/", csrf_exempt(DashboardView.as_view()), name="dashboard"),
    path("expired/", csrf_exempt(SubscriptionExpiredView.as_view()), name="subscription_expired"),
    path("categories/<uuid:pk>/products-add/", csrf_exempt(AddProductView.as_view()), name="products-add"),
    path("category-add/", csrf_exempt(AddCategoryView.as_view()), name="category-add"),
    path("products/<uuid:pk>/edit/", csrf_exempt(ProductUpdateView.as_view()), name="product-update"),
    path("products/<uuid:pk>/delete/", csrf_exempt(ProductDeleteView.as_view()), name="product-delete"),
    path("categories/<uuid:pk>/delete/", csrf_exempt(CategoryDeleteView.as_view()), name="category-delete"),
    path("categories/<uuid:pk>/update/", csrf_exempt(CategoryUpdateView.as_view()), name="category-update"),
    path("products/<uuid:id>/stickers/<str:sticker_type>/", csrf_exempt(GenerateStickersFromCSVView.as_view()),
         name="sticker-generate"),
    path("sticker-generate/<uuid:id>/", csrf_exempt(StickerGenerateView.as_view()), name="sticker-generate"),
    path("check-category/", csrf_exempt(check_category_exists), name="check-category"),
    path("categories/<uuid:pk>/", csrf_exempt(CategoryProductListView.as_view()), name="category-detail"),
]
