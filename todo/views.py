from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from todo.models import Register,Task,Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
# Create your views here.
def home(request):
    return render(request,'home.htm')
def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        address2 = request.POST.get("address2", "").strip()

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register_page')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register_page')
        if not all([first_name, last_name, username, email, password]):
            messages.error(request, "All fields are required.")
            return redirect("register_page")


        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
        )
        user.set_password(password, "").strip()
        user.is_active = True
        user.save()


        Register.objects.create(
            user=user,
            phone=phone,
            address=address,
            address2=address2
        )

        messages.success(request, 'Account created successfully')
        return redirect('login_page')

    return render(request, 'register.htm')
@csrf_protect
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Login successful')
                return redirect('todo_page')
            else:
                messages.error(request, 'Your account is inactive. Please contact admin.')
        else:
            messages.error(request, 'Invalid username or password')

        return redirect('login_page')

    return render(request, 'login.htm')
def logout_page(request):
    logout(request)
    return redirect('login_page')
@login_required
def todo_page(request):
    tasks = Task.objects.all()
    usernames = User.objects.all()

    if request.method == "POST":
        task_name = request.POST.get('task_name')
        owner_username = request.POST.get('ownername')
        payer_username = request.POST.get('payername')

        try:
            owner = User.objects.get(username=owner_username)
            payer = User.objects.get(username=payer_username)
        except User.DoesNotExist:
            messages.error(request, "Owner or Payer does not exist.")
            return redirect('todo_page')

        Task.objects.create(
            task_name=task_name,
            owner=owner,
            payer=payer,
        )
        return redirect('todo_page')

    return render(request, 'todos.htm', {
        'usernames': usernames,
        'tasks': tasks
    })

def delete_item(request, id):
    task = get_object_or_404(Task, id=id)
    if request.user == task.owner or request.user.is_superuser:
        task.delete()
        messages.success(request, "Task deleted successfully.")
        return redirect('todo_page')

    # ❌ Others are forbidden
    return HttpResponseForbidden("You are not allowed to delete this task.")

def update_item(request, id):
    task = get_object_or_404(Task, id=id)

    # ✅ ALLOW owner or superuser
    if request.user != task.owner and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to update this task.")

    if request.method == "POST":
        task.task_name = request.POST.get('task_name')
        owner_username = request.POST.get('ownername')
        payer_username = request.POST.get('payername')

        try:
            task.owner = User.objects.get(username=owner_username)
            task.payer = User.objects.get(username=payer_username)
        except User.DoesNotExist:
            messages.error(request, "Owner or Payer not found.")
            return redirect('update_item', id=id)

        task.completed = True
        task.save()
        messages.success(request, "Task updated successfully.")
        return redirect('todo_page')

    usernames = User.objects.all()
    return render(request, 'update_task.htm', {'task': task, 'usernames': usernames})
@login_required
def delete_orphan_tasks(request):
    if request.user.is_superuser:
        deleted_count, _ = Task.objects.filter(owner=None).delete()
        return HttpResponse(f"✅ Deleted {deleted_count} orphan task(s).")
    return HttpResponseForbidden("You are not authorized to perform this action.")

def contact_page(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        message=request.POST.get("message")
        Contact.objects.create(name=name,email=email,message=message)
        messages.success(request,'Detail sent successfully')
        return redirect('contact_page')

    return render(request,'contact.htm')
def about_page(request):
    return render(request,'about.htm')