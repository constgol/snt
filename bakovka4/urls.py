"""bakovka4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', admin.site.urls),
    path('bakovka4/purpose/', views.purposeIndex, name='purpose_index'),
    path('bakovka4/purpose/<slug:purpose>/', views.purposeByYear, name='purpose_by_year'),
    path('bakovka4/purpose/<slug:purpose>/<int:year>/', views.purposeByMonth, name='purpose_by_month'),
    path('bakovka4/purpose/<slug:purpose>/<slug:year>/<int:land>', views.purposeByLand, name='purpose_by_land'),
]
