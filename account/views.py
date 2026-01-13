from django.contrib.auth.models import User
from rest_framework import viewsets,status
from account.serializers import CustomTokenObtainPairSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

class UserViewsets(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.request.method=="POST":
            return [AllowAny()]
        return super().get_permissions()

    def create(self, request):
        serializer=UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class LoginMixin(viewsets.ViewSet):
    '''
        User login with either Jwt token or Two Factor auth
    '''
    custom_serializer = CustomTokenObtainPairSerializer
    queryset = User.objects.all()
    permission_classes = ()
 
   
    def create(self, request, *args, **kwargs):
        '''
        User login with Jwt token
        params : username , password
        return : Jwt token
        '''
        serializer = self.custom_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)