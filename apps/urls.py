from django.urls import path

from apps.views import (AddCategoryView, AddProductView, CategoryDeleteView,
                        CategoryProductListView, CategoryUpdateView,
                        DashboardView, GenerateStickersFromCSVView, LoginView,
                        ProductDeleteView, ProductUpdateView,
                        StickerGenerateView, SubscriptionExpiredView,
                        check_category_exists, landing_view, logout_user)

urlpatterns = [
#     ================== -- Login  ===============
    path("", landing_view, name="landing"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("expired/", SubscriptionExpiredView.as_view(), name="subscription_expired"),
    path("categories/<uuid:pk>/products-add/", AddProductView.as_view(), name="products-add"),
    path("category-add/", AddCategoryView.as_view(), name="category-add"),
    path("products/<uuid:pk>/edit/", ProductUpdateView.as_view(), name="product-update"),
    path("products/<uuid:pk>/delete/", ProductDeleteView.as_view(), name="product-delete"),
    path("categories/<uuid:pk>/delete/", CategoryDeleteView.as_view(), name="category-delete"),
    path("categories/<uuid:pk>/update/", CategoryUpdateView.as_view(), name="category-update"),
    path("products/<uuid:id>/stickers/<str:sticker_type>/", GenerateStickersFromCSVView.as_view(),
         name="sticker-generate"),
    path("sticker-generate/<uuid:id>/", StickerGenerateView.as_view(), name="sticker-generate"),
    path("check-category/", check_category_exists, name="check-category"),
    path("categories/<uuid:pk>/", CategoryProductListView.as_view(), name="category-detail"),
]
