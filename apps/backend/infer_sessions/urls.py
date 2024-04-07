from rest_framework import routers

from .views import InferSessionViewSet

router = routers.SimpleRouter()
router.register(r'', InferSessionViewSet)

urlpatterns = router.urls
