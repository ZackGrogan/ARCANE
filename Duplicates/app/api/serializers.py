from rest_framework import serializers
from backend.models.npc import NPC
from backend.models.encounter import Encounter
from backend.models.campaign import Campaign

class NPCSerializer(serializers.ModelSerializer):
    spells = serializers.ListField(child=serializers.DictField(), required=False)
    equipment_data = serializers.ListField(child=serializers.DictField(), required=False)

    class Meta:
        model = NPC
        fields = '__all__'

class EncounterSerializer(serializers.ModelSerializer):
    monster_data = serializers.ListField(child=serializers.DictField(), required=False)

    class Meta:
        model = Encounter
        fields = '__all__'

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'
