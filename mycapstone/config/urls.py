from django.contrib import admin
from django.urls import path, include
from api.views import api_views


urlpatterns = [
    # path('test/', base_views.index, name='index'),  # 메인 페이지
    path('', api_views.apindex, name='apindex'),
    path('admin/', admin.site.urls),  # 관리자 페이지
    path('common/', include('common.urls')),  # common 앱의 urls.py 포함
    path('post/', include('post.urls')),
    path('api/', include('api.urls')),
    path('class/', include(('class.urls', 'class')))
    
]
