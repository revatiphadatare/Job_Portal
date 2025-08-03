from django.contrib import admin
from django.urls import path
from job.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('adminpanel/', admin.site.urls),
    path('', index, name='index'),
    path('admin_login/', admin_login, name='admin_login'),
    path('admin_home/', admin_home, name='admin_home'),
    path('user_managemen/', user_management, name='user_management'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('update_user_role/<int:user_id>/', update_user_role, name='update_user_role'),
    path('reports/', reports, name='reports'),
    path('view_user/', view_user, name='view_user'),
    path('view_recruiter/', view_recruiter, name='view_recruiter'),
    path('logout/', logout_view, name='logout'),
    path('user_signup/', user_signup, name='user_signup'),
    path('user_login/', user_login, name='user_login'),
    path('user_home/', user_home, name='user_home'),
    path('user_logout/', user_logout, name='user_logout'),
    path('recruiter_signup/', recruiter_signup, name='recruiter_signup'),
    path('recruiter_login/', recruiter_login, name='recruiter_login'),
    path('newsletter_signup/', newsletter_signup, name='newsletter_signup'),
    path('latest_job/', latest_job, name='latest_job'),
    path('change_password/', change_password, name='change_password'),
    path('recruiter_home/', recruiter_home, name='recruiter_home'),
    path('contact/', contact_us, name='contact_us'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
