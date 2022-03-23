

# Django
from django.urls import path


# Views
from .views import *


urlpatterns = [
    path('programs/',ProgramsView.as_view()),
    path('programs/<str:id>/',ProgramsView.as_view()),
    path('programs/<str:id>/',ProgramsView.as_view()),
    path('program/<str:id>/',ProgramsView.as_view()),
    
    # Signature
    path('signature/<str:id>/<str:semester>/',SignatureView.as_view()),
    path('signature/<str:id>/<str:semester>/<str:signatureId>/',SignatureView.as_view()),
    
    # Item
    path('item/',ItemView.as_view()),
    path('item/<str:itemId>/',ItemView.as_view()),
    path('item-list/<str:signatureId>/',ItemView.as_view()),
    
    
    
    # Search urls
    path('search/',SearchView.as_view()),
    
]