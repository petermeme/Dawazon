from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('root', views.root, name='root'),
    path('about', views.about, name='about'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
#    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('checkout/', views.checkout, name='checkout'),
    path('oauth/success', views.oauth_success, name='test_oauth_success')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
