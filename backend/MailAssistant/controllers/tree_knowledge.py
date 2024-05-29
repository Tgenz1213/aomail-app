"""
Handles AI-driven search to extract data from emails."
"""

import json
import logging
import os
import threading
from MailAssistant.ai_providers import claude
from MailAssistant.models import KeyPoint


######################## LOGGING CONFIGURATION ########################
LOGGER = logging.getLogger(__name__)
ABS_TREE_PATH = "/app/MailAssistant/controllers/trees/"


class Search:
    """
    Class for searching through categorized email data within a knowledge tree.

    Example of a knowledge tree of a user:
    {
        "Studies": {
            "organizations": {
                "ESAIP": {
                    "topics": {
                        "Semester 4": {
                            "keypoints": [
                                "ends around mid-June",
                                "erasmus",
                                "evaluate the dormitory"
                            ],
                            "emails": ["id_email1", "id_email2"]
                        }
                    }
                }
            }
        }
    }
    """

    def __init__(
        self, user_id: int, question: str = None, knowledge_tree: dict = None
    ) -> None:
        self.user_id = user_id
        self.file_path = f"{ABS_TREE_PATH}{user_id}.json"

        self.question = question
        if knowledge_tree:
            self.knowledge_tree = knowledge_tree
            threading.Thread(target=self.save_user_data,
                             args=(knowledge_tree,)).start()
        elif not os.path.exists(self.file_path):
            self.knowledge_tree = {}
        else:
            self.knowledge_tree = self.load_user_data()
        self.categories = self.get_categories()

    '''def get_categories(self) -> dict[str, list[str]]:
        """
        Extracts and returns categories and their associated organizations from the knowledge tree.

        Returns:
            dict[str, list[str]]: A dictionary where the keys are category names and the values are lists of organization names within each category.
        """
        if not self.knowledge_tree:
            return []

        categories = {}
        for category in self.knowledge_tree:
            categories[category] = [
                organization
                for organization in self.knowledge_tree[category]["organizations"]
            ]
        return categories'''

    def get_categories(self) -> dict:
        """
        Extracts and returns categories and their associated organizations from the database for the specified user.

        Returns:
            dict: A dictionary where the keys are category names and the values are lists of organization names within each category.
        """
        categories = {}
        key_points = KeyPoint.objects.filter(email__user_id=self.user_id).values('category', 'organization')
        print(key_points, "IF YOU SEE THIS IT MEANS WE CAN MIGRATE")
        for key_point in key_points:
            category_name = key_point['category']
            organization = key_point['organization']
            if category_name not in categories:
                categories[category_name] = []
            if organization not in categories[category_name]:
                categories[category_name].append(organization)

        return categories

    def get_keypoints(self, selected_categories: dict[str, list[str]]) -> dict:
        """
        Retrieves keypoints for the selected categories and organizations.

        Args:
            selected_categories (dict[str, List[str]]): A dictionary where keys are category names and values are lists of organization names.

        Returns:
            dict[str, dict[str, dict[str, dict[str, List[str]]]]]: A nested dictionary containing keypoints for each category, organization, and topic.
        """
        if not self.knowledge_tree:
            return []

        keypoints = {}
        for category in selected_categories:
            keypoints[category] = {}
            for organization in selected_categories[category]:
                keypoints[category][organization] = {}
                for topic in self.knowledge_tree[category]["organizations"][
                    organization
                ]["topics"]:
                    keypoints[category][organization][topic] = {}
                    keypoints[category][organization][topic]["keypoints"] = [
                        keypoint
                        for keypoint in self.knowledge_tree[category]["organizations"][
                            organization
                        ]["topics"][topic]["keypoints"]
                    ]

        return keypoints

    def get_selected_categories(self) -> dict[str: list[str]]:
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
        response = claude.get_prompt_response(template)
        clear_response = response.content[0].text.strip()
        try:
            result_json = json.loads(clear_response)
        except json.JSONDecodeError:
            LOGGER.critical(
                f"The AI failed to return a proper JSON format for user {self.user_id}"
            )
            raise

        return result_json

    def get_answer(self, keypoints: dict, language: str = "French") -> dict:
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
        response = claude.get_prompt_response(template)
        clear_response = response.content[0].text.strip()
        try:
            result_json = json.loads(clear_response)
        except json.JSONDecodeError:
            LOGGER.critical(
                f"The AI failed to return a proper JSON format for user {self.user_id}"
            )
            raise

        return result_json

    def summarize_conversation(
        self,
        subject: str,
        body: str,
        user_description: str | None,
        email_id: str,
        language: str = "French",
    ) -> dict:
        """
        Summarizes an email conversation in the specified language with keypoints.

        Args:
            subject (str): The subject of the email conversation.
            body (str): The body of the email conversation.
            user_description (Optional[str]): A description provided by the user to enhance keypoints.
            email_id (str): The unique identifier of the email.
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
        }}
        """
        response = claude.get_prompt_response(template)
        clear_response = response.content[0].text.strip()
        try:
            result_json = json.loads(clear_response)
        except json.JSONDecodeError:
            LOGGER.critical(
                f"The AI failed to return a proper JSON format for user {self.user_id}"
            )
            raise

        category = result_json["category"]
        organization = result_json["organization"]
        topic = result_json["topic"]
        keypoints = result_json["keypoints"]

        user_keypoints = [
            keypoint for index in keypoints for keypoint in keypoints[index]
        ]
        self.add_user_data(category, organization, topic,
                           user_keypoints, [email_id])

        return result_json

    def summarize_email(
        self,
        subject: str,
        body: str,
        user_description: str | None,
        email_id: str,
        language: str = "French",
    ) -> dict:
        """
        Summarizes an email conversation in the specified language with keypoints.

        Args:
            subject (str): The subject of the email.
            body (str): The body content of the email.
            user_description (Optional[str]): A description provided by the user to enhance the summary.
            email_id (str): The unique identifier for the email.
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
        response = claude.get_prompt_response(template)
        clear_response = response.content[0].text.strip()
        try:
            result_json = json.loads(clear_response)
        except json.JSONDecodeError:
            LOGGER.critical(
                f"The AI failed to return a proper JSON format for user {self.user_id}"
            )
            raise

        category = result_json["category"]
        organization = result_json["organization"]
        topic = result_json["topic"]
        keypoints = result_json["keypoints"]

        self.add_user_data(category, organization,
                           topic, keypoints, [email_id])

        return result_json

    def save_user_data(self, data: dict) -> None:
        """
        Saves updated user data to a JSON file.

        Args:
            data (dict): The user data to be saved.
        """
        try:
            with open(self.file_path, "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            LOGGER.info(
                f"Data saved to JSON file successfully - user_id: {self.user_id}"
            )
        except (OSError, TypeError) as e:
            LOGGER.error(
                f"Failed to save data to JSON file - user_id: {self.user_id}, error: {e}"
            )

    def load_user_data(self) -> dict:
        """
        Loads user data from a JSON file.

        Returns:
            dict: The user data loaded from the JSON file.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as json_file:
                return json.load(json_file)
        except (OSError, json.JSONDecodeError) as e:
            LOGGER.error(
                f"Failed to load data from JSON file - user_id: {self.user_id}, error: {e}"
            )

    def add_user_data(
        self,
        category: str,
        organization: str,
        topic: str,
        keypoints: list[str],
        emails: list[str],
    ) -> None:
        """
        Adds or updates user data for a specific topic within a structured dictionary.
        Ensures no duplication of keypoints or emails, maintaining case-insensitivity.

        Parameters:
            - category (str): Top-level classification.
            - organization (str): Sub-level classification under category.
            - topic (str): Specific topic under organization for data storage.
            - keypoints (list[str]): List of unique keypoints related to the topic.
            - emails (list[str]): List of unique emails associated with the topic.
        """
        if category not in self.knowledge_tree:
            self.knowledge_tree[category] = {}
            self.knowledge_tree[category]["organizations"] = {}
        if organization not in self.knowledge_tree[category]["organizations"]:
            self.knowledge_tree[category]["organizations"][organization] = {}
            self.knowledge_tree[category]["organizations"][organization]["topics"] = {
            }
        if (
            topic
            not in self.knowledge_tree[category]["organizations"][organization][
                "topics"
            ]
        ):
            self.knowledge_tree[category]["organizations"][organization]["topics"][
                topic
            ] = {}
            self.knowledge_tree[category]["organizations"][organization]["topics"][
                topic
            ]["keypoints"] = keypoints
            self.knowledge_tree[category]["organizations"][organization]["topics"][
                topic
            ]["emails"] = emails
        else:
            prev_keypoints: list = self.knowledge_tree[category]["organizations"][
                organization
            ]["topics"][topic]["keypoints"]

            for keypoint in keypoints:
                if keypoint.lower() not in map(str.lower, prev_keypoints):
                    prev_keypoints.append(keypoint)

            self.knowledge_tree[category]["organizations"][organization]["topics"][
                topic
            ]["keypoints"] = prev_keypoints

            prev_emails: list = self.knowledge_tree[category]["organizations"][
                organization
            ]["topics"][topic]["emails"]

            for email in emails:
                if email.lower() not in prev_emails:
                    prev_emails.append(email)

            self.knowledge_tree[category]["organizations"][organization]["topics"][
                topic
            ]["emails"] = prev_emails

        self.save_user_data(self.knowledge_tree)
