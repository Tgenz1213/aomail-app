import json
from aomail.ai_providers.google.client import (
    categorize_and_summarize_email,
    correct_mail_language_mistakes,
    determine_action_scenario,
    extract_contacts_recipients,
    generate_categories_scratch,
    generate_email,
    generate_email_response,
    generate_prioritization_scratch,
    generate_response_keywords,
    get_answer,
    improve_draft,
    improve_email_copywriting,
    improve_email_response,
    review_user_description,
    search_emails,
    select_categories,
    summarize_conversation,
    summarize_email,
)
from aomail.ai_providers.prompts import (
    CATEGORIZE_AND_SUMMARIZE_EMAIL_PROMPT,
    GENERATE_EMAIL_PROMPT,
    GENERATE_EMAIL_RESPONSE_PROMPT,
    GENERATE_RESPONSE_KEYWORDS_PROMPT,
    IMPROVE_EMAIL_DRAFT_PROMPT,
    IMPROVE_EMAIL_RESPONSE_PROMPT,
)
from aomail.constants import DEFAULT_CATEGORY


def test_extract_contacts_recipients():
    result = extract_contacts_recipients(
        "Send an email to John Doe, Jane Doe, and John Smith"
    )
    assert result["main_recipients"] == ["John Doe", "Jane Doe", "John Smith"]
    assert result["cc_recipients"] == []
    assert result["bcc_recipients"] == []
    assert type(result["tokens_input"]) == int
    assert type(result["tokens_output"]) == int


def test_generate_response_keywords():
    result = generate_response_keywords(
        GENERATE_RESPONSE_KEYWORDS_PROMPT,
        "Will you be there on Friday?",
        "Meeting with John Doe",
    )
    assert type(result.get("keywords_list")) == list
    assert type(result["tokens_input"]) == int
    assert type(result["tokens_output"]) == int


def test_generate_email():
    result = generate_email(
        GENERATE_EMAIL_PROMPT,
        "Write an email to John Doe to ask if he will be there on Friday",
        "short",
        "formal",
        "english",
        {},
        "John Doe",
    )
    assert type(result["subject"]) == str
    assert type(result["body"]) == str
    assert type(result["tokens_input"]) == int
    assert type(result["tokens_output"]) == int


def test_correct_mail_language_mistakes():
    result = correct_mail_language_mistakes(
        "i wont b ther on Friay ev", "Meetig wiz directo"
    )
    assert type(result["correctedSubject"]) == str
    assert type(result["correctedBody"]) == str
    assert type(result["numCorrections"]) == int
    assert type(result["tokens_input"]) == int
    assert type(result["tokens_output"]) == int


def test_improve_email_copywriting():
    result = improve_email_copywriting(
        "I won't be there on Friday evening", "Meeting with the director"
    )
    assert type(result["feedback_ai"]) == str
    assert type(result["tokens_input"]) == int
    assert type(result["tokens_output"]) == int


def test_generate_email_response():
    result = generate_email_response(
        GENERATE_EMAIL_RESPONSE_PROMPT,
        "Meeting with the director",
        "I won't be there on Friday evening",
        "Okay, it's fine. I have noticed our colleagues",
        {},
        "John Doe",
    )
    assert type(result["body"]) == str
    assert type(result["tokens_input"]) == int
    assert type(result["tokens_output"]) == int


def test_categorize_and_summarize_email():
    result = categorize_and_summarize_email(
        CATEGORIZE_AND_SUMMARIZE_EMAIL_PROMPT,
        "Meeting with the director",
        "I won't be there on Friday evening",
        {DEFAULT_CATEGORY: "Default category for unclassified emails"},
        "John Doe is a worker at Noname company",
        "johndoe@gmail.com",
        "if it's strictly work-related AND either urgent or requires prompt business action",
        "if it's strictly work-related AND contains company updates or non-urgent team info",
        "it's promotional OR newsletter content (like TV shows, marketing emails, subscriptions)",
    )
    assert type(result["topic"]) == str
    assert type(result["response"]) == str
    assert type(result["relevance"]) == str
    assert type(result["importance"]) == str
    assert type(result["flags"]) == dict
    assert type(result["flags"]["spam"]) == bool
    assert type(result["flags"]["scam"]) == bool
    assert type(result["flags"]["newsletter"]) == bool
    assert type(result["flags"]["notification"]) == bool
    assert type(result["flags"]["meeting"]) == bool
    assert type(result["summary"]) == dict
    assert type(result["summary"]["one_line"]) == str
    assert type(result["summary"]["short"]) == str
    assert type(result["tokens_input"]) == int
    assert type(result["tokens_output"]) == int


def test_search_emails():
    result = search_emails(
        "Meeting with the director from 2025-02-28 and sender is John Doe",
        "english",
    )
    assert type(result["max_results"]) == int
    assert type(result["from"]) == list
    assert type(result["to"]) == list
    assert type(result["subject"]) == str
    assert type(result["body"]) == str
    assert type(result["filenames"]) == list
    assert type(result["date_from"]) == str
    assert type(result["keywords"]) == list
    assert type(result["search_in"]) == dict
    assert type(result["search_in"]["read"]) == bool
    assert type(result["search_in"]["unread"]) == bool
    assert type(result["search_in"]["drafts"]) == bool
    assert type(result["search_in"]["sent_emails"]) == bool
    assert type(result["search_in"]["deleted_emails"]) == bool
    assert type(result["search_in"]["spams"]) == bool
    assert type(result["tokens_input"]) == int
    assert type(result["tokens_output"]) == int


