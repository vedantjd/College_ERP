from django.shortcuts import render,redirect,get_list_or_404
from info.models import Student,Teacher,Dept,time_slots,DAYS_OF_WEEK,HOD
from .models import Announcement
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.

@login_required
def announcement_page(request):
    if request.method == 'POST':
        title = request.POST['titles']
        content = request.POST['content']
        Depts = request.POST['dept']
        category=''
        if(Depts=='All'):
            category='all'
            print(category)
        else:
            category+=Depts
            print(category)
        current_user=request.user
        name=current_user.first_name+' '+current_user.last_name
        print(current_user.first_name+' '+current_user.last_name)
        new_announce=Announcement(title=title, content=content, categories=category, announcer=name)
        new_announce.save()
        messages.success(request,"Announced Sucessfully")
        return redirect('/')
    if  request.user.is_teacher:
        current_user=request.user
        names=current_user.first_name+' '+current_user.last_name
        teacher=Teacher.objects.get(name=names)
        deptsofannounce=teacher.dept_id
        print(deptsofannounce,teacher)
        announcements = get_list_or_404(Announcement, categories=deptsofannounce)
    else:
        announcements = Announcement.objects.all().order_by('-timestamp')
        # print(request.user.is_teacher)
    all_dept = Dept.objects.order_by('-id')
    all_hod = HOD.objects.order_by('-id')
    context = {'all_dept': all_dept,'announcements': announcements,'all_hod':all_hod} 
    return render(request, 'announce.html',context=context)
