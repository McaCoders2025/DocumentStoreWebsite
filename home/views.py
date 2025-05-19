import random
import pandas as pd
from .models import Student
from .forms import StudForm
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from .decorators import user_has_permission, admin_required, acadmission_required
from django.urls import reverse
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


User = get_user_model()

# @user_has_permission('home.can_access_landing_page')
def landing_page(request):
    return render(request, "landingpage.html")


def firstpage(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel']
        df = pd.read_excel(excel_file)

        for index, row in df.iterrows():
            data = row.to_dict()

            student = Student(
                name=data["name"],
                age=random.randint(20, 25),
                email=data["email"],
                address="Thane",
                # date=datetime.now(),
                rollnumber=int(data["rollnumber"]),
                physics=int(data["physics"]),
                chemistry=int(data["chemistry"]),
                maths=int(data["maths"]),
                english=int(data["english"]),
                totalmarks=int(data["Totalmarks"]),
                maxmarks=int(data["Maxmarks"]),
                percentage=int(data["Percentage"]),
                user=request.user  # Associate with the user who uploaded the file
            )
            student.save()

    return redirect("landing-page")



def stdetails(request):
    if request.method == "POST":
        st_form = StudForm(request.POST)
        if st_form.is_valid():
            print(st_form)
            st_form.save()
            return redirect('studentlist')
    else:
        st_form = StudForm()

    context = {'form': st_form}
    return render(request, "forms.html", context)



def studentlist(request):
    students = Student.objects.all()[::-1]
    return render(request, 'databaselist.html', {'students': students})


@login_required
def student_marksheet(request, email):
    student_details = Student.objects.filter(email=email).first()
    if student_details:
        return render(request, 'scorecard.html', {'student': student_details})
    else:
        messages.error(request, "No marksheet found for this student.")
        return redirect('landing-page')



# @user_has_permission('home.can_view_student_info')
# @login_required
def student_info(request, pk):
    student = Student.objects.get(id=pk)
    context = {'student': student}
    return render(request, 'display.html', context)


# @user_has_permission('home.can_view_student_score')
# @login_required
def student_score(request, pk):
    student = Student.objects.get(id=pk)
    context = {'student': student}
    return render(request, 'scorecard.html', context)


def login_page(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on group membership
                if user.groups.filter(name='Students').exists():
                    return redirect('student_marksheet', email=user.email)
                elif user.groups.filter(name='Acadmission').exists():
                    return redirect('landing-page')
                elif user.groups.filter(name='Admin').exists():
                    return redirect('studentlist')
                else:
                    return redirect('landing-page')
            else:
                messages.error(request, 'Invalid email or password')
        elif 'forgot_password' in request.POST:
            password_reset_form = PasswordResetForm(request.POST)
            if password_reset_form.is_valid():
                password_reset_form.save(
                    request=request,
                    use_https=True,
                    email_template_name='password_reset_email.html',
                    subject_template_name='password_reset_subject.txt',
                    from_email=None,
                )
                messages.success(request, 'A password reset link has been sent to your email.')
                return redirect('login_page')
            else:
                messages.error(request, 'Invalid email address')
    except Exception as e:
        print(f"{e=}")
    return render(request, 'login.html')



def register(request):
    if request.method == "POST":
        email = request.POST.get('emailaddress')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        group_name = request.POST.get('group')  # This should be the name of the group from the form

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'register.html')

        # Ensure the group_name is not empty and valid
        if not group_name:
            messages.error(request, "Group selection is required.")
            return render(request, 'register.html')

        try:
            # Create the user
            user = User.objects.create(email=email)
            user.set_password(password)
            user.save()

            # Add the user to the group
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

            messages.success(request, "Registration successful.")
            return redirect('login_page')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, 'register.html')

    return render(request, 'register.html')




# def send_email_to_student(request):
#     send_mail(
#         subject="Test",
#         message="This is a test message",
#         html_message="scorecard.html",
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=["sonishubham362409@gmail.com",]
#     )
#     return redirect('landing-page')

from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import os

@login_required
def send_email_to_student(request):
    if request.method == "POST":
        recipient_email = request.POST.get('email')

        file_path = 'marksheet_21.pdf'
        if not os.path.exists(file_path):
            return HttpResponse("Marksheet file not found.", status=404)

        try:
            email = EmailMessage(
                subject="Student Marksheet",
                body="Please find the attached marksheet.",
                from_email=settings.EMAIL_HOST_USER,
                to=[recipient_email],
            )
            email.attach_file(file_path)
            email.content_subtype = "html"
            email.send()

            # ✅ Redirect to landing page after success
            return redirect('landing-page')

        except Exception as e:
            return HttpResponse(f"Failed to send email: {str(e)}", status=500)

    # On GET, render the form
    return render(request, 'send_email_form.html')


def download_marksheet(request, rollnumber):
    # Replace with your model query to fetch the student object
    student = Student.objects.filter(rollnumber=rollnumber).first()  
    if not student:
        return HttpResponse("Student not found.", status=404)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="marksheet_{rollnumber}.pdf"'

    # Create a PDF canvas
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 50, f"Marksheet for {student.name} (Roll No: {student.rollnumber})")
    
    # Header Row
    p.setFont("Helvetica-Bold", 12)
    table_start_y = height - 120
    row_height = 20

    headers = ["Subject", "Marks"]
    x_positions = [100, 300]
    for i, header in enumerate(headers):
        p.drawString(x_positions[i], table_start_y, header)

    # Student Scores
    subjects = {
        "Physics": student.physics,
        "Chemistry": student.chemistry,
        "Maths": student.maths,
        "English": student.english,
    }
    p.setFont("Helvetica", 12)
    for idx, (subject, marks) in enumerate(subjects.items()):
        y = table_start_y - ((idx + 1) * row_height)
        p.drawString(x_positions[0], y, subject)
        p.drawString(x_positions[1], y, str(marks))

    # Totals and Percentage
    total_y = table_start_y - ((len(subjects) + 2) * row_height)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(x_positions[0], total_y, "Total Marks:")
    p.drawString(x_positions[1], total_y, str(student.totalmarks))

    percentage_y = total_y - row_height
    p.drawString(x_positions[0], percentage_y, "Percentage:")
    p.drawString(x_positions[1], percentage_y, f"{student.percentage:.2f}%")

    # Footer
    footer_y = percentage_y - (2 * row_height)
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(100, footer_y, "This is a system-generated marksheet.")

    # Finalize PDF
    p.showPage()
    p.save()

    return response

