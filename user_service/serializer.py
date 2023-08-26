from .models import User,Account,Part,Position
from rest_framework import serializers

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'
    
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    part = PartSerializer()
    position = PositionSerializer()
    class Meta:
        model = User
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Account
        fields = '__all__'
        