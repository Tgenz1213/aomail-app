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
import requests
import logging

GOOGLE_CLIENT_ID = "900609376538-creikhrqkhuq82i7dh9lge3sg50526pi.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        credential = request.data.get('credential')  # Get the JWT credential from the request
        if not credential:
            return Response({'error': 'No credential provided'}, status=status.HTTP_400_BAD_REQUEST)

        user_info = self.verify_google_credentials(credential)

        if user_info:
            # Do your server-side logic with user_info, such as creating or updating the user's account
            return Response({
                'message': 'Login successful',
                'googleToken': credential  # Include the Google token in the response
            }, status=status.HTTP_200_OK)
        else:
            # Handle the case where the Google credentials are invalid
            return Response({'error': 'Invalid Google credentials'}, status=status.HTTP_401_UNAUTHORIZED)

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

class GoogleOAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        
        logging.info('POST request received at /oauth/callback')

        authorization_code = request.data.get('code')  # Get the authorization code from the request
        if not authorization_code:
            logging.warning('No authorization code provided')
            return Response({'error': 'No authorization code provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange the authorization code for tokens
        data = {
            'code': authorization_code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': 'http://localhost:8080/signup_part2',
            'grant_type': 'authorization_code'
        }
        response = requests.post(GOOGLE_TOKEN_URL, data=data)
        tokens = response.json()

        if 'error' in tokens:
            logging.error(f'Invalid authorization code: {tokens["error"]}')
            return Response({'error': 'Invalid authorization code'}, status=status.HTTP_401_UNAUTHORIZED)

        user_info = self.verify_google_token(tokens['id_token'])

        if user_info:
            logging.info(f'Login successful for user: {user_info["email"]}')
            # Do your server-side logic with user_info, such as creating or updating the user's account
            #return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            access_token = tokens.get('access_token', '')
            refresh_token = tokens.get('refresh_token', '')
            return Response({
                'message': 'Login successful',
                'token': tokens,
            }, status=status.HTTP_200_OK)
        else:
            logging.error('Invalid token')
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

    def verify_google_token(self, id_token):
        try:
            # Verify the ID token
            idinfo = requests.get(f'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={id_token}').json()
            if idinfo['aud'] == GOOGLE_CLIENT_ID:
                user_info = {
                    'user_id': idinfo['sub'],
                    'email': idinfo['email'],
                    'name': idinfo.get('name', ''),
                }
                return user_info
            else:
                logging.error(f'Token verification failed: {idinfo}')
                return None
        except ValueError:
            logging.exception('Exception occurred while verifying token')
            return None