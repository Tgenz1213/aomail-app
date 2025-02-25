"""
Default prompts for the LLM providers
"""

from aomail.constants import (
    ANSWER_REQUIRED,
    HIGHLY_RELEVANT,
    MIGHT_REQUIRE_ANSWER,
    NO_ANSWER_REQUIRED,
    NOT_RELEVANT,
    POSSIBLY_RELEVANT,
)


EXTRACT_CONTACTS_RECIPIENTS_PROMPT = """As an intelligent email assistant, analyze the input to categorize email recipients into main, cc, and bcc categories based on the presence of keywords and context that suggest copying or blind copying. Here's the input: '{query}'.

Guidelines for classification:
- Main recipients are those directly mentioned or implied to be the primary audience, without specific indicators for copying.
- CC (carbon copy) recipients are identified through the context or subtle cues that imply they should be informed of the communication. Look for any keywords or phrases, even if indirectly stated, that traditionally associate with copying someone on an email.
- BCC (blind carbon copy) recipients are identified similarly by context or cues suggesting a need for discretion or privacy in copying, without directly mentioning them in the conversation.

If the input does not clearly differentiate between main, cc, and bcc recipients, use intuitive rules and a careful analysis of the text structure and any potential copying-related keywords or implications:
1. Names appearing first or separated by phrases indicating inclusion (e.g., 'and', 'et') without clear copying context are considered as main recipients.
2. Utilize any linguistic or structural clues to infer if a recipient is intended for CC or BCC, focusing on the broader context rather than explicit markers

Return ONLY the results in JSON format with three keys:
main_recipients: [Python list],
cc_recipients: [Python list],
bcc_recipients: [Python list]    
"""

GENERATE_RESPONSE_KEYWORDS_PROMPT = """As an email assistant, analyze the email with the subject: '{input_subject}' and body: '{input_email}'.

IDENTIFY exactly 5 distinct ways to respond. For each scenario:
**Provide "keywords":** a list of short phrases (fragments) describing the approach. These should **not form complete sentences** but should contain multiple words to effectively convey the strategy. Ensure that the keywords are **in the same language** as the original email. For example:
- "can't attend 5pm, need new schedule, request confirmation"
- "appreciate feedback, will implement changes, thank you"

As an answer ONLY give a Python List format: ["...", "..."]. Do not use any other characters or explanations; RETURN only the list.
"""

SIGNATURE_INSTRUCTION_WITH_CONTENT = "\n3. DO NOT modify, remove or create a new signature. Keep this EXACT SAME signature at the end of the email:\n{signature}"
SIGNATURE_INSTRUCTION_WITHOUT_CONTENT = "Add a standard greeting and sign-off without a signature (unless explicitly mentioned).\nSignature: <br>"


GENERATE_EMAIL_PROMPT = """As an email assistant, following these agent guidelines: {agent_settings}, write a {length} and {formality} email in {language}.
Improve the QUANTITY and QUALITY in {language} according to the user guideline: '{input_data}'.
It must strictly contain only the information that is present in the input.
{signature_instruction}

---
Answer must ONLY be in JSON format with two keys: subject (STRING) and body in HTML format without spaces and unusual line breaks.
"""


CORRECT_MAIL_LANGUAGE_MISTAKES_PROMPT = """As an email assistant, check the following text for any grammatical or spelling errors and correct them, Do not change any words unless they are misspelled or grammatically incorrect.
    
Answer must be a Json format with two keys: subject (STRING) AND body (HTML)

subject: {subject},
body: {body}
"""


IMPROVE_EMAIL_COPYWRITING_PROMPT = """Evaluate the quality of copywriting in both the subject and body of this email. Provide feedback and improvement suggestions.

Email Subject:
"{email_subject}"

Email Body:
"{email_body}"

---

<strong>Subject Feedback</strong>:
[Your feedback on the subject]

<strong>Suggestions for the Subject</strong>:
[Your suggestions for the subject]

<strong>Email Body Feedback</strong>:
[Your feedback on the email body]

<strong>Suggestions for the Email Body</strong>:
[Your suggestions for the email body]
"""


