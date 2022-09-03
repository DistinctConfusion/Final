from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils import timezone
from urllib.parse import urlencode
import json
from itertools import chain
from datetime import datetime
import pytz

from document.models import Project,Specification,ProjectAccount,Changelog
from account.models import Account
from document.forms import ProjectForm, SpecificationForm

# Create your views here.
def project_view(request, *args, **kwargs):
    context = {}
    if not request.user.is_authenticated:
        return redirect("home")
    user_id = kwargs.get("user_id")
    account = Account.objects.get(pk=user_id)
    related_projects = ProjectAccount.objects.filter(collaborator=account)
    proj_list = []
    collab_list = []
    for p in related_projects:
        oneproject = Project.objects.get(proj_id=p.project_id)
        if oneproject.prev_iter is None and oneproject.deleted == False:
            proj_list.append(oneproject)
            collabs = ProjectAccount.objects.filter(project_id=oneproject.pk)
            for c in collabs:
                collab_list.append(c)
    spec_list = []
    for proj in proj_list:
        related_specs = Specification.objects.filter(related_proj=proj)
        for spec in related_specs:
            if spec.prev_iter is None and spec.deleted == False:
                spec_list.append(spec)
    
    
    context = {'projects': proj_list, 'specs': spec_list, 'collabs_list' : collab_list}

    return render(request, 'document/projects_view.html', context)

def project_detail(request, *args, **kwargs):
    context = {}
    if not request.user.is_authenticated:
        return redirect("home")
    project_id = kwargs.get("project_id")
    project = Project.objects.get(pk=project_id)
    related_specs = Specification.objects.filter(related_proj=project)
    spec_list = []
    for spec in related_specs:
        if spec.prev_iter is None and spec.deleted == False:
            spec_list.append(spec)
    context = {'specs': spec_list, 'proj_id' : project_id}

    return render(request, 'document/project_detail.html', context)

def project_add(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    user_id = kwargs.get("user_id")
    user2_id = kwargs.get("user2_id")
    account1 = Account.objects.get(pk=user_id)
    account2 = Account.objects.get(pk=user2_id)
    account_list=[account1,account2]
    context = {}
	
	#Change from here
    if request.POST:
        form = ProjectForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            new_proj = Project.objects.create(
            proj_name = form.cleaned_data['proj_name'],
			)
            new_proj.save()
            for acc in account_list:
                new_account_link = ProjectAccount.objects.create(
                    project_id = new_proj.proj_id,
                    collaborator = acc
                )
                new_account_link.save

            return redirect("document:projects_view", user_id=account1.pk)
        else:
            form = ProjectForm(request.POST, instance=request.user,
            initial={
			    "proj_name": form.cleaned_data.get('proj_name'),
			})
        context['form'] = form
    else:
        form = ProjectForm()
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, 'document/add_project.html', context)

def spec_add(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    id = kwargs.get("project_id")
    userid = kwargs.get("user_id")
    related_user = Account.objects.get(pk=userid)
    related_project = Project.objects.get(pk=id)
    context = {}
	
	#Change from here
    if request.POST:
        form = SpecificationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            new_spec = Specification.objects.create(
            spec_name = form.cleaned_data['spec_name'],
            description = form.cleaned_data['description'],
            related_proj = related_project
			)
            new_spec.save()

            if related_project.confirmed:
                new_changelog = Changelog.objects.create(
                    user = related_user,
                    project = related_project,
                    action = ' added specification ' + new_spec.spec_name + '  with the following description: ' + new_spec.description + ' at time: '
                )
                new_changelog.save()

            return redirect("document:projects_detail", project_id=id)
        else:
            form = SpecificationForm(request.POST, instance=request.user,
            initial={
			    "spec_name": form.cleaned_data.get('spec_name'),
                "description" : form.cleaned_data.get('description'),
			})
        context['form'] = form
    else:
        form = SpecificationForm()
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, 'document/add_specification.html', context)

def project_delete(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    project_id = kwargs.get("project_id")
    userid = kwargs.get("user_id")
    project = Project.objects.get(proj_id=project_id)
    project.deleted = True
    project.save()
    return redirect("document:projects_view", user_id=userid)

def spec_delete(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    id = kwargs.get("spec_id")
    userid = kwargs.get('user_id')
    specification = Specification.objects.get(spec_id=id)
    proj_id = specification.related_proj.proj_id
    related_project = Project.objects.get(pk=proj_id)
    related_user = Account.objects.get(pk=userid)
    specification.deleted = True
    specification.save()
    if related_project.confirmed:
        new_changelog = Changelog.objects.create(
        user = related_user,
        project = related_project,
        action = ' deleted specification ' + specification.spec_name + '  with the following description: ' + specification.description + ' at time: '
        )
        new_changelog.save()
    return redirect("document:projects_detail", project_id=proj_id)

def confirm_project(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    userid = kwargs.get("user_id")
    proj_id = kwargs.get("project_id")

    user = Account.objects.get(pk=userid)

    project_link = ProjectAccount.objects.get(collaborator=user, project_id=proj_id)
    project_link.user_confirm = not project_link.user_confirm
    project_link.save()

    project_links = ProjectAccount.objects.filter(project_id=proj_id)
    confirm_count = 0
    for link in project_links:
        if link.user_confirm is True:
            confirm_count += 1
    if confirm_count == 2:
        related_project = Project.objects.get(pk=proj_id)
        related_project.confirmed = True
        related_project.save()
    

    return redirect('document:projects_view', user_id=userid)


def archived_projects_view(request, *args, **kwargs):
    context = {}
    if not request.user.is_authenticated:
        return redirect("home")
    user_id = kwargs.get("user_id")
    account = Account.objects.get(pk=user_id)
    related_projects = ProjectAccount.objects.filter(collaborator=account)
    proj_list = []
    collab_list = []
    for p in related_projects:
        oneproject = Project.objects.get(proj_id=p.project_id)
        if oneproject.prev_iter is None and oneproject.deleted == True:
            proj_list.append(oneproject)
    spec_list = []
    for proj in proj_list:
        related_specs = Specification.objects.filter(related_proj=proj)
        for spec in related_specs:
            if spec.prev_iter is None and spec.deleted == False:
                spec_list.append(spec)
    
    
    context = {'projects': proj_list, 'specs': spec_list}

    return render(request, 'document/archived_projects_view.html', context)

def changelog_view(request, *args, **kwargs):
    context = {}
    if not request.user.is_authenticated:
        return redirect("home")
    
    project_id = kwargs.get('project_id')
    related_project = Project.objects.get(pk=project_id)
    related_changes = Changelog.objects.filter(project=related_project)
    changes = []
    for c in related_changes:
        changes.append(c)
    context = {'changelog' : changes}

    return render(request, 'document/changelog.html', context)