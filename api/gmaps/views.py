from rest_framework import viewsets
from .models import User, Gmap
from .serializers import UserSerializer, GmapSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from hashlib import md5
from rest_framework.views import APIView
import pdb


class HealthCheckView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        return Response({'status': 'ok'})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes=[]
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class GmapViewSet(viewsets.ModelViewSet):
    queryset = Gmap.objects.all()
    serializer_class = GmapSerializer
    
    def get_permissions(self):
        permission_classes=[]
        if self.action == 'list' or self.action == 'public_search':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(magic_word="").order_by('-created_at')[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def public_search(self, request):
        # breakpoint()
        username = request.query_params.get('username')
        birth = request.query_params.get('birth')
        gmaps = Gmap.objects.filter(user__username=username, user__birth=birth, magic_word="")
        serializer = self.get_serializer(gmaps, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def private_search(self, request):
        email = request.query_params.get('email')
        magic_word = request.query_params.get('magic_word')
        magic_word_hash = md5(magic_word.encode()).hexdigest()
        gmaps = Gmap.objects.filter(user__email=email).filter(Q(magic_word=magic_word_hash) & ~Q(magic_word=""))
        serializer = self.get_serializer(gmaps, many=True)
        return Response(serializer.data)
