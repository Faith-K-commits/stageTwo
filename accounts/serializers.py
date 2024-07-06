from rest_framework import serializers
from .models import User, Organisation
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userId', 'firstName', 'lastName', 'email', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = User(
            email = validated_data['email'],
            firstName = validated_data['firstName'],
            lastName = validated_data['lastName'],
            phone=validated_data.get('phone')
        )
        user.password = make_password(validated_data['password'])
        user.save()
        
        org = Organisation.objects.create(
            orgId=validated_data['firstName'] + '_org',
            name=validated_data['firstName'] + "'s Organisation"
        )
        org.users.add(user)
        return user
    
class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'