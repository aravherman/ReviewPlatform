from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('shop/<int:shop_id>/',views.shop_det,name='shop_detail'),
    path('add-shop/',views.add_shop,name='add_shop'),
    path('del-shop/',views.del_shop,name='del_shop'),
    path('upd-shop/',views.upd_shop,name='upd_shop'),
    path('login/',views.login_view,name='login'),
    path('logout/', views.logt, name='logout'),
    path('register/', views.regt, name='register'),
    path('review/<int:review_id>/upvote/', views.upvote, name='upvote'),
    path('review/<int:review_id>/downvote/', views.downvote, name='downvote'),
]