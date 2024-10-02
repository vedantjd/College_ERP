from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Dept, Class, Student, Attendance, Course,HOD, Teacher, Assign, AttendanceTotal, time_slots, \
    DAYS_OF_WEEK, AssignTime, AttendanceClass, StudentCourse, Marks, MarksClass
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib import messages
User = get_user_model()
from .forms import ToggleForm
# Create your views here.


@login_required
def index(request):
    if request.user.is_teacher:
        return render(request, 'info/t_homepage.html')
    if request.user.is_student:
        return render(request, 'info/homepage.html')
    if request.user.is_superuser:
        return render(request, 'info/admin_homepage.html')
    return render(request, 'info/logout.html')

@login_required
def edit_members(request):
    if request.user.is_superuser:
        return render(request, 'info/admin_page.html')
    return render(request, 'info/logout.html')

@login_required
def announce(request):
    return render(request, 'info/test.html')

@login_required()
def attendance(request, stud_id):
    stud = Student.objects.get(USN=stud_id)
    ass_list = Assign.objects.filter(class_id_id=stud.class_id)
    att_list = []
    for ass in ass_list:
        try:
            a = AttendanceTotal.objects.get(student=stud, course=ass.course)
        except AttendanceTotal.DoesNotExist:
            a = AttendanceTotal(student=stud, course=ass.course)
            a.save()
        att_list.append(a)
    return render(request, 'info/attendance.html', {'att_list': att_list})


@login_required()
def attendance_detail(request, stud_id, course_id):
    stud = get_object_or_404(Student, USN=stud_id)
    cr = get_object_or_404(Course, id=course_id)
    att_list = Attendance.objects.filter(course=cr, student=stud).order_by('date')
    return render(request, 'info/att_detail.html', {'att_list': att_list, 'cr': cr})


# Teacher Views

@login_required
def t_clas(request, teacher_id, choice):
    teacher1 = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'info/t_clas.html', {'teacher1': teacher1, 'choice': choice})


@login_required()
def t_student(request, assign_id):
    ass = Assign.objects.get(id=assign_id)
    att_list = []
    for stud in ass.class_id.student_set.all():
        try:
            a = AttendanceTotal.objects.get(student=stud, course=ass.course)
        except AttendanceTotal.DoesNotExist:
            a = AttendanceTotal(student=stud, course=ass.course)
            a.save()
        att_list.append(a)
    return render(request, 'info/t_students.html', {'att_list': att_list})


@login_required()
def t_class_date(request, assign_id):
    now = timezone.now()
    ass = get_object_or_404(Assign, id=assign_id)
    att_list = ass.attendanceclass_set.filter(date__lte=now).order_by('-date')
    return render(request, 'info/t_class_date.html', {'att_list': att_list})


