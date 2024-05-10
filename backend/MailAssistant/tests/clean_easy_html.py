import html
import re
from bs4 import BeautifulSoup
from colorama import Fore, init

# Initialize colorama for colored terminal output
init(autoreset=True)


# Print a header to indicate optional processing
print(
    f"{Fore.GREEN}=========== QUICK WAY TO GET HTML CONTENT EASILY ========"
)



# Constants for HTML transformations
NEWLINE_TO_BR = "<br>"
DIV_WRAPPER = "<div>{}</div>"

# Sample email message in bytes format
message = b"Bravo. Je te souhaite une bonne chance.\r\n\r\nAugustin\r\n________________________________\r\nFrom: Augustin <augustin@MailAssistant.onmicrosoft.com>\r\nSent: Thursday, May 9, 2024 8:11 PM\r\nTo: Augustin ROLET <augustin.rolet.pro@gmail.com>\r\nSubject: Re: Ceci est un pur test\r\n\r\nSalut, oui je viens je ram\xc3\xa8ne mon pique nique.\r\nA + bonne fin de journ\xc3\xa9e\r\n\r\nBernard\r\n________________________________\r\nFrom: Augustin <augustin@MailAssistant.onmicrosoft.com>\r\nSent: Thursday, May 9, 2024 7:44 PM\r\nTo: Augustin ROLET <augustin.rolet.pro@gmail.com>\r\nSubject: Re: Ceci est un pur test\r\n\r\nAh d'accord. est ce que tu viens demain?\r\n________________________________\r\nFrom: Augustin ROLET <augustin.rolet.pro@gmail.com>\r\nSent: Thursday, May 9, 2024 7:39 PM\r\nTo: Augustin <augustin@MailAssistant.onmicrosoft.com>\r\nSubject: Re: Ceci est un pur test\r\n\r\n\r\nSalut, j'utilise Thunderbird moi \xf0\x9f\x99\x82.\r\nBonne chance pour l'algo\r\n\r\n\r\nOn 5/9/2024 8:36 PM, Augustin wrote:\r\nCeci est un test depuis outlook\r\n________________________________\r\nFrom: Augustin <augustin@MailAssistant.onmicrosoft.com><mailto:augustin@MailAssistant.onmicrosoft.com>\r\nSent: Thursday, May 9, 2024 7:35 PM\r\nTo: Augustin <augustin@MailAssistant.onmicrosoft.com><mailto:augustin@MailAssistant.onmicrosoft.com>\r\nSubject: Re: Ceci est un pur test\r\n\r\nCecic esy un 2eme test qui va marcher en debug\r\n________________________________\r\nFrom: Augustin <augustin@MailAssistant.onmicrosoft.com><mailto:augustin@MailAssistant.onmicrosoft.com>\r\nSent: Thursday, May 9, 2024 7:31 PM\r\nTo: Augustin <augustin@MailAssistant.onmicrosoft.com><mailto:augustin@MailAssistant.onmicrosoft.com>\r\nSubject: Re: Ceci est un pur test\r\n\r\nJevois bien cela lakhuerese\r\n________________________________\r\nFrom: Augustin <augustin@MailAssistant.onmicrosoft.com><mailto:augustin@MailAssistant.onmicrosoft.com>\r\nSent: Thursday, May 9, 2024 7:30 PM\r\nTo: Augustin <augustin@MailAssistant.onmicrosoft.com><mailto:augustin@MailAssistant.onmicrosoft.com>\r\nSubject: Re: Ceci est un pur test\r\n\r\nOui, c'est bien mais ce n'est pas le cas\r\n________________________________\r\nFrom: Augustin <augustin@MailAssistant.onmicrosoft.com><mailto:augustin@MailAssistant.onmicrosoft.com>\r\nSent: Thursday, May 9, 2024 7:29 PM\r\nTo: Augustin <augustin@MailAssistant.onmicrosoft.com><mailto:augustin@MailAssistant.onmicrosoft.com>\r\nSubject: Ceci est un pur test\r\n\r\nj'imagine que personne ne bidouille\r\n"

# Decode the byte message to string and escape HTML special characters
text = message.decode("utf-8")
escaped_text = html.escape(text)

# Replace newline characters with HTML line breaks
formatted_text = escaped_text.replace("\r\n", NEWLINE_TO_BR)

# Wrap the formatted text in a div element
html_content = DIV_WRAPPER.format(formatted_text)

# Use regular expressions to remove unnecessary HTML character entities
html_content = re.sub(r"&gt;", "", html_content)
html_content = re.sub(r"&lt;", "", html_content)

# Print the initial HTML content
print(Fore.GREEN + "Initial HTML Content:")
print(html_content)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Prettify the HTML content using BeautifulSoup for better readability
pretty_html = soup.prettify()

# Remove email addresses from the prettified HTML content
# This regex targets typical email patterns within the text
email_cleaned_content = re.sub(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "", pretty_html
)

# Print the cleaned HTML content without email addresses
print(Fore.CYAN + "Cleaned HTML Content:")
print(email_cleaned_content)


###############################################################################################################################
###############################################################################################################################
###############################################################################################################################

# Print a header to indicate optional processing
print(
    f"{Fore.RED}=========== IF NEEDED (but need to handle most common date formats in various languages ==> super hard)========"
)

# Sample email content
email_content = """
<div> Bonjour, <br/> <br/> Merci <br/> Augustin ROLET <br/> <br/> <br/> <br/> On 5/6/2024 3:48 PM, CROCHET Moise wrote: <br/> Bonjour Augustin, Bonne semaine<br/> <br/> </div> """

# Regular expression pattern to search for date formats (MM/DD/YYYY)
date_pattern = r"\b\d{1,2}/\d{1,2}/\d{4}\b"

# Search for the first date format in the email content
match = re.search(date_pattern, email_content)

# Check if a date was found and print the result
if match:
    print("First date found:", match.group())
else:
    print("No date found in the email content.")
