"""
Handles LLM calls, returns results to frontend after processing.

Endpoints:
- ✅ get_new_email_response: Generate a new email.
- ✅ improve_draft: Improve the draft email.
- ✅ search_emails_ai: Search emails using AI interpretation of user query.
- ✅ search_tree_knowledge: Search emails using tree-based AI interpretation of user query.
- ✅ find_user_view_ai: Search for emails in the user's mailbox.
- ✅ new_email_ai: Return an AI-generated email.
- ✅ correct_email_language: Correct spelling and grammar mistakes.
- ✅ check_email_copywriting: Check and provide feedback on the email copywriting.
- ✅ generate_email_response_keywords: Generate response keywords based on the email.
- ✅ generate_email_answer: Generate an answer to an email.
"""

import json
import logging
import threading
from django.core.mail import send_mail
from django.http import HttpRequest
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from aomail.utils.security import subscription
from aomail.ai_providers import claude
from aomail.constants import (
    FREE_PLAN,
    ADMIN_EMAIL_LIST,
    EMAIL_NO_REPLY,
    GOOGLE,
    GOOGLE,
    MAX_RETRIES,
    MICROSOFT,
    MICROSOFT,
)
from aomail.email_providers.google import authentication as auth_google
from aomail.email_providers.microsoft import authentication as auth_microsoft
from aomail.email_providers.microsoft import (
    email_operations as email_operations_microsoft,
)
from aomail.email_providers.google import (
    email_operations as email_operations_google,
)
from aomail.utils.tree_knowledge import Search
from aomail.models import (
    SocialAPI,
    Preference,
    Contact,
    Email,
    Statistics,
)
from aomail.utils.serializers import (
    NewEmailAISerializer,
    EmailCorrectionSerializer,
    EmailCopyWritingSerializer,
    EmailProposalAnswerSerializer,
    EmailGenerateAnswer,
    ContactSerializer,
)
from aomail.utils.ai_memory import (
    EmailReplyConversation,
    GenerateEmailConversation,
)
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.schema import AIMessage, HumanMessage
from aomail.ai_providers.utils import update_tokens_stats


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


def dict_to_chat_history(data: dict) -> ChatMessageHistory:
    """
    Convert a dictionary representation of chat history to a ChatMessageHistory object.

    Args:
        data (dict): A dictionary containing chat history data

    Returns:
        ChatMessageHistory: A ChatMessageHistory object representing the chat history.
    """
    messages = []
    if not data.get("messages", []):
        chat_history = ChatMessageHistory()
        chat_history.add_ai_message("Does this answer satisfy you?")
        return chat_history
    for message_data in data["messages"]:
        speaker = message_data["type"]
        content = message_data["content"]
        if speaker == "ai":
            message = AIMessage(content=content)
        else:
            message = HumanMessage(content=content)
        messages.append(message)
    return ChatMessageHistory(messages=messages)