GENERATE_EMAIL_RESPONSE_PROMPT = """As a smart email assistant, following these agent guidelines: {agent_settings}, and based on the email with the subject: '{input_subject}' and body: '{input_body}'.
Craft a response strictly in the language used in the email following the user instruction: '{user_instruction}'.
0. Pay attention if the email appears to be a conversation. You MUST only reply to the last email and do NOT summarize the conversation at all.
1. Ensure the response is structured as an HTML email. Make sure to create a brief response that is straight to the point unless a contradictory guideline is explicitly mentioned by the user.
2. Respect the tone employed in the subject and body, as well as the relationship and respectful markers between recipients.
{signature_instruction}

---
Answer must ONLY be in JSON format with one key: body in HTML.
"""

RESPONSE_LIST = {
    ANSWER_REQUIRED: "Message requires an answer.",
    MIGHT_REQUIRE_ANSWER: "Message might require an answer.",
    NO_ANSWER_REQUIRED: "No answer is required.",
}
RELEVANCE_LIST = {
    HIGHLY_RELEVANT: "Message is highly relevant to the recipient.",
    POSSIBLY_RELEVANT: "Message might be relevant to the recipient.",
    NOT_RELEVANT: "Message is not relevant to the recipient.",
}

CATEGORIZE_AND_SUMMARIZE_EMAIL_PROMPT = """You are a smart email assistant acting as if you were a secretary, summarizing an email for the recipient orally.
    
Given the following email:

Sender:
{sender}

Subject:
{subject}

Text:
{decoded_data}

User description:
{user_description}

Using the provided categories:

Topic Categories:
{category_dict}

Response Categories:
{response_list}

Relevance Categories:
{relevance_list}

Follow those rules:
"important" emails: {important_guidelines}
"informative" emails: {informative_guidelines}
"useless" emails: {useless_guidelines}

Complete the following tasks in same language used in the email:
- Categorize the email according to the user description (if provided) and given categories.
- Summarize the email without adding any greetings.
- If the email explicitly mentions the name of the user (provided with user description), then use 'You' instead of the name of the user.
- Provide a short sentence (up to 10 words) summarizing the core content of the email.
- Define the importance level of the email with one keyword: "important", "informative" or "useless".
- If the email appears to be a response or a conversation, summarize only the last email and IGNORE the previous ones.
- The summary should objectively reflect the most important information of the email without making subjective judgments.    

---
Return this JSON object completed with the requested information:
{{
    "topic": Selected Category,
    "response": Response,
    "relevance": Relevance,
    "importance": Importance of the email,
    "flags": {{
        "spam": bool,
        "scam": bool,
        "newsletter": bool,
        "notification": bool,
        "meeting": bool
    }},
    "summary": {{
        "one_line": One sentence summary,
        "short": Short summary of the email
    }}
}}"""


SEARCH_EMAILS_PROMPT = """As a smart email assistant and based on the user query: '{query}'. Knowing today's date: {today}
1. Analyse and create a filter to search emails content with the Gmail API and Graph API.
2. If nothing special is specified, 'from', 'to', 'subject', 'body' MUST have the same value as the most relevant keyword. By default, search in 'read', 'unread' emails
3. Regarding keywords, provide ONLY individual words. Sentences are not allowed unless explicitly mentioned. If you're unsure, list every relevant word separately.
4. If and only if a date is explicitely provided by the user; add it to the output using this format: MM/DD/YYYY. Otherwise leave it as an empty string if you hesitate.

---
Answer must ONLY be a Json format matching this template in {language} WITHOUT giving any explanation:
{{
    max_results: int - default 100,
    from: [],
    to: [],
    subject: "",
    body: "",
    filenames: [filenames OR extensions following (a-z0-9)],
    date_from: "",
    keywords: [],
    search_in: {{
        "read": boolean,
        "unread": boolean,
        "drafts": boolean,
        "sent_emails": boolean,
        "deleted_emails": boolean,
        "spams": boolean
    }}
}}"""


