import datetime
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    email=serializers.EmailField(required=True)
    re_password=serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        if attrs['re_password']!=attrs['password']:
            raise serializers.ValidationError("isn't match")
        return super().validate(attrs)
    
    def validate_email(self,email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("you cannot duplicate the email")
        return email
    
    class Meta:
        model=User 
        fields=["id","username","first_name","last_name","email","is_active","password","re_password"]
        extra_kwargs = {"password": {"write_only": True}}
    
    def create(self,validated_date):
        user= User.objects.create_user(email=self.validated_data['email'],
                                  first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            username=self.validated_data['username'],
            password=self.validated_data["password"])
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        User.objects.filter(id=user.id).update(
            last_login=datetime.datetime.now())
        user.save()
        token = super().get_token(user)
        # Add custom claims
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["email"] = user.email
        token["user_type"] = "normal user"  
        return token