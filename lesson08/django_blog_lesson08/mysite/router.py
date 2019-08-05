from rest_framework import routers
from api.viewsets import BloggingViewSet

router = routers.DefaultRouter()
router.register('blogging', BloggingViewSet, base_name='blogging')

for post in router.urls:
    print(post, '\n')
