

# Django
from django.urls import path


# Views
from .views import *


urlpatterns = [
    
    # Program urls
    path('program/',ProgramsView.as_view()),
    path('program/<str:programId>/',ProgramsView.as_view()),
    path('program/<str:programId>/<str:semester>/',ProgramsView.as_view()),
    path('program/<str:programId>/<str:semester>/<str:signatureId>/',ProgramsView.as_view()),
    path('program/<str:programId>/<str:semester>/<str:signatureId>/<str:itemId>/',ProgramsView.as_view()),
     
     
    # Item urls
    path('item/',ItemView.as_view()),
    path('item/<str:itemId>/',ItemView.as_view()),

     
    # Search urls
    path('search/',SearchView.as_view())
    
]