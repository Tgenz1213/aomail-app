"""
Test file to handle chat bot conv
"""
#import claude
from langchain.memory import ChatMessageHistory


class EmailReplyConversation:
    """Handles the conv with the AI to reply to an email."""


    def __init__(self, user) -> None:
        self.user = user
        #main_list, cc_list, bcc_list = claude.extract_contacts_recipients("à test")
        # TODO: use the algo in views.py
        self.history = ChatMessageHistory()
        print(self.user)



    def start_chat(self):
        self.history.add_ai_message("Hello, to whom would you like to send this e-mail?")


email_reply_conv = EmailReplyConversation("1")
print(email_reply_conv.history)