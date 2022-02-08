from django.urls import path
from . import views

urlpatterns=[
    path('', views.Student_List.as_view(), name='student'),
    path('intake/', views.Intake_List.as_view(), name='intake'),
    path('student/<id>', views.StudentDetailsAPI.as_view(), name='student1'),

]