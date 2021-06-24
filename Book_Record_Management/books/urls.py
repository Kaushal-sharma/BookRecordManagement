from django.urls import path
from books import views

urlpatterns = [
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('dashboard/', views.dashboard),
    path('booktable/', views.addTable), # This is calling from 'Add book' sidelink and 'Add Book' button
    path('showresult/', views.showResult),
    path('edit/', views.editform),
    path('update/', views.update),
    path('delete/', views.delete),
]