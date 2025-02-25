"""
Handles AI-driven search to extract data from emails and help Ao to answer user questions.
"""

import json
import logging
from aomail.ai_providers.google import client as gemini
from aomail.models import KeyPoint
from aomail.ai_providers.utils import extract_json_from_response


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)


class Search:
    """Class for searching through categorized email data within a knowledge tree."""

    def __init__(self, user_id: int, question: str = None):
        """
        Initializes a Search object.

        Args:
            user_id (int): The ID of the user for whom the search is being conducted.
            question (str, optional): The question or query for the search. Defaults to None.
        """
        self.user_id = user_id
        self.question = question
        self.knowledge_tree = self.get_knowledge_tree()
        self.categories = self.get_categories()

    def get_knowledge_tree(self) -> dict:
        """
        Retrieves the knowledge tree of the user from the database.

        Returns:
            dict: The knowledge tree of the user.
        """
        knowledge_tree: dict = {}
        key_points = KeyPoint.objects.filter(email__user_id=self.user_id)

        for key_point in key_points:
            category_name: str = key_point.category
            organization_name: str = key_point.organization
            topic_name: str = key_point.topic

            category: dict = knowledge_tree.setdefault(
                category_name, {"organizations": {}}
            )
            organizations: dict = category["organizations"]
            organization: dict = organizations.setdefault(
                organization_name, {"topics": {}}
            )
            category["organizations"] = organizations

            topics: dict = organization["topics"]
            topic: dict = topics.setdefault(topic_name, {"keypoints": [], "emails": []})
            organization["topics"] = topics

            keypoints: list = topic["keypoints"]
            keypoints.append(key_point.content)
            topic["keypoints"] = keypoints

            emails: list = topic["emails"]
            emails.append(key_point.email.provider_id)
            topic["emails"] = emails

        return knowledge_tree

    def get_categories(self) -> dict:
        """
        Extracts and returns categories and their associated organizations from the database for the specified user.

        Returns:
            dict: A dictionary where the keys are category names and the values are lists of organization names within each category.
        """
        if not self.knowledge_tree:
            return {}

        categories = {}
        key_points = KeyPoint.objects.filter(email__user_id=self.user_id).values(
            "category", "organization"
        )

        for key_point in key_points:
            category_name = key_point["category"]
            organization = key_point["organization"]
            if category_name not in categories:
                categories[category_name] = []
            list_category_name: list = categories[category_name]
            list_category_name.append(organization)
            categories[category_name] = list_category_name

        return categories

    def get_keypoints(
        self, selected_categories: dict[str, list[str]]
    ) -> dict[str, dict[str, dict[str, dict[str, list[str]]]]]:
        """
        Retrieves keypoints for the selected categories and organizations.

        Args:
            selected_categories (dict): A dictionary where keys are category names and values are lists of organization names.

        Returns:
            dict: A nested dictionary containing keypoints for each category, organization, and topic.
        """
        keypoints = {}

        for category, organizations in selected_categories.items():
            keypoints[category] = {}
            for organization in organizations:
                keypoints[category][organization] = {}
                topics: dict = self.knowledge_tree[category]["organizations"][
                    organization
                ]["topics"]
                for topic, topic_data in topics.items():
                    keypoints[category][organization][topic] = {
                        "keypoints": topic_data["keypoints"]
                    }

        return keypoints

    def can_answer(self) -> bool:
        """
        Checks if Ao can potentially answer a question.

        Returns:
            bool: True if Ao has data to search through and may answer a question,
                False otherwise.
        """
        return self.categories != {}

    def get_selected_categories(self) -> dict[str : list[str]]:
        """
        Returns the highly relevant categories and organizations to answer the user's question.

        Returns:
            dict: A dictionary mapping highly relevant category names to their corresponding organizations.
        """
        template = f"""You are an email assistant that helps a user to answer its question.
        
        Email categories and organizations:
        {self.categories}

        User question:
        {self.question}
        
        Choose categories and organizations that have high probability to help the user to find its answer.
        The chosen categories and organizations must be highly relevant. If you hesitate do not add it.
        Do not add any comments nor explain your thinking process.

        ---
        Answer must always be a Json format matching this template:
        {{
            "category1": [selected organizations],
            ...
            "categoryN": [selected organizations]
        }}
        """
        try:
            response = gemini.get_prompt_response(template)
            result_json = extract_json_from_response(response.text)
            result_json["tokens_input"] = response.usage_metadata.prompt_token_count
            result_json["tokens_output"] = (
                response.usage_metadata.candidates_token_count
            )
        except json.JSONDecodeError:
            LOGGER.critical(
                f"The AI failed to return a proper JSON format for user {self.user_id}"
            )
            raise

        return result_json

    def get_answer(self, keypoints: dict, language: str) -> dict:
        """
        Generates an answer based on the keypoints and checks if further details are needed.

        Args:
            keypoints (dict[str, str]): A dictionary containing key points of the user's data.
            language (str, optional): The language in which the answer should be provided. Defaults to "French".

        Returns:
            dict[str, str]: A dictionary containing the answer and a boolean indicating if the answer is likely to be good.
        """
        template = f"""You are an email assistant that helps a user to answer their question.

        User data:
        {keypoints}

        User question:
        {self.question}
        
        If you estimate that the answer is likely to be good, set the boolean field to 'true'.
        Otherwise, set it to 'false' if you think the user is very likely to look for further details.
        The answer must be concise and straight to the point without giving explanations.

        ---
        The answer must always be in Json format matching this template:
        {{
            "sure": bool,
            "answer": "answer to the user question in {language}"
        }}
        Ensure the JSON is properly formatted and parsable by Python.
        """
        try:
            response = gemini.get_prompt_response(template)
            result_json = extract_json_from_response(response.text)
            result_json["tokens_input"] = response.usage_metadata.prompt_token_count
            result_json["tokens_output"] = (
                response.usage_metadata.candidates_token_count
            )
        except json.JSONDecodeError:
            LOGGER.critical(
                f"The AI failed to return a proper JSON format for user {self.user_id}"
            )
            raise

        return result_json

    def summarize_conversation(
        self, subject: str, body: str, user_description: str | None, language: str
    ) -> dict:
        """
        Summarizes an email conversation in the specified language with keypoints.

        Args:
            subject (str): The subject of the email conversation.
            body (str): The body of the email conversation.
            user_description (Optional[str]): A description provided by the user to enhance keypoints.
            language (str, optional): The language in which to summarize the conversation. Defaults to "French".

        Returns:
            dict: A dictionary containing the category, organization, topic, and keypoints of the email.
        """
        template = f"""As a smart email assistant, 
        For each email in the following conversation, summarize it in {language} as a list of up to three ultra-concise keypoints (up to seven words) that encapsulate the core information. This will aid the user in recalling the past conversation.
        Increment the number of keys to match the number of emails. The number of keys must STRICTLY correspond to the number of emails.
        The sentence must be highly relevant and not deal with details or unnecessary information. If you hesitate, do not add the keypoint.
        If a user description is clearly provided, use it to enhance the keypoints.
        In {language}: Add a 'category' (one word), an 'organization', and a 'topic' that best describes the conversation.
        If you hesitate on any of them, or if it is unclear or not explicitly mentioned, set it to 'Unknown'.
        To assist you in categorizing the conversation, here are the existing categories and organizations: {self.get_categories()}.
        If you can classify the conversation in an existing category/organization: Do it. If you hesitate, create another category/organization in {language}.

        User description:
        {user_description}
        
        Email subject:
        {subject}
        
        Email conversation:
        {body}
        
        ---
        Answer must always be a Json format matching this template:
        {{
            "category": "",
            "organization": "",
            "topic": "",
            "keypoints": {{
                "1": [list of keypoints],
                "2": [list of keypoints],
                "n": [list of keypoints]
            }}
        }}"""
        try:
            response = gemini.get_prompt_response(template)
            result_json = extract_json_from_response(response.text)
            result_json["tokens_input"] = response.usage_metadata.prompt_token_count
            result_json["tokens_output"] = (
                response.usage_metadata.candidates_token_count
            )
        except json.JSONDecodeError:
            LOGGER.critical(
                f"The AI failed to return a proper JSON format for user {self.user_id}"
            )
            raise

        return result_json

    def summarize_email(
        self, subject: str, body: str, user_description: str | None, language: str
    ) -> dict:
        """
        Summarizes an email conversation in the specified language with keypoints.

        Args:
            subject (str): The subject of the email.
            body (str): The body content of the email.
            user_description (Optional[str]): A description provided by the user to enhance the summary.
            language (str, optional): The language in which to summarize the email. Defaults to "French".

        Returns:
            dict: A dictionary containing the category, organization, topic, and keypoints of the email.
        """
        template = f"""As a smart email assistant, 
        Summarize the email body in {language} as a list of up to three ultra-concise keypoints (up to seven words each) that encapsulate the core information. This will aid the user in recalling the content of the email.
        The sentences must be highly relevant and should not include minor details or unnecessary information. If in doubt, do not add the keypoint.
        If a user description is clearly provided, use it to enhance the keypoints.
        In {language}: Add a 'category' (one word), an 'organization', and a 'topic' that best describe the conversation.
        If you hesitate on any of them, or if it is unclear or not explicitly mentioned, set it to 'Unknown'.
        To assist you in categorizing the email, here are the existing categories and organizations: {self.get_categories()}.
        If you can classify the email within an existing category/organization, do so. If uncertain, create another category/organization in {language}.

        User description:
        {user_description}
        
        Email subject:
        {subject}
        
        Email body:
        {body}
        
        ---
        Answer must always be a Json format matching this template:
        {{
            "category": "",
            "organization": "",
            "topic": "",
            "keypoints": [list of keypoints]
        }}
        """
        try:
            response = gemini.get_prompt_response(template)
            result_json = extract_json_from_response(response.text)
            result_json["tokens_input"] = response.usage_metadata.prompt_token_count
            result_json["tokens_output"] = (
                response.usage_metadata.candidates_token_count
            )
        except json.JSONDecodeError:
            LOGGER.critical(
                f"The AI failed to return a proper JSON format for user {self.user_id}"
            )
            raise

        return result_json
