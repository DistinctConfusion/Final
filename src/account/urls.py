from django.urls import path

from account.views import (
	account_view,
	add_post,
	edit_account_view,
	crop_image,
	edit_status_view,
	gallery,
)

app_name = 'account'

urlpatterns = [

	path('<user_id>/', account_view, name="view"),
	path('<user_id>/edit/', edit_account_view, name="edit"),
	path('<user_id>/status/', edit_status_view, name="update_status"),
	path('<user_id>/edit/cropImage/', crop_image, name="crop_image"),
	path('<user_id>/home', gallery, name="account_home"),
	path('<user_id>/add',add_post ,name="add_post")

	
]