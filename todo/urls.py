from django.contrib import admin
from django.urls import path,include
from todo import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    
     path('',views.home,name="home"),
     path('register/',views.register_page,name="register_page"),
     path('login/',views.login_page,name="login_page"),
     path('logout/',views.logout_page,name="logout_page"),
     path('todos/',views.todo_page,name="todo_page"),
     path('delete/<id>/',views.delete_item,name="delete_item"),
     path('update/<id>/',views.update_item,name="update_item"),
     path('delete-orphan-tasks/', views.delete_orphan_tasks, name='delete_orphan_tasks'),
     path('contact/', views.contact_page, name='contact_page'),
     path('about/', views.about_page, name='about_page')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)