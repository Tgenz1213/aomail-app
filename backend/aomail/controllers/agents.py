import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from aomail.utils.serializers import AgentSerializer
from aomail.models import Agent
from django.http import HttpRequest

LOGGER = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_agent(request: HttpRequest) -> Response:
    """
    Create a new agent for the authenticated user.

    Args:
        request (HttpRequest): HTTP request containing agent data.

    Returns:
        Response: JSON response with agent data or error messages.
    """
    data = request.data.copy()
    data['user'] = request.user.id
    serializer = AgentSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_agent(request: HttpRequest, agent_id: int) -> Response:
    """
    Update an existing agent for the authenticated user.

    Args:
        request (HttpRequest): HTTP request containing updated agent data.
        agent_id (int): ID of the agent to update.

    Returns:
        Response: JSON response with updated agent data or error messages.
    """
    try:
        agent = Agent.objects.get(id=agent_id, user=request.user)
    except Agent.DoesNotExist:
        return Response(
            {"error": "Agent not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = AgentSerializer(agent, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_agents(request: HttpRequest) -> Response:
    """
    List all agents for the authenticated user.

    Args:
        request (HttpRequest): HTTP request.

    Returns:
        Response: JSON response with a list of agents.
    """
    agents = Agent.objects.filter(user=request.user)
    serializer = AgentSerializer(agents, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_agent(request: HttpRequest, agent_id: int) -> Response:
    """
    Delete an existing agent for the authenticated user.

    Args:
        request (HttpRequest): HTTP request.
        agent_id (int): ID of the agent to delete.

    Returns:
        Response: JSON response indicating success or error message.
    """
    try:
        agent = Agent.objects.get(id=agent_id, user=request.user)
        agent.delete()
        return Response(
            {"message": "Agent deleted successfully."},
            status=status.HTTP_200_OK
        )
    except Agent.DoesNotExist:
        return Response(
            {"error": "Agent not found."},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_last_used_agent(request: HttpRequest) -> Response:
    """
    Check if any agent for the authenticated user has 'last_used' set to True.

    Returns:
        - If no agent has 'last_used=True':
            {"exists": False}
        - If an agent has 'last_used=True':
            {"exists": True, "agent_id": <agent_id>}
    """
    user = request.user
    agent = Agent.objects.filter(user=user, last_used=True).first()

    if agent:
        return Response(
            {"exists": True, "agent_id": agent.id},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"exists": False},
            status=status.HTTP_200_OK
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_agent(request: HttpRequest, agent_id: int) -> Response:
    """
    Retrieve the details of a specific agent by its ID.

    Args:
        request (HttpRequest): HTTP request object.
        agent_id (int): ID of the agent to retrieve.

    Returns:
        Response: JSON response with agent details or an error message.
    """
    try:
        agent = Agent.objects.get(id=agent_id, user=request.user)
    except Agent.DoesNotExist:
        return Response(
            {"error": "Agent not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = AgentSerializer(agent)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_agents_info(request: HttpRequest) -> Response:
    """
    Retrieve comprehensive information of all agents for the authenticated user.

    Args:
        request (HttpRequest): HTTP request object.

    Returns:
        Response: JSON response with detailed agent information or an error message.
    """
    try:
        agents = Agent.objects.filter(user=request.user)
        if not agents.exists():
            return Response(
                {"message": "No agents found for the user."},
                status=status.HTTP_200_OK
            )
        
        serializer = AgentSerializer(agents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        LOGGER.error(f"Error fetching agents for user {request.user.id}: {str(e)}")
        return Response(
            {"error": "An error occurred while fetching agents."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 