from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from aomail.models import Signature, SocialAPI
from aomail.utils.serializers import SignatureSerializer
from django.http import HttpRequest
import json

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_signature(request: HttpRequest) -> Response:
    """
    Create a new email signature for the authenticated user and specified SocialAPI.
    
    Args:
        request (HttpRequest): HTTP request containing:
            email (str): Email of the SocialAPI.
            signature_content (str): The signature content.
    Returns:
        Response: JSON response with signature data or error message.
    """
    try:
        data = json.loads(request.body)
        email = data.get('email')
        signature_content = data.get('signature_content')
        
        try:
            social_api = SocialAPI.objects.get(email=email, user=request.user)
        except SocialAPI.DoesNotExist:
            return Response(
                {"error": "SocialAPI not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if Signature.objects.filter(user=request.user, social_api=social_api).exists():
            return Response(
                {"error": "Signature already exists for this SocialAPI. Use update endpoint."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        signature = Signature.objects.create(
            user=request.user,
            social_api=social_api,
            signature_content=signature_content,
        )
        
        serializer = SignatureSerializer(signature)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON."},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_signature(request: HttpRequest) -> Response:
    """
    Update an existing email signature.

    Args:
        request (HttpRequest): HTTP request containing:
            signature_content (str): The new signature content.
            signature_id (int): ID of the signature to update.
    
    Returns:
        Response: JSON response with updated signature data or error message.
    """
    try:
        data = json.loads(request.body)
        signature_id = data.get('signature_id')
        signature_content = data.get('signature_content')
        
        try:
            signature = Signature.objects.get(id=signature_id, user=request.user)
        except Signature.DoesNotExist:
            return Response(
                {"error": "Signature not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        signature.signature_content = signature_content
        signature.save()
        
        serializer = SignatureSerializer(signature)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON."},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_signature(request: HttpRequest, signature_id: int) -> Response:
    """
    Delete an existing email signature.
    
    Args:
        request (HttpRequest): HTTP request.
        signature_id (int): ID of the signature to delete.
    
    Returns:
        Response: JSON response indicating success or error.
    """
    try:
        signature = Signature.objects.get(id=signature_id, user=request.user)
        signature.delete()
        return Response(
            {"message": "Signature deleted successfully."},
            status=status.HTTP_200_OK
        )
    except Signature.DoesNotExist:
        return Response(
            {"error": "Signature not found."},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_signatures(request: HttpRequest) -> Response:
    """
    List all email signatures for the authenticated user.
    
    Args:
        request (HttpRequest): HTTP request.
    
    Returns:
        Response: JSON response with a list of signatures.
    """
    signatures = Signature.objects.filter(user=request.user)
    serializer = SignatureSerializer(signatures, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK) 