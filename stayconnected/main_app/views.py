from django.shortcuts import render, redirect
from .models import Project, Job, Profile, Photo
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
import uuid
import boto3

# Add the following import

from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
import uuid
import boto3

# Add the following import
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'sei-stay-connected'

# Define the home view


S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'sei-stay-connected'

# Define the home view


def home(request):
    return HttpResponseRedirect('/about/')

def about(request):
    return render(request, 'about.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user, 'this is the user')
            print(dir(user))
            login(request, user)

            profile = Profile(user=user, username=user.username)
            print(profile)
            profile.save()
            return redirect('index')

        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def profile_index(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile/detail.html', {'profile':profile}) 
    

class ProjectList(LoginRequiredMixin, ListView):
    model = Project
    template = 'job_list.html'


class JobList(ListView):
    model = Job


class JobDetail(DetailView):
    model = Job


class JobCreate(LoginRequiredMixin, CreateView):
    model = Job
    fields = '__all__'


class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Project


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    fields = '__all__'


class JobUpdate(LoginRequiredMixin, UpdateView):
    model = Job
    fields = '__all__'


class JobDelete(LoginRequiredMixin, DeleteView):
    model = Job
    success_url = '/profile/'  


class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    fields = '__all__'


class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = '/profile/'  



# hi this is working while we are all in different folders

def add_photo(request):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url)
        except:
            print('An error occurred uploading file to S3')
    return redirect('photo_list')

class PhotoList(ListView):
    model = Photo
    template = 'photo_list.html'
