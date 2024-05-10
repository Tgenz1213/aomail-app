import html
import re
from bs4 import BeautifulSoup

# TODO: remove email preprocess data: 
# regex to remove when findin @ + check if provider.domain (only 2 stuff)
# mailto: | <mailto:augustin@MailAssistant.onmicrosoft.com>
# <augustin@MailAssistant.onmicrosoft.com>

message = b"Bravo. Je te souhaite une bonne chance.\r\n\r\nAugustin\r\n________________________________\r\nFrom: Augustin <augustin@MailAssistant.onmicrosoft.com>\r\nSent: Thursday, May 9, 2024 8:11 PM\r\nTo: Augustin ROLET <augustin.rolet.pro@gmail.com>\r\nSubject: Re: Ceci est un pur test\r\n\r\nSalut, oui je viens je ram\xc3\xa8ne mon pique nique.\r\nA + bonne fin de journ\xc3\xa9e\r\n\r\nBernard\r\n________________________________\r\nFrom: Augustin <augustin@MailAssistant.onmicrosoft.com>\r\nSent: Thursday, May 9, 2024 7:44 PM\r\nTo: Augustin ROLET <augustin.rolet.pro@gmail.com>\r\nSubject: Re: Ceci est un pur test\r\n\r\nAh d'accord. est ce que tu viens demain?\r\n________________________________\r\nFrom: Augustin ROLET <augustin.rolet.pro@gmail.com>\r\nSent: Thursday, May 9, 2024 7:39 PM\r\nTo: Augustin <augustin@MailAssistant.onmicrosoft.com>\r\nSubject: Re: Ceci est un pur test\r\n\r\n\r\nSalut, j'utilise Thunderbird moi \xf0\x9f\x99\x82.\r\nBonne chance pour l'algo\r\n\r\n\r\nOn 5/9/2024 8:36 PM, Augustin wrote:\r\nCeci est un test depuis outlook\r\n________________________________\r\nFrom: Augustin <augustin@MailAssistant.onmicrosoft.com><mailto:augustin@MailAssistant.onmicrosoft.com>\r\nSent: Thursday, May 9, 2024 7:35 PM\r\nTo: Augustin <augustin@MailAssistant.onmicrosoft.com><mailto:augustin@MailAssistant.onmicrosoft.com>\r\nSubject: Re: Ceci est un pur test\r\n\r\nCecic esy un 2eme test qui va marcher en debug\r\n________________________________\r\nFrom: Augustin <augustin@MailAssistant.onmicrosoft.com><mailto:augustin@MailAssistant.onmicrosoft.com>\r\nSent: Thursday, May 9, 2024 7:31 PM\r\nTo: Augustin <augustin@MailAssistant.onmicrosoft.com><mailto:augustin@MailAssistant.onmicrosoft.com>\r\nSubject: Re: Ceci est un pur test\r\n\r\nJevois bien cela lakhuerese\r\n________________________________\r\nFrom: Augustin <augustin@MailAssistant.onmicrosoft.com><mailto:augustin@MailAssistant.onmicrosoft.com>\r\nSent: Thursday, May 9, 2024 7:30 PM\r\nTo: Augustin <augustin@MailAssistant.onmicrosoft.com><mailto:augustin@MailAssistant.onmicrosoft.com>\r\nSubject: Re: Ceci est un pur test\r\n\r\nOui, c'est bien mais ce n'est pas le cas\r\n________________________________\r\nFrom: Augustin <augustin@MailAssistant.onmicrosoft.com><mailto:augustin@MailAssistant.onmicrosoft.com>\r\nSent: Thursday, May 9, 2024 7:29 PM\r\nTo: Augustin <augustin@MailAssistant.onmicrosoft.com><mailto:augustin@MailAssistant.onmicrosoft.com>\r\nSubject: Ceci est un pur test\r\n\r\nj'imagine que personne ne bidouille\r\n"



text = message.decode("utf-8")
escaped_text = html.escape(text)
formatted_text = escaped_text.replace("\r\n", "<br>")

html_content = f"<div>{formatted_text}</div>"  # Wrap in a div for example
html_content = re.sub(r"&gt;", "", html_content)
html_content = re.sub(r"&lt;", "", html_content)

print(html_content)

soup = BeautifulSoup(html_content, 'html.parser')
print(soup.prettify())























'''
import re

# Sample email content
email_content = """
<div> Bonjour, <br/> <br/> Merci <br/> Augustin ROLET <br/> <br/> <br/> <br/> On 5/6/2024 3:48 PM, CROCHET Moise wrote: <br/> Bonjour Augustin, <br/> <br/> </div> """

# Regular expression pattern to search for date formats
date_pattern = r'\b\d{1,2}/\d{1,2}/\d{4}\b'

# Search for the first date format in the email content
match = re.search(date_pattern, email_content)

if match:
    print("First date found:", match.group())
else:
    print("No date found in the email content.")
'''


# OR if there is _________________________ BEFORE finding a date then we can take everything before this line as the 1st email
# if one long line is found we try to find others and split like that
