from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Note
from django.contrib import messages
from .forms import UserRegistrationForm, LoginForm, NoteForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# ==========================
# REGISTER
# ==========================


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, 'Passwords do not match')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                messages.success(request, 'Account created successfully')
                return redirect('notes:login')  # changed namespace to notes
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})

# ==========================
# LOGIN
# ==========================


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('notes:list')  # notes namespace
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})

# ==========================
# LOGOUT
# ==========================


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('notes:login')  # notes namespace

# ==========================
# NOTES LIST
# ==========================


@login_required(login_url='notes:login')  # notes namespace
def note_list_view(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'notes/note_list.html', {'notes': notes})

# ==========================
# CREATE NOTE
# ==========================


@login_required(login_url='notes:login')
def note_create_view(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, 'Note created successfully')
            return redirect('notes:list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form})

# ==========================
# UPDATE NOTE
# ==========================


@login_required(login_url='notes:login')
def note_update_view(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully')
            return redirect('notes:list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form})

# ==========================
# DELETE NOTE
# ==========================


@login_required(login_url='notes:login')
def note_delete_view(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully')
        return redirect('notes:list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})
