from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import authentication_classes, permission_classes

from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    
    # Create User
    def create(self, validated_data):
        # Extract the password
        password = validated_data.pop('password', None)
        
        # Assign `CustomUser` model's data to `instance` object
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        
        instance.save()
        return instance

    # Update User
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value) # Apply `set_password` function 
            else:
                setattr(instance, attr, value) # Update the instance with new value

        instance.save()
        return instance
    
    class Meta:    
        # Model to be serialized
        model = CustomUser
        
        # Fields to be serialized 
        fields = ('name', 'email', 'password', 'phone', 'gender', 'is_active', 'is_staff', 'is_superuser') 
        
        # Make the password inaccessible in GET request and don't show in plain text  
        extra_kwargs = {
            'password':{
                'write_only':True,
                'style':{'input_type':'password'}
            }
        }