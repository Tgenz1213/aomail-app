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


TODO:
- (ANTI scraping/reverse engineering): Add a system that counts the number of 400 erros per user and send warning + ban

REMAINING functions to opti and clean:
- def find_user_view_ai(request: HttpRequest) -> Response:
    - Log important messages/errors with user id, clear error name when possible
    - Clean the code by adding data types.
    - Remove unrelevant comments
    - Use ONLY: status=status.HTTP_200_OK NOT 200
    - Ensure Pylance can recognize variable types and methods.
        EXAMPLE:
        def view_function(request: HttpRequest):
            user = request.user
            # USE THIS instead of 'data'
            parameters: dict = json.loads(request.body)
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
from MailAssistant.utils.security import subscription
from MailAssistant.ai_providers import claude
from MailAssistant.constants import (
    FREE_PLAN,
    ADMIN_EMAIL_LIST,
    EMAIL_NO_REPLY,
    GOOGLE_PROVIDER,
    MAX_RETRIES,
    MICROSOFT_PROVIDER,
)
from MailAssistant.utils.tree_knowledge import Search
from MailAssistant.email_providers import google_api, microsoft_api
from MailAssistant.models import (
    SocialAPI,
    Preference,
    Contact,
)
from MailAssistant.utils.serializers import (
    NewEmailAISerializer,
    EmailCorrectionSerializer,
    EmailCopyWritingSerializer,
    EmailProposalAnswerSerializer,
    EmailGenerateAnswer,
    ContactSerializer,
)
from MailAssistant.utils.ai_memory import (
    EmailReplyConversation,
    GenerateEmailConversation,
)
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.schema import AIMessage, HumanMessage


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
            - userInput (str): User input to enhance the email body response.
            - importance (str): Importance level of the email.
            - subject (str): Subject of the email response.
            - body (str): Current body of the previously generated response.
            - history (dict): Dictionary representing the chat history.

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
            new_body_response = email_reply_conv.improve_email_response(user_input)
            return Response(
                {
                    "email_body": new_body_response,
                    "history": email_reply_conv.history.dict(),
                },
                status=200,
            )
        except Exception as e:
            LOGGER.critical(
                f"[Attempt n°{i+1}] failed to generate a new body response: {str(e)}"
            )
            context = {
                "attempt_number": i,
                "error": str(e),
                "user": user,
                "title": "Critical Alert: Failed to generate a new body response with AI.",
            }
            email_html = render_to_string("ai_failed_conv.html", context)
            send_mail(
                subject="Critical Alert: Failed to generate a new body response",
                message="",
                recipient_list=ADMIN_EMAIL_LIST,
                from_email=EMAIL_NO_REPLY,
                html_message=email_html,
                fail_silently=False,
            )

    return Response(
        {
            "error": "The generation of a new email response body failed 3 times in a row. Our team is on his way to fix it."
        },
        status=500,
    )


