from django.urls import path
from .views import CreateUserView,VerifyAPIView

urlpatterns = [
    path('signup/', CreateUserView.as_view()),
    path('verify-code/', VerifyAPIView.as_view()),
    # path('signup/', CreateUserView.as_view()),

]
