#from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
#from dj_rest_auth.registration.views import SocialLoginView

#class GoogleLogin(SocialLoginView):
#    adapter_class = GoogleOAuth2Adapter

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.permissions import AllowAny

GOOGLE_CLIENT_ID = "900609376538-creikhrqkhuq82i7dh9lge3sg50526pi.apps.googleusercontent.com"

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        credential = request.data.get('credential')  # Get the JWT credential from the request
        if not credential:
            return Response({'error': 'No credential provided'}, status=status.HTTP_400_BAD_REQUEST)

        user_info = self.verify_google_credentials(credential)

        if user_info:
            # Do your server-side logic with user_info, such as creating or updating the user's account
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credential'}, status=status.HTTP_401_UNAUTHORIZED)

    def verify_google_credentials(self, credential):
        try:
            # Verify the JWT token
            idinfo = id_token.verify_oauth2_token(credential, requests.Request(), GOOGLE_CLIENT_ID)

            # Check if the user's email is verified
            if idinfo['email_verified']:
                # You can access user information in idinfo dictionary
                user_info = {
                    'user_id': idinfo['sub'],
                    'email': idinfo['email'],
                    'name': idinfo.get('name', ''),
                }
                return user_info
            else:
                # Email not verified
                return None
        except ValueError:
            # Invalid token
            return None