@api_view(["POST"])
@subscription([FREE_PLAN])
def improve_draft(request: HttpRequest) -> Response:
    """
    Improves the draft email response based on user input, email length, formality, subject, body, and chat history.

    Parameters:
        request (HttpRequest): The HTTP request object containing the following parameters in the POST data:
            - userInput (str): User input to refine the email draft.
            - length (str): Length of the email (short, medium, long).
            - formality (str): Formality level of the email (casual, formal).
            - subject (str): Subject of the email draft.
            - body (str): Current body of the email draft.
            - history (dict): Dictionary representing the chat history.

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
            new_subject, new_body = gen_email_conv.improve_draft(user_input, language)
            return Response(
                {
                    "subject": new_subject,
                    "email_body": new_body,
                    "history": gen_email_conv.history.dict(),
                },
                status=200,
            )
        except Exception as e:
            LOGGER.critical(f"[Attempt n°{i+1}] Failed to generate a draft: {str(e)}")
            context = {
                "attempt_number": i,
                "error": str(e),
                "user": user,
                "title": "Critical Alert: Failed to generate a draft.",
            }
            email_html = render_to_string("ai_failed_conv.html", context)
            send_mail(
                subject="Critical Alert: Failed to generate a draft",
                message="",
                recipient_list=ADMIN_EMAIL_LIST,
                from_email=EMAIL_NO_REPLY,
                html_message=email_html,
                fail_silently=False,
            )

    return Response(
        {
            "error": "The generation of a draft failed 3 times in a row. Our team is on his way to fix it."
        },
        status=500,
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
    search_params: dict = claude.search_emails(query, language)
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

        if type_api == "google":
            services = google_api.authenticate_service(user, email)
            search_result = threading.Thread(
                target=append_to_result,
                args=(
                    GOOGLE_PROVIDER,
                    email,
                    google_api.search_emails_ai(
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
        elif type_api == "microsoft":
            access_token = microsoft_api.refresh_access_token(
                microsoft_api.get_social_api(user, email)
            )
            search_result = threading.Thread(
                target=append_to_result,
                args=(
                    MICROSOFT_PROVIDER,
                    email,
                    microsoft_api.search_emails_ai(
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
        keypoints = search.get_keypoints(selected_categories)

        if not selected_categories or not keypoints:
            return Response(
                {"message": "Not enough data"},
                status=status.HTTP_200_OK,
            )

        language = Preference.objects.get(user=user).language
        answer = search.get_answer(keypoints, language)
        emails = []

        for category in keypoints:
            for organization in keypoints[category]:
                for topic in keypoints[category][organization]:
                    emails.extend(
                        search.knowledge_tree[category]["organizations"][organization][
                            "topics"
                        ][topic]["emails"]
                    )

        answer["emails"] = emails

        return Response({"answer": answer}, status=status.HTTP_200_OK)

    except Exception as e:
        LOGGER.error(
            f"An error occurred while searching email with search tree knowledge feature: {str(e)}"
        )
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@subscription([FREE_PLAN])
def find_user_view_ai(request: HttpRequest) -> Response:
    """Searches for emails in the user's mailbox based on the provided search query in both the subject and body."""
    search_query = request.GET.get("query")

    if search_query:
        main_list, cc_list, bcc_list = claude.extract_contacts_recipients(search_query)

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

        contacts_serializer = ContactSerializer(user_contacts, many=True)

        # TODO: check for performance (should be fast)
        def transform_list_of_dicts(list_of_dicts):
            new_dict = {}

            for item in list_of_dicts:
                new_dict[item["username"]] = item["email"]

            return new_dict

        contacts_dict = transform_list_of_dicts(contacts_serializer.data)

        def find_emails(input_str, contacts_dict):
            # Split input_str into substrings if it contains spaces
            input_substrings = input_str.split() if " " in input_str else [input_str]

            # Convert input substrings to lowercase for case-insensitive matching
            input_substrings_lower = [sub_str.lower() for sub_str in input_substrings]

            # List comprehension to find matching emails
            matching_emails = [
                email
                for name, email in contacts_dict.items()
                if all(sub_str in name.lower() for sub_str in input_substrings_lower)
            ]

            # Return the list of matching emails
            return matching_emails

        def find_emails_for_recipients(recipient_list, contacts_dict) -> dict:
            """Find matching emails for a list of recipients."""
            recipients_with_emails = []

            # Iterate through recipient_list to find matches
            for recipient_name in recipient_list:
                matching_emails = find_emails(recipient_name, contacts_dict)

                # Append the result as a dictionary
                if len(matching_emails) > 0:
                    recipients_with_emails.append(
                        {"username": recipient_name, "email": matching_emails}
                    )

            return recipients_with_emails

        # Find matching emails for each list of recipients
        main_recipients_with_emails = find_emails_for_recipients(
            main_list, contacts_dict
        )
        cc_recipients_with_emails = find_emails_for_recipients(cc_list, contacts_dict)
        bcc_recipients_with_emails = find_emails_for_recipients(bcc_list, contacts_dict)

        return Response(
            {
                "main_recipients": main_recipients_with_emails,
                "cc_recipients": cc_recipients_with_emails,
                "bcc_recipients": bcc_recipients_with_emails,
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"error": "Failed to authenticate or no search query provided"},
            status=status.HTTP_400_BAD_REQUEST,
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
        input_data = serializer.validated_data["input_data"]
        length = serializer.validated_data["length"]
        formality = serializer.validated_data["formality"]
        language = Preference.objects.get(user=user).language

        subject_text, mail_text = claude.generate_email(
            input_data, length, formality, language
        )

        return Response({"subject": subject_text, "mail": mail_text})
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
        email_subject = serializer.validated_data["email_subject"]
        email_body = serializer.validated_data["email_body"]

        corrected_subject, corrected_body, num_corrections = (
            claude.correct_mail_language_mistakes(email_body, email_subject)
        )
        return Response(
            {
                "corrected_subject": corrected_subject,
                "corrected_body": corrected_body,
                "num_corrections": num_corrections,
            }
        )
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
        email_subject = serializer.validated_data["email_subject"]
        email_body = serializer.validated_data["email_body"]

        feedback_copywriting = claude.improve_email_copywriting(
            email_body, email_subject
        )
        return Response({"feedback_copywriting": feedback_copywriting})
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
        email_subject = serializer.validated_data["email_subject"]
        email_content = serializer.validated_data["email_content"]

        response_keywords = claude.generate_response_keywords(
            email_subject, email_content
        )
        return Response({"response_keywords": response_keywords})
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
        email_subject = serializer.validated_data["email_subject"]
        email_content = serializer.validated_data["email_content"]
        user_instruction = serializer.validated_data["response_type"]

        email_answer = claude.generate_email_response(
            email_subject, email_content, user_instruction
        )

        return Response({"email_answer": email_answer})
    else:
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
