from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.views import  LoginView, DashboardView, SubscriptionExpiredView, AddProductView, ProductUpdateView, \
    ProductDeleteView, GenerateStickersFromCSVView, StickerGenerateView, logout_user, \
    AddCategoryView, check_category_exists, CategoryDeleteView, CategoryUpdateView, CategoryProductListView

# ProductListView,ProductDetailView,ProductPatchView,GenerateStickersFromCSV
# #
# urlpatterns = [
#     path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
#     path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
#     path('products-create/', ProductCreateView.as_view(), name='product-create'),
#     path('products-list/', ProductListView.as_view(), name='products-list'),
#     path('delete_product/', ProductDetailView.as_view(), name='delete'),
#     path('update_product/<int:id>/patch', ProductPatchView.as_view(), name='update'),
#     path("products/<int:id>/stickers/<str:sticker_type>/", GenerateStickersFromCSV.as_view(),
#     name="create_stickers_from_csv"),
# ]

urlpatterns = [
#     ================== -- Login  ===============
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
    path("products/<uuid:id>/stickers/<str:sticker_type>/", GenerateStickersFromCSVView.as_view(),name="sticker-generate"),
    path("sticker-generate/<uuid:id>/", StickerGenerateView.as_view(),name="sticker-generate"),
    path("check-category/", check_category_exists, name="check-category"),
    path("categories/<uuid:pk>/", CategoryProductListView.as_view(), name="category-detail"),
]
