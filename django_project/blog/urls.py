from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_class/', views.create_classroom, name='create-classroom'),
    path('join_class/', views.join_classroom, name='join-classroom'),
    path('dashboard/classroom/<int:classroom_id>/', views.classroom, name='classroom'),
    path('dashboard/classroom/<int:classroom_id>/create_forum/', views.create_forum, name='create-forum'),
    path('dashboard/classroom/<int:classroom_id>/<int:forum_id>/', views.forum, name='forum'),
    path('dashboard/classroom/<int:classroom_id>/<int:forum_id>/<int:post_id>', views.reply, name='reply'),
    path('dashboard/classroom/<int:classroom_id>/<int:forum_id>/<int:post_id>/pin/', views.pin_post, name='pin'),
    path('dashboard/classroom/<int:classroom_id>/<int:forum_id>/<int:post_id>/unpin/', views.unpin_post, name='unpin'),
    path('dashboard/classroom/<int:classroom_id>/create_exam/', views.create_exam, name='create_exam'),
    path('dashboard/classroom/<int:classroom_id>/exams/<int:exam_id>/', views.exam_page, name='exam'),
    path('dashboard/classroom/<int:classroom_id>/exams/<int:exam_id>/score/<int:response_id>', views.submit_score,
         name='score')
]
