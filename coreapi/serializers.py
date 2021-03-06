from ctypes.wintypes import HKEY
from rest_framework import serializers
from coreapi.models import Venue, HkuMember, Visit
class HkuMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = HkuMember
        fields = '__all__'
class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'
class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'
class VisitedVenuesSerializer(serializers.Serializer):
    venue = serializers.CharField()

class CloseContactsSerializer(serializers.Serializer):
    name = serializers.CharField()
    hku_id = serializers.CharField()
