import base64
from datetime import timedelta

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class LoginAPI(APIView):
    def post(self, request):
        username, password = self.extract_basic_credentials(request)
        user = authenticate(username=username, password=password)
        if user:
            access_token = AccessToken.for_user(user)
            access_token.set_exp(lifetime=timedelta(days=5))
            return Response({
                "access_token": str(access_token),
            })
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def extract_basic_credentials(request):
        auth = request.headers.get('Authorization', b'').split()
        if len(auth) == 2 and auth[0].lower() == 'basic':
            credentials = base64.b64decode(auth[1]).decode('utf-8')
            username, password = credentials.split(':', 1)
            return username, password

        return None, None