@login_required()
def cancel_class(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    assc.status = 2
    assc.save()
    return HttpResponseRedirect(reverse('t_class_date', args=(assc.assign_id,)))


@login_required()
def t_attendance(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    ass = assc.assign
    c = ass.class_id
    context = {
        'ass': ass,
        'c': c,
        'assc': assc,
    }
    return render(request, 'info/t_attendance.html', context)


@login_required()
def edit_att(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    cr = assc.assign.course
    att_list = Attendance.objects.filter(attendanceclass=assc, course=cr)
    context = {
        'assc': assc,
        'att_list': att_list,
    }
    return render(request, 'info/t_edit_att.html', context)


@login_required()
def confirm(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    ass = assc.assign
    cr = ass.course
    cl = ass.class_id
    for i, s in enumerate(cl.student_set.all()):
        status = request.POST[s.USN]
        if status == 'present':
            status = 'True'
        else:
            status = 'False'
        if assc.status == 1:
            try:
                a = Attendance.objects.get(course=cr, student=s, date=assc.date, attendanceclass=assc)
                a.status = status
                a.save()
            except Attendance.DoesNotExist:
                a = Attendance(course=cr, student=s, status=status, date=assc.date, attendanceclass=assc)
                a.save()
        else:
            a = Attendance(course=cr, student=s, status=status, date=assc.date, attendanceclass=assc)
            a.save()
            assc.status = 1
            assc.save()

    return HttpResponseRedirect(reverse('t_class_date', args=(ass.id,)))


@login_required()
def t_attendance_detail(request, stud_id, course_id):
    stud = get_object_or_404(Student, USN=stud_id)
    cr = get_object_or_404(Course, id=course_id)
    att_list = Attendance.objects.filter(course=cr, student=stud).order_by('date')
    return render(request, 'info/t_att_detail.html', {'att_list': att_list, 'cr': cr})


@login_required()
def change_att(request, att_id):
    a = get_object_or_404(Attendance, id=att_id)
    a.status = not a.status
    a.save()
    return HttpResponseRedirect(reverse('t_attendance_detail', args=(a.student.USN, a.course_id)))


@login_required()
def t_extra_class(request, assign_id):
    ass = get_object_or_404(Assign, id=assign_id)
    c = ass.class_id
    context = {
        'ass': ass,
        'c': c,
    }
    return render(request, 'info/t_extra_class.html', context)


@login_required()
def e_confirm(request, assign_id):
    ass = get_object_or_404(Assign, id=assign_id)
    cr = ass.course
    cl = ass.class_id
    assc = ass.attendanceclass_set.create(status=1, date=request.POST['date'])
    assc.save()

    for i, s in enumerate(cl.student_set.all()):
        status = request.POST[s.USN]
        if status == 'present':
            status = 'True'
        else:
            status = 'False'
        date = request.POST['date']
        a = Attendance(course=cr, student=s, status=status, date=date, attendanceclass=assc)
        a.save()

    return HttpResponseRedirect(reverse('t_clas', args=(ass.teacher_id, 1)))


@login_required()
def t_report(request, assign_id):
    ass = get_object_or_404(Assign, id=assign_id)
    sc_list = []
    for stud in ass.class_id.student_set.all():
        a = StudentCourse.objects.get(student=stud, course=ass.course)
        sc_list.append(a)
    return render(request, 'info/t_report.html', {'sc_list': sc_list})


@login_required()
def timetable(request, class_id):
    asst = AssignTime.objects.filter(assign__class_id=class_id)
    matrix = [['' for i in range(10)] for j in range(6)]

    for i, d in enumerate(DAYS_OF_WEEK):
        t = 0
        for j in range(9):
            if j == 0:
                matrix[i][0] = d[0]
                continue
            if j == 4 or j == 7:
                continue
            try:
                a = asst.get(period=time_slots[t][0], day=d[0])
                matrix[i][j] = a.assign.course.shortname
            except AssignTime.DoesNotExist:
                pass
            t += 1

    context = {'matrix': matrix}
    return render(request, 'info/timetable.html', context)


@login_required()
def t_timetable(request, teacher_id):
    asst = AssignTime.objects.filter(assign__teacher_id=teacher_id)
    class_matrix = [[True for i in range(10)] for j in range(6)]
    for i, d in enumerate(DAYS_OF_WEEK):
        t = 0
        for j in range(9):
            if j == 0:
                class_matrix[i][0] = d[0]
                continue
            if j == 4 or j == 7:
                continue
            try:
                a = asst.get(period=time_slots[t][0], day=d[0])
                class_matrix[i][j] = a
            except AssignTime.DoesNotExist:
                pass
            t += 1
    print(class_matrix)

    context = {
        'class_matrix': class_matrix,
    }
    return render(request, 'info/t_timetable.html', context)


@login_required()
def free_teachers(request, asst_id):
    asst = get_object_or_404(AssignTime, id=asst_id)
    ft_list = []
    t_list = Teacher.objects.filter(assign__class_id__id=asst.assign.class_id_id)
    for t in t_list:
        is_free = True
        at_list = AssignTime.objects.filter(assign__teacher=t)
        for at in at_list:
            if at.period == asst.period and at.day == asst.day:
                is_free = False
                break
        if is_free:
            ft_list.append(t)
    return render(request, 'info/free_teachers.html', {'ft_list': ft_list})


# student marks


@login_required()
def marks_list(request, stud_id):
    stud = Student.objects.get(USN=stud_id, )
    ass_list = Assign.objects.filter(class_id_id=stud.class_id)
    sc_list = []
    for ass in ass_list:
        try:
            sc = StudentCourse.objects.get(student=stud, course=ass.course)
        except StudentCourse.DoesNotExist:
            sc = StudentCourse(student=stud, course=ass.course)
            sc.save()
            sc.marks_set.create(type='I', name='Class Test 1')
            sc.marks_set.create(type='I', name='Midsem Exam')
            sc.marks_set.create(type='I', name='Class Test 2')
            sc.marks_set.create(type='E', name='Event 1')
            sc.marks_set.create(type='E', name='Event 2')
            sc.marks_set.create(type='S', name='End Semester Exam')
        sc_list.append(sc)

    return render(request, 'info/marks_list.html', {'sc_list': sc_list})


# teacher marks


@login_required()
def t_marks_list(request, assign_id):
    ass = get_object_or_404(Assign, id=assign_id)
    m_list = MarksClass.objects.filter(assign=ass)
    return render(request, 'info/t_marks_list.html', {'m_list': m_list})


@login_required()
def t_marks_entry(request, marks_c_id):
    mc = get_object_or_404(MarksClass, id=marks_c_id)
    ass = mc.assign
    c = ass.class_id
    context = {
        'ass': ass,
        'c': c,
        'mc': mc,
    }
    return render(request, 'info/t_marks_entry.html', context)


@login_required()
def marks_confirm(request, marks_c_id):
    mc = get_object_or_404(MarksClass, id=marks_c_id)
    ass = mc.assign
    cr = ass.course
    cl = ass.class_id
    for s in cl.student_set.all():
        mark = request.POST[s.USN]
        sc = StudentCourse.objects.get(course=cr, student=s)
        m = sc.marks_set.get(name=mc.name)
        m.marks1 = mark
        m.save()
    mc.status = True
    mc.save()

    return HttpResponseRedirect(reverse('t_marks_list', args=(ass.id,)))


@login_required()
def edit_marks(request, marks_c_id):
    mc = get_object_or_404(MarksClass, id=marks_c_id)
    cr = mc.assign.course
    stud_list = mc.assign.class_id.student_set.all()
    m_list = []
    for stud in stud_list:
        sc = StudentCourse.objects.get(course=cr, student=stud)
        m = sc.marks_set.get(name=mc.name)
        m_list.append(m)
    context = {
        'mc': mc,
        'm_list': m_list,
    }
    return render(request, 'info/edit_marks.html', context)


@login_required()
def student_marks(request, assign_id):
    ass = Assign.objects.get(id=assign_id)
    sc_list = StudentCourse.objects.filter(student__in=ass.class_id.student_set.all(), course=ass.course)
    return render(request, 'info/t_student_marks.html', {'sc_list': sc_list})


@login_required()
def add_teacher(request):
    if not request.user.is_superuser:
        return redirect("/")

    if request.method == 'POST':
        dept = get_object_or_404(Dept, id=request.POST['dept'])
        name = request.POST['full_name']
        id = request.POST['id'].lower()
        dob = request.POST['dob']
        sex = request.POST['sex']
        
        # Creating a User with teacher username and password format
        # USERNAME: firstname + underscore + unique ID
        # PASSWORD: firstname + underscore + year of birth(YYYY)
        user = User.objects.create_user(
            username=name.split(" ")[0].lower() + '_' + id,
            password=name.split(" ")[0].lower() + '_' + dob.replace("-","")[:4],
            first_name=name.split(" ")[0].lower(),
            last_name=name.split(" ")[1].lower()
        )
        user.save()

        Teacher(
            user=user,
            id=id,
            dept=dept,
            name=name,
            sex=sex,
            DOB=dob
        ).save()
        return redirect('/')
    
    all_dept = Dept.objects.order_by('-id')
    context = {'all_dept': all_dept}

    return render(request, 'info/add_teacher.html', context)


@login_required()
def assign_teacher(request):
    if not request.user.is_superuser:
        return redirect("/")

    if request.method == 'POST':
        f_name = request.POST['f_names']
        classes = request.POST['classes_lists']
        course = request.POST['subjectss']
        time_slot=request.POST['slotss']
        days=request.POST['day']
        form = ToggleForm(request.POST)
        if form.is_valid():
            a_or_d = form.cleaned_data['checkbox']
        else:
            a_or_d = False
        if(a_or_d==True):
            assist=AssignTime.objects.all()
            
            is_free = True
            for assist in assist:
                assigned_class = AssignTime.objects.filter(period=assist.period).first()
                class_id_at_specific_slot = assigned_class.assign.class_id_id
                if time_slot == assist.period and days == assist.day and class_id_at_specific_slot==classes:
                    
                    print(class_id_at_specific_slot)
                    is_free = False
                    break
            if is_free:
                class_obj = Class.objects.get(id=classes)
                assign_teacher_to_slot=Assign.objects.filter(class_id=class_obj,course_id=course,teacher_id=f_name)
                if(str(assign_teacher_to_slot) == '<QuerySet []>' ):
                    assign_teacher=Assign(class_id=class_obj,course_id=course,teacher_id=f_name)
                    assign_teacher.save()
                else:
                    assign_teacher=Assign.objects.get(class_id=class_obj,course_id=course,teacher_id=f_name)

                assig_slot=AssignTime(assign=assign_teacher,period=time_slot,day=days)
                assig_slot.save()
                messages.success(request, 'Assigned successfully!')
            else:
                messages.success(request, 'Slot is Full!')

        else:
            assist=AssignTime.objects.all()
            is_free = True
            for assist in assist:
                if time_slot == assist.period and days == assist.day:
                    is_free = False
                    break
            if is_free:
                messages.success(request, 'Slot is Empty!')
            else:
                print("Not free")
                class_obj = Class.objects.get(id=classes)
                assign_teacher_to_slot=Assign.objects.filter(class_id=class_obj,course_id=course,teacher_id=f_name).exists()
                if(assign_teacher_to_slot):
                    assign_teacher=Assign.objects.get(class_id=class_obj,course_id=course,teacher_id=f_name)
                    AssignTime.objects.filter(assign=assign_teacher,period=time_slot,day=days).delete()
                    messages.success(request, 'De-Assigned successfully!')
                else:
                    messages.success(request, 'No Data Found!')
                    
                    
        return redirect('/')
    else:
        form = ToggleForm()
    slot=[]
    daysofweek=[]
    all_dept = Dept.objects.order_by('-id')
    for i in time_slots:
        slot.append(i[0])
    for i in DAYS_OF_WEEK:
        daysofweek.append(i[0])
    context = {'all_dept': all_dept,'timeslots':slot,'days':daysofweek} 

    return render(request, 'info/assign_teacher.html', context)


@login_required()
def add_delete_dept(request):
    if not request.user.is_superuser:
        return redirect("/")

    if request.method == 'POST':
        form = ToggleForm(request.POST)
        if form.is_valid():
            a_or_d = form.cleaned_data['checkbox']
        else:
            a_or_d = False
        if(a_or_d==True):
            Depts = request.POST['depts']
            id = request.POST['ids']
            assist=Dept.objects.all()
            is_free = True
            for assist in assist:
                if id == assist.id:
                    is_free = False
                    break
            if is_free:
                add_dept=Dept(id=id,name=Depts)
                add_dept.save()
                messages.success(request, 'Added successfully!')
            else:
                print("Already Present!!!")
                messages.success(request, 'Already Present!!!')
        else:
            Depts = request.POST['departments']
            assist=Dept.objects.all()
            is_free = True
            for assist in assist:
                if Depts == assist.id:
                    is_free = False
                    break
            if is_free:
                print("Department not found!!!")
                messages.success(request, 'Department not found!!!')
            else:
                print("Deleted")
                Dept.objects.filter(id=Depts).delete()
                messages.success(request, 'Deleted successfully!')
                
                    
                    
        return redirect('/')
    else:
        form = ToggleForm()
    slot=[]
    daysofweek=[]
    all_dept = Dept.objects.order_by('-id')
    for i in time_slots:
        slot.append(i[0])
    for i in DAYS_OF_WEEK:
        daysofweek.append(i[0])
    context = {'all_dept': all_dept,'timeslots':slot,'days':daysofweek} 

    return render(request, 'info/add_dept.html', context)



@login_required()
def add_delete_class(request):
    if not request.user.is_superuser:
        return redirect("/")

    if request.method == 'POST':
        form = ToggleForm(request.POST)
        if form.is_valid():
            a_or_d = form.cleaned_data['checkbox']
        else:
            a_or_d = False
        if(a_or_d==True):
            classes = request.POST['classes']
            depts = request.POST['departments']
            sections=request.POST['sect']
            sems = request.POST['sem']
            assist=Class.objects.all()
            is_free = True
            for assist in assist:
                if classes == assist.id:
                    is_free = False
                    break
            if is_free:
                add_class=Class(id=classes,section=sections,sem=sems,dept_id=depts)
                add_class.save()
                messages.success(request, 'Added successfully!')
            else:   
                print("Already Present!!!")
                messages.success(request, 'Already Present!!!')
        else:
            Depts = request.POST['clas']
            assist=Class.objects.all()
            is_free = True
            for assist in assist:
                if Depts == assist.id:
                    is_free = False
                    break
            if is_free:
                print("Class not found!!!")
                messages.success(request, 'Class not found!!!')
            else:
                Class.objects.filter(id=Depts).delete()
                messages.success(request, 'Deleted successfully!')
        return redirect('/')
    else:
        form = ToggleForm()
    all_dept = Dept.objects.order_by('-id')
    # print(Class.objects.filter(id='CSE2B'))
    context = {'all_dept': all_dept} 
    return render(request, 'info/add_class.html', context)





@login_required()
def add_delete_HOD(request):
    if not request.user.is_superuser:
        return redirect("/")

    if request.method == 'POST':
        
        Depts = request.POST['dept']
        ids = request.POST['f_names']
        assist=HOD.objects.all()
        for assists in assist:
              if str(Depts) == str(assists.department.id):
                  HOD.objects.filter(department=assists.department).delete()
                  break
        Depts=Dept.objects.get(id=Depts)
        get_hod= Teacher.objects.get(id=ids)
        print(get_hod.id)
        add_dept=HOD(hod_id=get_hod,department=Depts)
        add_dept.save()
        messages.success(request, 'Added successfully!')
        return redirect("/")
    slot=[]
    daysofweek=[]
    all_dept = Dept.objects.order_by('-id')
    for i in time_slots:
        slot.append(i[0])
    for i in DAYS_OF_WEEK:
        daysofweek.append(i[0])
    context = {'all_dept': all_dept,'timeslots':slot,'days':daysofweek} 

    return render(request, 'info/add_HOD.html', context)



@login_required()
def get_d_teachers(request,department_id):
    if not request.user.is_superuser:
        return redirect("/")
    try:
        subjects = Teacher.objects.filter(dept_id=department_id).values('id','name')
        # print(subjects)
        # Query the subjects related to the selected department and fetch id and name fields
        return JsonResponse(list(subjects), safe=False)
    except Teacher.DoesNotExist:
        return JsonResponse([], safe=False)

@login_required()
def get_d_teachers_classes(request,department_id):
    if not request.user.is_superuser:
        return redirect("/")
    try:
        subjects = Class.objects.filter(dept=department_id).values('id')
        
        # Query the subjects related to the selected department and fetch id and name fields
        return JsonResponse(list(subjects), safe=False)
    except Teacher.DoesNotExist:
        return JsonResponse([], safe=False)

@login_required()
def get_d_teachers_sub(request,department_id):
    if not request.user.is_superuser:
        return redirect("/")
    try:
        subjects = Course.objects.filter(dept=department_id).values('id','name')
        
        # Query the subjects related to the selected department and fetch id and name fields
        return JsonResponse(list(subjects), safe=False)
    except Teacher.DoesNotExist:
        return JsonResponse([], safe=False)

@login_required()
def add_student(request):
    # If the user is not admin, they will be redirected to home
    if not request.user.is_superuser:
        return redirect("/")

    if request.method == 'POST':
        # Retrieving all the form data that has been inputted
        class_id = get_object_or_404(Class, id=request.POST['class'])
        name = request.POST['full_name']
        usn = request.POST['usn']
        dob = request.POST['dob']
        sex = request.POST['sex'] 

        # Creating a User with student username and password format
        # USERNAME: firstname + underscore + last 3 digits of USN
        # PASSWORD: firstname + underscore + year of birth(YYYY)
        user = User.objects.create_user(
            username=name.split(" ")[0].lower() + '_' + request.POST['usn'][-3:],
            password=name.split(" ")[0].lower() + '_' + dob.replace("-","")[:4],
            first_name=name.split(" ")[0].lower(),
            last_name=name.split(" ")[1].lower()

        )
        user.save()

        # Creating a new student instance with given data and saving it.
        Student(
            user=user,
            USN=usn,
            class_id=class_id,
            name=name,
            sex=sex,
            DOB=dob
        ).save()
        return redirect('/')
    
    all_classes = Class.objects.order_by('-id')
    context = {'all_classes': all_classes}
    return render(request, 'info/add_student.html', context)

@login_required()
def get_hods(request):
    hods= HOD.objects.all().values()
    hod=[]
    for i in hods:
        lists=[]
        print(i)
        get_hod= Teacher.objects.filter(id=i['hod_id_id']).values('name','dept')
        get_dept = Dept.objects.filter(id=get_hod[0]['dept']).values('name')
        # print(i['name'],get_dept[j]['name'])
        lists.append(i['hod_id_id'])
        lists.append(get_hod[0]['name'])
        lists.append(get_dept[0]['name'])
        hod.append(lists)
    try:
        print(hod)
        # Query the subjects related to the selected department and fetch id and name fields
        return JsonResponse(hod, safe=False)
    except Teacher.DoesNotExist:
        return JsonResponse([], safe=False)


def presentation(request):
    return render(request,"info/presentation.html")