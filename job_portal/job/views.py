from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import StudentUser,RecruiterUser

def user_signup(request):
    error = ""
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')
        image = request.FILES.get('image')
        resume = request.FILES.get('resume')

        if password != confirm_password:
            error = "yes"
        else:
            try:
                user = User.objects.create_user(username=username, password=password, first_name=full_name)
                StudentUser.objects.create(
                    user=user,
                    email=email,
                    mobile=mobile,
                    gender=gender,
                    image=image,
                    resume=resume, 
                    type="student"
                )
                error = "no"
            except Exception as ex:
                print("Signup error:", ex)
                error = "yes"

    return render(request, 'user_signup.html', {'error': error})


def user_login(request):
    error = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            try:
                profile = StudentUser.objects.get(user=user)
                if profile.type == "student":
                    login(request, user)
                    error = "no"
                else:
                    error = "yes"
            except StudentUser.DoesNotExist:
                error = "yes"
        else:
            error = "yes"

    return render(request, 'user_login.html', {'error': error})


def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    return render(request, 'user_home.html')


def user_logout(request):
    logout(request)
    return redirect('index')

def recruiter_signup(request):
    success = False
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        contact = request.POST.get("contact_number")
        company = request.POST.get("company_name")
        gender = request.POST.get("gender")
        image = request.FILES.get("profile_picture")

        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password, first_name=full_name, email=email)
                RecruiterUser.objects.create(
                    user=user,
                    company_name=company,
                    contact_number=contact,
                    gender=gender,
                    profile_picture=image
                )
                success = True
            except:
                success = False
        else:
            success = False
    return render(request, "recruiter_signup.html", {"success": success})

def recruiter_login(request):
    success = False
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            try:
                recruiter = RecruiterUser.objects.get(user=user)
                login(request, user)
                success = True
                return render(request, "recruiter_login.html", {"success": success})
            except RecruiterUser.DoesNotExist:
                success = False
        else:
            success = False
    return render(request, "recruiter_login.html", {"success": success})

def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect("recruiter_login")
    return render(request, "recruiter_home.html")


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_home')
        else:
            messages.error(request, "Invalid credentials or not an admin user.")
    
    return render(request, 'admin_login.html')



def user_management(request):
    users = StudentUser.objects.select_related('user').order_by('-id')
    return render(request, 'user_management.html', {'users': users})

def delete_user(request, user_id):
    user_obj = get_object_or_404(StudentUser, id=user_id)
    if request.method == 'POST':
        user_obj.user.delete()
        user_obj.delete()
        return redirect('user_management')
    return render(request, 'delete_user.html', {'user': user_obj})


def update_user_role(request, user_id):
    user_obj = get_object_or_404(StudentUser, id=user_id)
    if request.method == 'POST':
        new_type = request.POST.get('type')
        user_obj.type = new_type
        user_obj.save()
        return redirect('user_management')
    return render(request, 'update_user_role.html', {'user': user_obj})

def reports(request):
    total_users = StudentUser.objects.count()
    total_recruiters = RecruiterUser.objects.count()
    recent_users = StudentUser.objects.select_related('user').order_by('-id')[:5]
    recent_recruiters = RecruiterUser.objects.select_related('user').order_by('-id')[:5]

    context = {
        'total_users': total_users,
        'total_recruiters': total_recruiters,
        'recent_users': recent_users,
        'recent_recruiters': recent_recruiters,
    }
    return render(request, 'reports.html', context)




def view_user(request):
    users = StudentUser.objects.all().order_by('-id')  # Fetch all users, latest first
    context = {
        'users': users
    }
    return render(request, 'view_user.html', context)


def view_recruiter(request):
    recruiters = RecruiterUser.objects.select_related('user').all().order_by('-id')
    return render(request, 'view_recruiter.html', {'recruiters': recruiters})

# def settings_view(request):
#     return render(request, 'settings.html')

def logout_view(request):
    logout(request)
    return redirect('admin_login')
 


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect("admin_login")
    return render(request, "admin_home.html")


def index(request):
    return render(request, 'index.html')


def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(f"Newsletter signup received: {email}")
        messages.success(request, "Thank you for subscribing!")
    return redirect('index')


            



def latest_job(request):
    # Simulated job data (replace with API or scraping logic)
    jobs = [
        {
            "title": "Executive Assistant",
            "company": "Jobs For All",
            "location": "India",
            "posted": "2025-07-21",
            "link": "https://in.bebee.com/job/034c1ed116f6b8790e6a32f3901f87b2"
        },
        {
            "title": "Sales Manager",
            "company": "The Career Company India",
            "location": "Bengaluru",
            "posted": "2025-07-22",
            "link": "https://in.linkedin.com/jobs/view/sales-manager-at-the-career-company-india-4268530647"
        },
        {
            "title": "Engineering Manager",
            "company": "Branch International",
            "location": "India",
            "posted": "2025-07-21",
            "link": "https://in.bebee.com/job/4d97867c493bf2d6ee93526910798410"
        }
    ]
    return render(request, 'latest_job.html', {'jobs': jobs})

def change_password(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    # Add password change logic here
    return render(request, 'change_password.html')



def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # You could store this in the database or email it to admin
        print(f"Contact Us Message:\nFrom: {name} <{email}>\nSubject: {subject}\nMessage: {message}")

        messages.success(request, "Thanks for reaching out! We'll get back to you shortly.")
        return render(request, 'contact_us.html', {'success': True})

    return render(request, 'contact_us.html')