@api_view(["POST"])
@subscription([FREE_PLAN])
def get_new_email_response(request: HttpRequest) -> Response:
    """
    Generate a new email response based on user input, email importance, subject, body, and chat history.

    Parameters:
        request (HttpRequest): The HTTP request object containing the following parameters in the POST data:
            userInput (str): User input to enhance the email body response.
            importance (str): Importance level of the email.
            subject (str): Subject of the email response.
            body (str): Current body of the previously generated response.
            history (dict): Dictionary representing the chat history.

    Returns:
        Response: A response object containing the new email body response or an error message.
    """
    user = request.user
    parameters: dict = json.loads(request.body)
    user_input: str = parameters["userInput"]
    importance: str = parameters["importance"]
    subject: str = parameters["subject"]
    body: str = parameters["body"]
    history: dict = parameters["history"]

    chat_history = dict_to_chat_history(history)
    email_reply_conv = EmailReplyConversation(
        user, importance, subject, body, chat_history
    )

    for i in range(MAX_RETRIES):
        try:
            result = email_reply_conv.improve_email_response(user_input)
            update_tokens_stats(user, result)
            return Response(
                {
                    "emailBody": result["body"],
                    "history": email_reply_conv.history.dict(),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            LOGGER.critical(
                f"[Attempt n°{i+1}] failed to generate a new body response: {str(e)}"
            )
            # context = {
            #     "attempt_number": i,
            #     "error": str(e),
            #     "user": user,
            #     "title": "Critical Alert: Failed to generate a new body response with AI.",
            # }
            # email_html = render_to_string("ai_failed_conv.html", context)
            # send_mail(
            #     subject="Critical Alert: Failed to generate a new body response",
            #     message="",
            #     recipient_list=ADMIN_EMAIL_LIST,
            #     from_email=EMAIL_NO_REPLY,
            #     html_message=email_html,
            #     fail_silently=False,
            # )

    return Response(
        {
            "error": "The generation of a new email response body failed 3 times in a row. Our team is on his way to fix it."
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@api_view(["POST"])
@subscription([FREE_PLAN])
def improve_draft(request: HttpRequest) -> Response:
    """
    Improves the draft email response based on user input, email length, formality, subject, body, and chat history.

    Parameters:
        request (HttpRequest): The HTTP request object containing the following parameters in the POST data:
            userInput (str): User input to refine the email draft.
            length (str): Length of the email (short, medium, long).
            formality (str): Formality level of the email (casual, formal).
            subject (str): Subject of the email draft.
            body (str): Current body of the email draft.
            history (dict): Dictionary representing the chat history.

    Returns:
        Response: A response object containing the updated subject, email body, and chat history, or an error message if the draft generation fails.
    """
    user = request.user
    parameters: dict = json.loads(request.body)
    user_input: str = parameters["userInput"]
    length: str = parameters["length"]
    formality: str = parameters["formality"]
    subject: str = parameters["subject"]
    body: str = parameters["body"]
    history: dict = parameters["history"]

    chat_history = dict_to_chat_history(history)
    gen_email_conv = GenerateEmailConversation(
        user, length, formality, subject, body, chat_history
    )
    language = Preference.objects.get(user=user).language

    for i in range(MAX_RETRIES):
        try:
            result = gen_email_conv.improve_draft(user_input, language)
            update_tokens_stats(user, result)

            return Response(
                {
                    "subject": result["new_subject"],
                    "emailBody": result["new_body"],
                    "history": gen_email_conv.history.dict(),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            LOGGER.critical(f"[Attempt n°{i+1}] Failed to generate a draft: {str(e)}")
            # context = {
            #     "attempt_number": i,
            #     "error": str(e),
            #     "user": user,
            #     "title": "Critical Alert: Failed to generate a draft.",
            # }
            # email_html = render_to_string("ai_failed_conv.html", context)
            # send_mail(
            #     subject="Critical Alert: Failed to generate a draft",
            #     message="",
            #     recipient_list=ADMIN_EMAIL_LIST,
            #     from_email=EMAIL_NO_REPLY,
            #     html_message=email_html,
            #     fail_silently=False,
            # )

    return Response(
        {
            "error": "The generation of a draft failed 3 times in a row. Our team is on his way to fix it."
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@api_view(["POST"])
@subscription([FREE_PLAN])
def search_emails_ai(request: HttpRequest) -> Response:
    """
    Searches emails using AI interpretation of user query.

    Args:
        request (HttpRequest): HTTP request object containing the search parameters in the request body.
            Expects JSON body with:
                emails (list of str): List of email addresses to search.
                query (str): The user query for the search.

    Returns:
        Response: A JSON response with the search results categorized by email provider and email address,
                      or {"error": "Details of the specific error."} if there's an issue with the search process.
    """
    data: dict = json.loads(request.body)
    user = request.user
    emails = data["emails"]
    query = data["query"]
    language = Preference.objects.get(user=user).language
    result: dict = claude.search_emails(query, language)
    search_params = result["search_params"]
    update_tokens_stats(user, result)

    result = {}

    def append_to_result(provider: str, email: str, data: list):
        if len(data) > 0:
            if provider not in result:
                result[provider] = {}
            result[provider][email] = data

    max_results: int = search_params["max_results"]
    from_addresses: list = search_params["from"]
    to: list = search_params["to"]
    subject: str = search_params["subject"]
    body: str = search_params["body"]
    filenames: list = search_params["filenames"]
    date_from: str = search_params["date_from"]
    keywords: list = search_params["keywords"]
    search_in: dict = search_params["search_in"]

    for email in emails:
        social_api = SocialAPI.objects.get(email=email)
        type_api = social_api.type_api

        if type_api == GOOGLE:
            services = auth_google.authenticate_service(user, email)
            search_result = threading.Thread(
                target=append_to_result,
                args=(
                    GOOGLE,
                    email,
                    email_operations_google.search_emails_ai(
                        services,
                        max_results=max_results,
                        filenames=filenames,
                        from_addresses=from_addresses,
                        to_addresses=to,
                        subject=subject,
                        body=body,
                        keywords=keywords,
                        date_from=date_from,
                        search_in=search_in,
                    ),
                ),
            )
        elif type_api == MICROSOFT:
            access_token = auth_microsoft.refresh_access_token(
                auth_microsoft.get_social_api(user, email)
            )
            search_result = threading.Thread(
                target=append_to_result,
                args=(
                    MICROSOFT,
                    email,
                    email_operations_microsoft.search_emails_ai(
                        access_token,
                        max_results=max_results,
                        filenames=filenames,
                        from_addresses=from_addresses,
                        to_addresses=to,
                        subject=subject,
                        body=body,
                        keywords=keywords,
                        date_from=date_from,
                        search_in=search_in,
                    ),
                ),
            )

        search_result.start()
        search_result.join()

    return Response(result, status=status.HTTP_200_OK)


@api_view(["POST"])
@subscription([FREE_PLAN])
def search_tree_knowledge(request: HttpRequest) -> Response:
    """
    Searches emails using AI interpretation of user query.

    Args:
        request (HttpRequest): HTTP request object containing the search parameters in the request body.
            Expects JSON body with:
                question (str): The user query for the search.

    Returns:
        Response: A JSON response with the search results, including the answer and related emails,
                      or {"error": "Details of the specific error."} if there's an issue with the search process.
    """
    try:
        parameters: dict = json.loads(request.body)
        user = request.user
        user_id = user.id
        question = parameters.get("question")

        if not question:
            return Response(
                {"error": "Question is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        search = Search(user_id, question)
        if not search.can_answer():
            return Response(
                {"message": "Not enough data"},
                status=status.HTTP_200_OK,
            )

        selected_categories = search.get_selected_categories()
        selected_categories = update_tokens_stats(user, selected_categories)

        keypoints = search.get_keypoints(selected_categories)

        if not selected_categories or not keypoints:
            return Response(
                {"message": "Not enough data"},
                status=status.HTTP_200_OK,
            )

        language = Preference.objects.get(user=user).language
        answer = search.get_answer(keypoints, language)
        emails_ids = []

        for category in keypoints:
            for organization in keypoints[category]:
                for topic in keypoints[category][organization]:
                    provider_ids = search.knowledge_tree[category]["organizations"][
                        organization
                    ]["topics"][topic]["emails"]
                    ids = Email.objects.filter(
                        provider_id__in=provider_ids, user=user
                    ).values_list("id", flat=True)
                    emails_ids.extend(ids)

        answer["ids"] = emails_ids
        answer = update_tokens_stats(user, answer)

        return Response({"answer": answer}, status=status.HTTP_200_OK)

    except Exception as e:
        LOGGER.error(
            f"An error occurred while searching email with search tree knowledge feature: {str(e)}"
        )
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@subscription([FREE_PLAN])
def find_user_view_ai(request: HttpRequest) -> Response:
    """
    Searches for emails in the user's mailbox based on the provided search query in both the subject and body.

    Args:
        request (HttpRequest): HTTP request object containing the search parameters in the request body.
            Expects JSON body with:
                query (str): The search query to find email recipients.

    Returns:
        Response: A JSON response with the matched email recipients, including main, CC, and BCC recipients,
                  or {"error": "Details of the specific error."} if there's an issue with the search process.
    """
    parameters: dict = json.loads(request.body)
    search_query = parameters.get("query")

    if not search_query:
        return Response(
            {"error": "Failed to authenticate or no search query provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    recipients_dict = claude.extract_contacts_recipients(search_query)
    update_tokens_stats(request.user, recipients_dict)

    main_list = recipients_dict.get("main_recipients", [])
    cc_list = recipients_dict.get("cc_recipients", [])
    bcc_list = recipients_dict.get("bcc_recipients", [])

    if not main_list:
        return Response(
            {"error": "Invalid input or query not about email recipients"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user_contacts = Contact.objects.filter(user=request.user)
    except Contact.DoesNotExist:
        return Response(
            {"error": "No contacts found"}, status=status.HTTP_404_NOT_FOUND
        )

    contacts_dict = {
        contact["username"]: contact["email"]
        for contact in ContactSerializer(user_contacts, many=True).data
    }

    def find_emails(input_str: str, contacts_dict: dict) -> list:
        input_substrings = input_str.lower().split()
        return [
            email
            for name, email in contacts_dict.items()
            if name and all(sub_str in name.lower() for sub_str in input_substrings)
        ]

    def find_emails_for_recipients(recipient_list: list, contacts_dict: dict) -> list:
        return [
            {
                "username": recipient_name,
                "email": find_emails(recipient_name, contacts_dict),
            }
            for recipient_name in recipient_list
            if find_emails(recipient_name, contacts_dict)
        ]

    main_recipients_with_emails = find_emails_for_recipients(main_list, contacts_dict)
    cc_recipients_with_emails = find_emails_for_recipients(cc_list, contacts_dict)
    bcc_recipients_with_emails = find_emails_for_recipients(bcc_list, contacts_dict)

    return Response(
        {
            "mainRecipients": main_recipients_with_emails,
            "ccRecipients": cc_recipients_with_emails,
            "bccRecipients": bcc_recipients_with_emails,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@subscription([FREE_PLAN])
def new_email_ai(request: HttpRequest) -> Response:
    """
    Return an AI-generated email subject and content based on input data.

    Args:
        request (HttpRequest): The HTTP request object containing input data in the body.

    Returns:
        Response: JSON response with generated email subject and content on success,
                      or error messages on failure.
    """
    data: dict = json.loads(request.body)
    serializer = NewEmailAISerializer(data=data)
    user = request.user

    if serializer.is_valid():
        input_data = serializer.validated_data["inputData"]
        length = serializer.validated_data["length"]
        formality = serializer.validated_data["formality"]
        language = Preference.objects.get(user=user).language

        result = claude.generate_email(input_data, length, formality, language)
        update_tokens_stats(user, result)

        return Response(
            {"subject": result["subject_text"], "mail": result["email_body"]}
        )
    else:
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@subscription([FREE_PLAN])
def correct_email_language(request: HttpRequest) -> Response:
    """
    Corrects spelling and grammar mistakes in the email subject and body based on user's request.

    Args:
        request (HttpRequest): HTTP request object containing data to correct the email.
            Expects JSON body with:
                email_subject (str): The subject of the email to be corrected.
                email_body (str): The body of the email to be corrected.

    Returns:
        Response: JSON response containing corrected email subject, body, and the number of corrections made.
                      If there are validation errors in the serializer, returns a JSON response with the errors
                      and status HTTP 400 Bad Request.
    """
    data: dict = json.loads(request.body)
    serializer = EmailCorrectionSerializer(data=data)

    if serializer.is_valid():
        subject = serializer.validated_data["subject"]
        body = serializer.validated_data["body"]

        result = claude.correct_mail_language_mistakes(body, subject)
        result = update_tokens_stats(request.user, result)

        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@subscription([FREE_PLAN])
def check_email_copywriting(request: HttpRequest) -> Response:
    """
    Checks and provides feedback on the email copywriting based on the user's request.

    Args:
        request (HttpRequest): HTTP request object containing data to check the email copywriting.
            Expects JSON body with:
                email_subject (str): The subject of the email to be checked.
                email_body (str): The body of the email to be checked.

    Returns:
        Response: JSON response containing feedback on the email copywriting.
                      If there are validation errors in the serializer, returns a JSON response with the errors
                      and status HTTP 400 Bad Request.
    """
    data: dict = json.loads(request.body)
    serializer = EmailCopyWritingSerializer(data=data)

    if serializer.is_valid():
        subject = serializer.validated_data["subject"]
        body = serializer.validated_data["body"]

        result = claude.improve_email_copywriting(body, subject)
        update_tokens_stats(request.user, result)

        return Response(
            {"feedbackCopywriting": result["feedback_ai"]}, status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@subscription([FREE_PLAN])
def generate_email_response_keywords(request: HttpRequest) -> Response:
    """
    Generates response keywords based on the provided email subject and content.

    Args:
        request (HttpRequest): HTTP request object containing data to generate response keywords.
            Expects JSON body with:
                email_subject (str): The subject of the email for which response keywords are to be generated.
                email_content (str): The content/body of the email for which response keywords are to be generated.

    Returns:
        Response: JSON response containing response keywords generated from the email subject and content.
                      If there are validation errors in the serializer, returns a JSON response with the errors
                      and status HTTP 400 Bad Request.
    """
    data: dict = json.loads(request.body)
    serializer = EmailProposalAnswerSerializer(data=data)

    if serializer.is_valid():
        subject = serializer.validated_data["subject"]
        body = serializer.validated_data["body"]

        result = claude.generate_response_keywords(subject, body)
        update_tokens_stats(request.user, result)

        return Response(
            {"responseKeywords": result["keywords_list"]},
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@subscription([FREE_PLAN])
def generate_email_answer(request: HttpRequest) -> Response:
    """
    Generates an automated response to an email based on its subject, content, and user instructions.

    Args:
        request (HttpRequest): HTTP request object containing data to generate an email response.
            Expects JSON body with:
                email_subject (str): The subject of the email for which the response is generated.
                email_content (str): The content/body of the email for which the response is generated.
                response_type (str): User instruction indicating how the response should be generated.

    Returns:
        Response: JSON response containing the generated email response.
                      If there are validation errors in the serializer, returns a JSON response with the errors
                      and status HTTP 400 Bad Request.
    """
    data: dict = json.loads(request.body)
    serializer = EmailGenerateAnswer(data=data)

    if serializer.is_valid():
        subject = serializer.validated_data["subject"]
        body = serializer.validated_data["body"]
        user_instruction = serializer.validated_data["keyword"]

        result = claude.generate_email_response(
            subject, body, user_instruction
        )
        update_tokens_stats(request.user, result)

        return Response({"emailAnswer": result["body"]}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
