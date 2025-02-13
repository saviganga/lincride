from rest_framework import routers

from pricing import views as pricing_views

router = routers.DefaultRouter()

router.register(r"", pricing_views.PricingConfigurationViewSet, basename="pricing")

urlpatterns = []

urlpatterns += router.urls
