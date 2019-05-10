from django.urls import path
from rollback import yanzheng
from rollback import views,insert_mysql

urlpatterns = [
    path('', views.roll_login),
    path('verification_code',views.create_code_img),
    path('user_verification',views.user_verification),
    path('index.html',views.roll_homepage),
    path('roll_project',views.project_web),
    path('exit',views.delete_session),
    path('rollbacking',views.rollback_api),
    path('rollbackingceshi',views.rollbackingceshi),
    #insert
    path('insert_project.html',insert_mysql.insert_project),
    path('add_project.html',insert_mysql.judge_server),
    path('add_server',insert_mysql.add_server),
    path('add_server.html',insert_mysql.add_server),
    path('del_project.html',insert_mysql.delete_project),
    path('api_del_project',insert_mysql.delete_project),
    #user
    path('userinfo.html',views.user_info),
    path('update_password',views.update_password),
    path('adduser.html',views.add_user),
    path('add_user',views.add_user_api),
    #test
    path('test/concurrent_test.html',views.concurrent_test),
]
