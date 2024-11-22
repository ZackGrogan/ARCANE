from rest_framework import viewsets, filters, response, Response
from backend.models.npc import NPC
from backend.models.encounter import Encounter
from backend.models.campaign import Campaign
from .serializers import NPCSerializer, EncounterSerializer, CampaignSerializer
from rest_framework.decorators import action
from backend.app.ai_services.gemini import GoogleGeminiProClient
from backend.app.ai_services.flux import FLUXClient
import logging

logger = logging.getLogger(__name__)

class NPCViewSet(viewsets.ModelViewSet):
    queryset = NPC.objects.all()
    serializer_class = NPCSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'race', 'class_type']
    ordering_fields = ['name', 'level']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def generate(self, request):
        prompt = request.data.get('prompt', '')
        ai_client = GoogleGeminiProClient()
        flux_client = FLUXClient()

        try:
            name = ai_client.generate_name(prompt)
            backstory = ai_client.generate_backstory(prompt)
            portrait_url = flux_client.generate_profile_picture(prompt)
        except Exception as e:
            logger.error(f"AI service error: {e}")
            return Response({'error': 'Failed to generate NPC details.'}, status=500)

        npc = NPC.objects.create(
            name=name,
            backstory=backstory,
            portrait_url=portrait_url,
            # Include additional fields as necessary
        )
        serializer = self.get_serializer(npc)
        return Response(serializer.data)

class EncounterViewSet(viewsets.ModelViewSet):
    queryset = Encounter.objects.all()
    serializer_class = EncounterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
