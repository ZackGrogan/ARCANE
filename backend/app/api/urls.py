from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NPCViewSet, EncounterViewSet, CampaignViewSet

router = DefaultRouter()
router.register(r'npcs', NPCViewSet)
router.register(r'encounters', EncounterViewSet)
router.register(r'campaigns', CampaignViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
