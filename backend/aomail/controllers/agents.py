import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from aomail.utils.serializers import AgentSerializer
from aomail.models import Agent
from django.http import HttpRequest
from django.contrib.auth.models import User

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
    serializer = AgentSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['PUT'])
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
    LOGGER.info(f"Received update request for agent_id: {agent_id} by user: {request.user.username}")
    
    try:
        agent = Agent.objects.get(id=agent_id, user=request.user)
        LOGGER.debug(f"Agent before update: {agent}")
    except Agent.DoesNotExist:
        LOGGER.error(f"Agent with id {agent_id} not found for user {request.user.username}")
        return Response(
            {"error": "Agent not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = AgentSerializer(agent, data=request.data, partial=True)
    LOGGER.debug(f"Serialized data: {serializer.initial_data}")

    if serializer.is_valid():
        updated_agent = serializer.save()
        LOGGER.info(f"Agent updated successfully: {updated_agent}")
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        LOGGER.error(f"Serializer errors: {serializer.errors}")
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
    


def create_default_agents(user: User, language: str) -> dict:
    """
    Creates default agents for the user based on the preferred language (English or French).

    Args:
        user (User): The user for whom agents will be created.
        language (str): The preferred language ('en' or 'fr').

    Returns:
        dict: A dictionary indicating the success or failure of the operation.
              - On success: {'message': 'Default agents created successfully'}
              - On failure: {'error': <error_message>}
    """
    try:
        default_agents_en = [
            {
                "agent_name": "Bob : to talk to friends",
                "agent_ai_model": "gpt-3.5-turbo",
                "ai_template": "Quick and informal as if talking to a friend.",
                "email_example": "",
                "length": "short",
                "formality": "informal",
                "language": language,
                "picture": "/app/media/agent_icon/default_aomail_agent_bob.png",
                "icon_name": "default_aomail_agent_bob.png",
            },
            {
                "agent_name": "AO : to talk to colleagues",
                "agent_ai_model": "gpt-3.5-turbo",
                "ai_template": "Fast and formal as if talking to colleagues.",
                "email_example": "",
                "length": "short",
                "formality": "formal",
                "language": language,
                "picture": "/app/media/agent_icon/aomail_agent_ao.png",
                "icon_name": "aomail_agent_ao.png",
            },
            {
                "agent_name": "Jhon : to talk to supervisors",
                "agent_ai_model": "gpt-3.5-turbo",
                "ai_template": "Medium-paced and highly formal as if talking to supervisors.",
                "email_example": "",
                "length": "medium",
                "formality": "very formal",
                "language": language,
                "picture": "/app/media/agent_icon/default_aomail_agent_jhon.png",
                "icon_name": "default_aomail_agent_jhon.png",
            },
        ]

        default_agents_fr = [
            {
                "agent_name": "Bob",
                "agent_ai_model": "gpt-3.5-turbo",
                "ai_template": "Rapide et informel comme si vous parliez à un ami.",
                "email_example": "",
                "length": "court",
                "formality": "informel",
                "language": language,
                "picture": "/app/media/agent_icon/default_aomail_agent_bob.png",
                "icon_name": "default_aomail_agent_bob.png",
            },
            {
                "agent_name": "AO",
                "agent_ai_model": "gpt-3.5-turbo",
                "ai_template": "Rapide et formel comme si vous parliez à des collègues.",
                "email_example": "",
                "length": "court",
                "formality": "formel",
                "language": language,
                "picture": "/app/media/agent_icon/aomail_agent_ao.png",
                "icon_name": "aomail_agent_ao.png",
            },
            {
                "agent_name": "Jhon",
                "agent_ai_model": "gpt-3.5-turbo",
                "ai_template": "Modéré et très formel comme si vous parliez à des décideurs.",
                "email_example": "",
                "length": "moyen",
                "formality": "formel",
                "language": language,
                "picture": "/app/media/agent_icon/default_aomail_agent_jhon.png",
                "icon_name": "default_aomail_agent_jhon.png",
            },
        ]

        if language.lower() == "fr" or language.lower() == "french":
            agents_to_create = default_agents_fr
            LOGGER.info(f"Creating default French agents for user {user.username}")
        else:
            agents_to_create = default_agents_en
            LOGGER.info(f"Creating default English agents for user {user.username}")

        for agent_data in agents_to_create:
            Agent.objects.create(
                agent_name=agent_data["agent_name"],
                agent_ai_model=agent_data["agent_ai_model"],
                ai_template=agent_data["ai_template"],
                email_example=agent_data["email_example"],
                user=user,
                length=agent_data["length"],
                formality=agent_data["formality"],
                language=agent_data["language"],
                last_used=False,
                picture=agent_data["picture"],
                icon_name=agent_data["icon_name"],
            )
        LOGGER.info(f"Default agents created for user {user.username}")
        return {"message": "Default agents created successfully"}
    except Exception as e:
        LOGGER.error(
            f"Failed to create default agents for user {user.username}: {str(e)}"
        )
        return {"error": "An error occurred during agent creation."}