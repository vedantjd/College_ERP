from django.urls import path, include
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('edit_members',views.edit_members,name='edit_members'),
    path('add_delete_class',views.add_delete_class,name='add_delete_class'),
    path('add_delete_HOD',views.add_delete_HOD,name='add_delete_HOD'),
    path('get_hods',views.get_hods,name='get_hods'),
    path('reset_password/', auth_views.PasswordResetView.as_view(),name="reset_password"),
    path('announce/',views.announce,name='announce'),
    path('presentation',views.presentation,name='presentation'),
    path('student/<slug:stud_id>/attendance/',
         views.attendance, name='attendance'),
    path('student/<slug:stud_id>/<slug:course_id>/attendance/',
         views.attendance_detail, name='attendance_detail'),
    path('student/<slug:class_id>/timetable/',
         views.timetable, name='timetable'),
    # path('student/<slug:class_id>/search/', views.student_search, name='student_search'),

    path('student/<slug:stud_id>/marks_list/',
         views.marks_list, name='marks_list'),

    path('teacher/<slug:teacher_id>/<int:choice>/Classes/',
         views.t_clas, name='t_clas'),
    path('teacher/<int:assign_id>/Students/attendance/',
         views.t_student, name='t_student'),
    path('teacher/<int:assign_id>/ClassDates/',
         views.t_class_date, name='t_class_date'),
    path('teacher/<int:ass_c_id>/Cancel/',
         views.cancel_class, name='cancel_class'),
    path('teacher/<int:ass_c_id>/attendance/',
         views.t_attendance, name='t_attendance'),
    path('teacher/<int:ass_c_id>/Edit_att/', views.edit_att, name='edit_att'),
    path('teacher/<int:ass_c_id>/attendance/confirm/',
         views.confirm, name='confirm'),
    path('teacher/<slug:stud_id>/<slug:course_id>/attendance/',
         views.t_attendance_detail, name='t_attendance_detail'),
    path('teacher/<int:att_id>/change_attendance/',
         views.change_att, name='change_att'),
    path('teacher/<int:assign_id>/Extra_class/',
         views.t_extra_class, name='t_extra_class'),
    path('teacher/<slug:assign_id>/Extra_class/confirm/',
         views.e_confirm, name='e_confirm'),
    path('teacher/<int:assign_id>/Report/', views.t_report, name='t_report'),

    path('teacher/<slug:teacher_id>/t_timetable/',
         views.t_timetable, name='t_timetable'),
    path('teacher/<int:asst_id>/Free_teachers/',
         views.free_teachers, name='free_teachers'),

    path('teacher/<int:assign_id>/marks_list/',
         views.t_marks_list, name='t_marks_list'),
    path('teacher/<int:assign_id>/Students/Marks/',
         views.student_marks, name='t_student_marks'),
    path('teacher/<int:marks_c_id>/marks_entry/',
         views.t_marks_entry, name='t_marks_entry'),
    path('teacher/<int:marks_c_id>/marks_entry/confirm/',
         views.marks_confirm, name='marks_confirm'),
    path('teacher/<int:marks_c_id>/Edit_marks/',
         views.edit_marks, name='edit_marks'),
    path('api/auth/', include('djoser.urls')),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('assign-teacher/', views.assign_teacher, name='assign_teacher'),
    path('get_d_teachers/<str:department_id>/', views.get_d_teachers, name='get_d_teachers'),
    path('get_d_teachers/<str:department_id>/subs', views.get_d_teachers_sub, name='get_d_teachers_sub'),
    path('get_d_teachers/<str:department_id>/classes', views.get_d_teachers_classes, name='get_d_teachers_classes'),
    path('add-student/', views.add_student, name='add_student'),
    path('add_delete_dept/',views.add_delete_dept,name='add_delete_dept')
    
]
admin.site.site_url = None
admin.site.site_header = 'My Site'
