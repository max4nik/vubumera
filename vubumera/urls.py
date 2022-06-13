"""vubumera URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


from elections.views import RegisterUserAPI, RetrieveElectionsAPI, LocationsAPI, LoginUserAPI, VotingAPI, \
    ElectionsAPI, StatisticAPI, GetElection, UnvoteAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/voter/register/', RegisterUserAPI.as_view(), name='user-management'),
    path('api/voter/login/', LoginUserAPI.as_view(), name='user-management'),
    path('api/locations', LocationsAPI.as_view(), name='locations'),
    path('api/elections/user/<int:user_id>', RetrieveElectionsAPI.as_view(), name='retrieve-elections'),
    path('api/elections/<int:election_id>', GetElection.as_view(), name='get-election'),
    path('api/statistics/<int:user_id>', StatisticAPI.as_view(), name='statistics'),
    path('api/vote/<int:user_id>', VotingAPI.as_view(), name='vote'),
    path('api/unvote/<int:user_id>/election/<int:election_id>', UnvoteAPI.as_view(), name='unvote'),
    path('api/election/details/<int:user_id>/<int:election_id>', ElectionsAPI.as_view(), name='election-details'),
]