REVIEW_USER_DESCRIPTION_PROMPT = """You are an assistant helping a user to create categories to automatically classify emails. The user has provided the following description for a category: {user_description}
    
The category should be clear and precise with enough details to classify incoming emails. The description should be in the third person and provide a clear understanding of the category.
Here are some good examples:
            'Augustin ROLET is a student at ESAIP (Engineering School specialized in Computer Science),
            Augustin ROLET is an Integration Development Intern at CDS (Cognitive Design Systems is a company that creates software for 3D printing).'

Tasks:
- Review the description provided by the user.
- Provide feedback on the quality of the description.
- Indicate whether the description is valid. As long as the description is clear and provides enough details, it should be considered valid.
- Do not be strict about the details: as long as the description is a short sentence and contains a few relevant keywords, it should be considered valid.

The response MUST be a JSON formatted as follows:
{{
    "valid": boolean,
    "feedback": "short sentence describing the quality of the description"
}}
"""


CHAT_HISTORY_TEXT = "- Take into account the chat history, but prioritize the latest guidelines from the user:\n  {chat_history}"

GENERATE_CATEGORIES_SCRATCH_PROMPT = """You are an assistant helping a user to create categories to automatically classify emails. The user has provided the following list of topics: {user_topics}
    
Tasks:
- The topics will be used to classify incoming emails.
- If you see an obvious mistake in the name or the desctiption you can correct it.
- The description should be clear and precise with enough details to classify incoming emails.
- Avoid creating categories that are too similar to each other the categories MUST have no links between them or very little if not possible.
- Stay as minimal as possible with the numers of created categories, DO NOT TRY to add additional categories that might fit the user.
- Provide feedback on the quality of the name and description for each category. It MUST be short and will only be visible by the user if he dislikes the name or description.
{chat_history_text}

The response MUST be a JSON formatted as follows:
{{
    "categories": [
        {{
            "name": "Category 1",
            "description": "Description of the category",
            "feedback": "short sentence describing the quality of the name and description"
        }},
        {{
            "name": "Category 2",
            "description": "Description of the category",
            "feedback": "short sentence describing the quality of the name and description"
        }}
    ]
}}
"""


GENERATE_PRIORITIZATION_SCRATCH_PROMPT = """You are an intelligent email assistant tasked with helping a user create detailed and effective email prioritization guidelines.
    
The user has provided the following input: {user_input}
This input will be used to guide an AI system in automatically categorizing and prioritizing emails based on the user's preferences.

Your tasks are:
1. Review the user's guidance for accuracy, completeness, and clarity.
2. Correct any inconsistencies or errors in descriptions.
3. Improve the descriptions to ensure they are:
    - Clear and concise
    - Specific and actionable
    - Aligned with the user's input
4. Adapt the descriptions while taking inspiration from the example provided below, ensuring the response remains user-specific.

Example of effective prioritization guidance:
{{
    "important": "Emails requiring immediate attention, such as meetings and deadlines.",
    "informative": "General updates or communications that don't need urgent action.",
    "useless": "Spam, marketing emails, and newsletters that are not useful."
}}

Your response MUST strictly follow this JSON format:
{{
    "important": "Description of what important emails are for the user.",
    "informative": "Description of what informative emails are for the user.",
    "useless": "Description of what useless emails are for the user."
}}
"""


DETERMINE_ACTION_SCENARIO_PROMPT = """
Determine the appropriate scenario based on the following user request:
"{user_request}"

Scenarios:
1. The user wants the AI to fetch a sender's email using name or directly email or part of the email. Or the user ask to send an email to someone without specifying any email instructions or draft.
2. The user wants to ask the AI to generate an email and has specified the sender or senders.
3. The user wants to ask the AI to generate an email and has not specified any senders.

Please respond with the scenario number (1, 2, or 3) that best fits the user request.
"""
