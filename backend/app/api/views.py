from rest_framework import viewsets, filters, response, Response
from backend.models.npc import NPC
from backend.models.encounter import Encounter
from backend.models.campaign import Campaign
from .serializers import NPCSerializer, EncounterSerializer, CampaignSerializer
from rest_framework.decorators import action
from backend.app.ai_services.gemini import GoogleGeminiProClient
from backend.app.ai_services.flux import FLUXClient
from backend.app.ai_services.prompts import get_prompt
import logging
from rest_framework import status
import os

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
        prompt_key = request.data.get('prompt_key', 'name_generation')
        user_prompt = request.data.get('prompt', '')
        prompt = get_prompt(prompt_key, user_prompt)

        ai_client = GoogleGeminiProClient()
        flux_client = FLUXClient()

        try:
            name = ai_client.generate_name(prompt)
            backstory = ai_client.generate_backstory(prompt)
        except Exception as e:
            logger.error(f"AI client error: {e}")
            return Response({'error': 'Failed to generate NPC details.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            portrait_url = flux_client.generate_profile_picture(prompt)
            if portrait_url:
                npc = NPC.objects.create(
                    name=name,
                    backstory=backstory,
                    # Additional fields...
                )
                local_image_path = os.path.join('media', f"npc_{npc.id}_portrait.jpg")
                flux_client.download_and_process_image(portrait_url, local_image_path)
                npc.portrait_url = local_image_path
                npc.save()
        except Exception as e:
            logger.error(f"FLUX client error: {e}")
            npc = NPC.objects.create(
                name=name,
                backstory=backstory,
                portrait_url=None,
                # Additional fields...
            )

        serializer = self.get_serializer(npc)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
