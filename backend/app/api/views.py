from rest_framework import viewsets, filters
from backend.models.npc import NPC
from backend.models.encounter import Encounter
from backend.models.campaign import Campaign
from .serializers import NPCSerializer, EncounterSerializer, CampaignSerializer

class NPCViewSet(viewsets.ModelViewSet):
    queryset = NPC.objects.all()
    serializer_class = NPCSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'race', 'class_type']
    ordering_fields = ['name', 'level']

class EncounterViewSet(viewsets.ModelViewSet):
    queryset = Encounter.objects.all()
    serializer_class = EncounterSerializer

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
