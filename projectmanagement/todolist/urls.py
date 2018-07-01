from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login-email',views.user_login,name='user_login'),
    url(r'^register-user',views.register_user,name='register_user'),
    url(r'^registration-page',views.registration_page,name='registration_page'),
    url(r'^logout',views.user_logout,name='user_logout'),
    url(r'^task/',views.task_details,name='task_details'), 
    url(r'^change-task-status/',views.change_task_status,name='change_task_status'), 
    url(r'^delete-task/',views.delete_task,name='delete_task'), 
    url(r'^edit-task/',views.edit_task,name='edit_task'), 
    url(r'^create-task/',views.create_task,name='create_task'), 
]