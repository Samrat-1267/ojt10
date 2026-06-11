from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, UserProfileForm, UserInfoForm, AddressForm
from .models import Address
from orders.models import Order
from custom_pc_builder.models import SavedBuild


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserInfoForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        user_form = UserInfoForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def address_list(request):
    addresses = request.user.addresses.all()
    return render(request, 'accounts/address_list.html', {'addresses': addresses})


@login_required
def address_add(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            if address.is_default:
                Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
            address.save()
            messages.success(request, 'Address added successfully.')
            return redirect('accounts:addresses')
    else:
        form = AddressForm()
    return render(request, 'accounts/address_form.html', {'form': form, 'title': 'Add Address'})


@login_required
def address_edit(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            if form.cleaned_data['is_default']:
                Address.objects.filter(user=request.user, is_default=True).exclude(pk=pk).update(is_default=False)
            form.save()
            messages.success(request, 'Address updated successfully.')
            return redirect('accounts:addresses')
    else:
        form = AddressForm(instance=address)
    return render(request, 'accounts/address_form.html', {'form': form, 'title': 'Edit Address'})


@login_required
def address_delete(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    messages.success(request, 'Address deleted.')
    return redirect('accounts:addresses')


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'accounts/order_history.html', {'orders': orders})


@login_required
def saved_builds(request):
    builds = SavedBuild.objects.filter(user=request.user)
    return render(request, 'accounts/saved_builds.html', {'builds': builds})
