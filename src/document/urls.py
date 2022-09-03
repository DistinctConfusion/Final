from django.urls import path

from document.views import(
	archived_projects_view,
	changelog_view,
	confirm_project,
	project_detail,
	project_view,
    project_add,
    spec_add,
    project_delete,
    spec_delete,
)

app_name = 'document'

urlpatterns = [
	path('<user_id>/projects', project_view, name='projects_view'),
	path('<project_id>/detail', project_detail, name='projects_detail'),
    path('add/<user_id>/<user2_id>', project_add, name='projects_add'),
    path('/projects/<project_id>/specifications/<user_id>', spec_add, name='specifications_add'),
    path('<user_id>/projects/delete/<project_id>', project_delete, name='projects_del'),
    path('/projects/specifications/<spec_id>/<user_id>', spec_delete, name='spec_del'),
    path('/projects/confirm/<user_id>/<project_id>', confirm_project, name='proj_confirm'),
    path('<user_id>/projects/archived', archived_projects_view, name='archived_projects'),
    path('/projects/<project_id>/changelog', changelog_view, name='view_changelog'),
]