def test_review_user_description():
    result = review_user_description("John Doe is a worker at Noname company")
    assert type(result["feedback"]) == str
    assert type(result["valid"]) == bool
    assert type(result["tokens_input"]) == int
    assert type(result["tokens_output"]) == int


def test_generate_categories_scratch():
    result = generate_categories_scratch(
        "I receive a lot of sports emails, work at Noname company, and marketing emails that I hate + cold promotional emails",
    )
    assert type(result["categories"]) == list
    for category in result["categories"]:
        assert type(category["name"]) == str
        assert type(category["description"]) == str
        assert type(category["feedback"]) == str
    assert type(result["tokens_input"]) == int
    assert type(result["tokens_output"]) == int


def test_generate_prioritization_scratch():
    result = generate_prioritization_scratch(
        "I receive a lot of sports emails, work at Noname company, and marketing emails that I hate + cold promotional emails",
    )
    assert type(result["important"]) == str
    assert type(result["informative"]) == str
    assert type(result["useless"]) == str
    assert type(result["tokens_input"]) == int
    assert type(result["tokens_output"]) == int


def test_determine_action_scenario():
    result = determine_action_scenario(
        False, False, False, "Send email to John Doe and Patricia", True
    )

    assert result["scenario"] in [1, 2, 3]
    assert type(result["tokens_input"]) == int
    assert type(result["tokens_output"]) == int

    result = determine_action_scenario(True, False, True, "", True)
    assert result["scenario"] == 3
    assert result["tokens_input"] == 0
    assert result["tokens_output"] == 0

    result = determine_action_scenario(True, False, False, "", False)
    assert result["scenario"] == 3
    assert result["tokens_input"] == 0
    assert result["tokens_output"] == 0

    result = determine_action_scenario(True, True, False, "", False)
    assert result["scenario"] == 3
    assert result["tokens_input"] == 0
    assert result["tokens_output"] == 0

    result = determine_action_scenario(True, True, True, "", True)
    assert result["scenario"] == 3
    assert result["tokens_input"] == 0
    assert result["tokens_output"] == 0

    result = determine_action_scenario(False, True, True, "", False)
    assert result["scenario"] == 4
    assert result["tokens_input"] == 0
    assert result["tokens_output"] == 0


def test_improve_email_response():
    result = improve_email_response(
        IMPROVE_EMAIL_RESPONSE_PROMPT,
        "important",
        "Meeting with the director",
        "Okay, it's fine. I have noticed our colleagues",
        {},
        "Make it more formal and add a signature",
        {},
    )
    assert type(result["body"]) == str
    assert type(result["tokens_input"]) == int
    assert type(result["tokens_output"]) == int


def test_improve_draft():
    result = improve_draft(
        IMPROVE_EMAIL_DRAFT_PROMPT,
        "english",
        {},
        "Meeting with the director",
        "I won't be there on Friday evening",
        {},
        "Make it more formal and add a signature",
        "short",
        "formal",
    )
    assert type(result["subject"]) == str
    assert type(result["body"]) == str
    assert type(result["tokens_input"]) == int
    assert type(result["tokens_output"]) == int


def test_select_categories():
    result = select_categories(
        json.dumps(
            {
                "Jobs": ["Indeed", "Glassdoor", "LinkedIn", "Gradcracker"],
                "Sports": ["Cycling", "Football"],
                "Work": ["Aomail", "AlphaPen"],
                "ESAIP": ["Java", "Network", "JavaScript", "Deutsch"],
            }
        ),
        "Did I receive any positive answer for my internship applications?",
    )
    tokens_input = result.pop("tokens_input")
    tokens_output = result.pop("tokens_output")
    assert type(tokens_input) == int
    assert type(tokens_output) == int
    for organization_list in result.values():
        assert type(organization_list) == list


def test_get_answer():
    result = get_answer(
        {
            "internship": {
                "Company1": {
                    "interview": {"keypoints": ["homework", "decent", "python"]}
                }
            }
        },
        "Did I receive any positive answer for my internship applications?",
        "english",
    )
    assert type(result["sure"]) == bool
    assert type(result["answer"]) == str
    assert type(result["tokens_input"]) == int
    assert type(result["tokens_output"]) == int


def test_summarize_conversation():
    result = summarize_conversation(
        "subject",
        "body",
        "user_description",
        {
            "sports": ["Cycling", "Football"],
            "work": ["Project X", "Project Y"],
            "internship": ["refuse", "accept"],
        },
        "english",
    )
    assert type(result["category"]) == str
    assert type(result["organization"]) == str
    assert type(result["topic"]) == str
    assert type(result["keypoints"]) == dict
    for keypoints in result["keypoints"].values():
        assert type(keypoints) == list
    assert type(result["tokens_input"]) == int
    assert type(result["tokens_output"]) == int


def test_summarize_email():
    result = summarize_email(
        "Meeting with the director",
        "I won't be there on Friday evening",
        "John Doe is a worker at Noname company",
        {
            "sports": ["Cycling", "Football"],
            "work": ["Project X", "Project Y"],
            "internship": ["refuse", "accept"],
        },
        "english",
    )
    assert type(result["category"]) == str
    assert type(result["organization"]) == str
    assert type(result["topic"]) == str
    assert type(result["keypoints"]) == list
    assert type(result["tokens_input"]) == int
    assert type(result["tokens_output"]) == int
