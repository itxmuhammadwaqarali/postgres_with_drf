from django.urls import path
from .views import CreateUserView, DeleteUserView, MyTokenObtainPairView, LogoutView

urlpatterns = [
    path('create/', CreateUserView.as_view()),
    path('delete/<int:pk>/', DeleteUserView.as_view()),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='token_logout'),
]
