from django.forms import ModelForm
from .models import Job, Project


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['company_name', 'title', 'link',
                  'salary_min', 'salary_max', 'date']


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'link']