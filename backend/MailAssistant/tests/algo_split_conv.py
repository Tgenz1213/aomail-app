import html
import re
from bs4 import BeautifulSoup
from colorama import Fore, init

# Initialize colorama for colored terminal output
init(autoreset=True)

# Print section headers in the console with clear demarcation and color
section_header = "-" * 110
print(f"{Fore.BLUE}{section_header}")
print(f"{Fore.BLUE}# [GOOGLE] THIS IS FROM HTML SAFE (taking only pre)")
print(f"{Fore.BLUE}{section_header}")

# Sample HTML content for processing
html_content = """
Salut,
oui j'aimerai tellement ça fait un moment que l'on ne sait pas vu.

Quels sont tes disponibilités?

Paul
________________________________
From: Augustin ROLET <augustin.rolet.pro@gmail.com>
Sent: Friday, May 10, 2024 9:44 AM
To: Augustin <augustin@mailassistant.onmicrosoft.com>
Subject: Re: Salut

Moi aussi 😀.
Ca te dit qu'on fasse un foot avec mes copains du lycée?

Le ven. 10 mai 2024 à 10:02, Augustin <augustin@mailassistant.onmicrosoft.com> a écrit :
Salut Augustin,
Oui, je suis content que tu me contacte.
Paul
________________________________
From: Augustin ROLET <augustin.rolet.pro@gmail.com>
Sent: Friday, May 10, 2024 9:01 AM
To: Augustin <augustin@mailassistant.onmicrosoft.com>
Subject: Salut

Salut Paul,

est ce que cv ?

--
Augustin ROLET
Software Engineer Student
GitHub: github.com/teloryfrozy
"""


def split_email_goog(body: str):
    """
    Extracts and prints the last email from a given email thread.

    Args:
    body (str): The string containing the entire email thread.

    This function uses a regular expression to split the email content based on a line of underscores,
    which typically denotes separation between emails in a thread. It then prints each part separately.
    """
    # Regex pattern to match a line of underscores, possibly surrounded by whitespace
    line_pattern = r"\s*_{6,}\s*"

    # Split the email body into parts using the regex pattern
    parts = re.split(line_pattern, body)

    # Iterate over each part and print it
    for part in parts:
        print(
            "::::::::::::::::::::::PART extracted GOOG::::::::::::::::::::::::::::::::::::::::"
        )
        print(part.strip())


# Call the function to process the HTML content
split_email_goog(html_content)


# Print section headers in the console with clear demarcation and color
print("-" * 110)
print(f"{Fore.CYAN}# [MICROSOFT] MICROSOFT SPLIT EMAIL 2")
print("-" * 110)

# MICROSOFT SPLIT EMAIL 2
html_content = """
<p>Salut Paul,</p><p>Youpi.<br>Je peux à partir de mi juin si tout ce passe bien.<br>Augustin 📚⌚😀<br></p><p><br></p><p><br></p><div class="moz-cite-prefix">On 5/10/2024 10:46 AM, Augustin wrote:<br></div><blockquote type="cite"><style type="text/css" style="display:none">
<!--
p
        {margin-top:0;
        margin-bottom:0}
-->
</style><div class="elementToProof" style="font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0)">Salut,</div><div class="elementToProof" style="font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0)">oui j'aimerai tellement ça fait un moment que l'on ne sait pas vu.<br><br>Quels sont tes disponibilités?<br><br>Paul</div><hr tabindex="-1" style="display:inline-block; width:98%"><div id="divRplyFwdMsg" dir="ltr"><font face="Calibri, sans-serif" color="#000000" style="font-size:11pt"><b>From:</b> Augustin ROLET <a class="moz-txt-link-rfc2396E" href="mailto:augustin.rolet.pro@gmail.com">&lt;augustin.rolet.pro@gmail.com&gt;</a><br><b>Sent:</b> Friday, May 10, 2024 9:44 AM<br><b>To:</b> Augustin <a class="moz-txt-link-rfc2396E" href="mailto:augustin@MailAssistant.onmicrosoft.com">&lt;augustin@MailAssistant.onmicrosoft.com&gt;</a><br><b>Subject:</b> Re: Salut</font> <div>&nbsp;</div></div><div><div dir="ltr"><div>Moi aussi 😀.<br></div>Ca te dit qu'on fasse un foot avec mes copains du lycée?<br><br></div><br><div class="x_gmail_quote"><div dir="ltr" class="x_gmail_attr">Le&nbsp;ven. 10 mai 2024 à&nbsp;10:02, Augustin &lt;<a href="mailto:augustin@mailassistant.onmicrosoft.com" class="moz-txt-link-freetext">augustin@mailassistant.onmicrosoft.com</a>&gt; a écrit&nbsp;:<br></div><blockquote class="x_gmail_quote" style="margin:0px 0px 0px 0.8ex; border-left:1px solid rgb(204,204,204); padding-left:1ex"><div class="x_msg2542158256977656014"><div dir="ltr"><div style="font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0)">Salut Augustin,</div><div style="font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0)">Oui, je suis content que tu me contacte.</div><div style="font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0)">Paul</div><hr style="display:inline-block; width:98%"><div id="x_m_2542158256977656014divRplyFwdMsg" dir="ltr"><font face="Calibri, sans-serif" color="#000000" style="font-size:11pt"><b>From:</b> Augustin ROLET &lt;<a href="mailto:augustin.rolet.pro@gmail.com" target="_blank" class="moz-txt-link-freetext">augustin.rolet.pro@gmail.com</a>&gt;<br><b>Sent:</b> Friday, May 10, 2024 9:01 AM<br><b>To:</b> Augustin &lt;<a href="mailto:augustin@MailAssistant.onmicrosoft.com" target="_blank" class="moz-txt-link-freetext">augustin@MailAssistant.onmicrosoft.com</a>&gt;<br><b>Subject:</b> Salut</font> <div>&nbsp;</div></div><div><font size="2"><span style="font-size:11pt"><div>Salut Paul,<br><br>est ce que cv ?<br><br>-- <br>Augustin ROLET<br>Software Engineer Student<br>GitHub: <a href="http://github.com/teloryfrozy" target="_blank">github.com/teloryfrozy</a><br><br></div></span></font></div></div></div></blockquote></div></div></blockquote>
"""


def split_email_msft(body: str):
    """
    Splits the email content based on HTML comment patterns.

    This function identifies sections of an email separated by HTML comments and extracts each section
    as a distinct part. It is particularly useful for processing emails that contain threaded or
    forwarded messages encapsulated within HTML comments.

    Parameters:
    - body (str): The HTML content of the email.

    Returns:
    - list: A list of the separated parts of the email.
    """
    # Define the pattern to match HTML comments
    separator = r"<!--.*?-->"

    # Split the content using the defined separator pattern
    parts = re.split(separator, body, flags=re.IGNORECASE | re.DOTALL)

    # Iterate over the parts and print non-empty parts
    for index, part in enumerate(parts):
        if part.strip():  # Check to ensure part is not just whitespace
            print(
                f"\n\n::::::::::::::::::::::::PART {index + 1}:::::::::::::::::::::::::::::::::"
            )
            print(part.strip())

    return parts


# Call the function with the HTML content
split_email_msft(html_content)


# CONVERSATION_HTML_MSFT = split_email_msft(html_content)[1]
print("-" * 110)
print(f"{Fore.YELLOW}# [MICROSOFT] SPLIT CONVERSATION HISTORY (NOT NEEDED AND HARD)")
print("-" * 110)


# this should be taken from part [1] from prev function
CONVERSATION_HTML_MSFT = """
</style><div class="elementToProof" style="font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0)">Salut,</div><div class="elementToProof" style="font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0)">oui j'aimerai tellement ça fait un moment que l'on ne sait pas vu.<br><br>Quels sont tes disponibilités?<br><br>Paul</div><hr tabindex="-1" style="display:inline-block; width:98%"><div id="divRplyFwdMsg" dir="ltr"><font face="Calibri, sans-serif" color="#000000" style="font-size:11pt"><b>From:</b> Augustin ROLET <a class="moz-txt-link-rfc2396E" href="mailto:augustin.rolet.pro@gmail.com">&lt;augustin.rolet.pro@gmail.com&gt;</a><br><b>Sent:</b> Friday, May 10, 2024 9:44 AM<br><b>To:</b> Augustin <a class="moz-txt-link-rfc2396E" href="mailto:augustin@MailAssistant.onmicrosoft.com">&lt;augustin@MailAssistant.onmicrosoft.com&gt;</a><br><b>Subject:</b> Re: Salut</font> <div>&nbsp;</div></div><div><div dir="ltr"><div>Moi aussi 😀.<br></div>Ca te dit qu'on fasse un foot avec mes copains du lycée?<br><br></div><br><div class="x_gmail_quote"><div dir="ltr" class="x_gmail_attr">Le&nbsp;ven. 10 mai 2024 à&nbsp;10:02, Augustin &lt;<a href="mailto:augustin@mailassistant.onmicrosoft.com" class="moz-txt-link-freetext">augustin@mailassistant.onmicrosoft.com</a>&gt; a écrit&nbsp;:<br></div><blockquote class="x_gmail_quote" style="margin:0px 0px 0px 0.8ex; border-left:1px solid rgb(204,204,204); padding-left:1ex"><div class="x_msg2542158256977656014"><div dir="ltr"><div style="font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0)">Salut Augustin,</div><div style="font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0)">Oui, je suis content que tu me contacte.</div><div style="font-family:Aptos,Aptos_EmbeddedFont,Aptos_MSFontService,Calibri,Helvetica,sans-serif; font-size:12pt; color:rgb(0,0,0)">Paul</div><hr style="display:inline-block; width:98%"><div id="x_m_2542158256977656014divRplyFwdMsg" dir="ltr"><font face="Calibri, sans-serif" color="#000000" style="font-size:11pt"><b>From:</b> Augustin ROLET &lt;<a href="mailto:augustin.rolet.pro@gmail.com" target="_blank" class="moz-txt-link-freetext">augustin.rolet.pro@gmail.com</a>&gt;<br><b>Sent:</b> Friday, May 10, 2024 9:01 AM<br><b>To:</b> Augustin &lt;<a href="mailto:augustin@MailAssistant.onmicrosoft.com" target="_blank" class="moz-txt-link-freetext">augustin@MailAssistant.onmicrosoft.com</a>&gt;<br><b>Subject:</b> Salut</font> <div>&nbsp;</div></div><div><font size="2"><span style="font-size:11pt"><div>Salut Paul,<br><br>est ce que cv ?<br><br>-- <br>Augustin ROLET<br>Software Engineer Student<br>GitHub: <a href="http://github.com/teloryfrozy" target="_blank">github.com/teloryfrozy</a><br><br></div></span></font></div></div></div></blockquote></div></div></blockquote>
"""


def split_html_content(html_content: str):
    """
    Splits the HTML content into parts based on specific <div> tags.

    This function is designed to parse and split HTML content, specifically focusing on sections
    encapsulated within <div> tags that have a 'dir="ltr"' attribute. It's useful for extracting
    and analyzing parts of an HTML document or email content.

    Parameters:
    - html_content (str): The HTML content to be split.

    Returns:
    - list: A list of HTML content parts after splitting.
    """
    # Define the regex pattern to split HTML content based on <div> tag attributes
    pattern = r'<div\s+dir="ltr"[^>]*>'

    # Split the HTML content using the regex pattern
    parts = re.split(pattern, html_content)

    # Print and return the parts
    for index, part in enumerate(parts):
        if part.strip():  # Ensure the part is not just whitespace
            print(f"Part {index + 1}:")
            print(part.strip())
            print("-" * 25)  # Separator for readability

    return parts


# Call the function with the HTML content
split_html_content(CONVERSATION_HTML_MSFT)


###############################################################################################################################
###############################################################################################################################
###############################################################################################################################

# 2nd test if someone wants to check


def split_html_content(html_content: str):

    # Define the regex pattern to split HTML content based on <div> tag attributes
    pattern = r'<div\s+dir="ltr"[^>]*>'
    # Split the HTML content using the regex pattern
    parts = re.split(pattern, html_content)

    for part in parts:
        print(part.strip())
        print("-------------------------")


# Example HTML content
html_content = """
<html>
 <head>
  <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
  <style style="display:none;" type="text/css">
   P {margin-top:0;margin-bottom:0;}
  </style>
 </head>
 <body dir="ltr">
  <div class="elementToProof" style="font-family: Aptos, Aptos_EmbeddedFont, Aptos_MSFontService, Calibri, Helvetica, sans-serif; font-size: 12pt; color: rgb(0, 0, 0);">
   Salut Augustin,
  </div>
  <div class="elementToProof" style="font-family: Aptos, Aptos_EmbeddedFont, Aptos_MSFontService, Calibri, Helvetica, sans-serif; font-size: 12pt; color: rgb(0, 0, 0);">
   Oui, je suis content que tu me contacte.
  </div>
  <div class="elementToProof" style="font-family: Aptos, Aptos_EmbeddedFont, Aptos_MSFontService, Calibri, Helvetica, sans-serif; font-size: 12pt; color: rgb(0, 0, 0);">
   Paul
  </div>
  <div id="appendonsend">
  </div>
  <hr style="display:inline-block;width:98%" tabindex="-1"/>
  <div dir="ltr" id="divRplyFwdMsg">
   <font color="#000000" face="Calibri, sans-serif" style="font-size:11pt">
    <b>
     From:
    </b>
    Augustin ROLET &lt;augustin.rolet.pro@gmail.com&gt;
    <br/>
    <b>
     Sent:
    </b>
    Friday, May 10, 2024 9:01 AM
    <br/>
    <b>
     To:
    </b>
    Augustin &lt;augustin@MailAssistant.onmicrosoft.com&gt;
    <br/>
    <b>
     Subject:
    </b>
    Salut
   </font>
   <div>
   </div>
  </div>
  <div class="BodyFragment">
   <font size="2">
    <span style="font-size:11pt;">
     <div class="PlainText">
      Salut Paul,
      <br/>
      <br/>
      est ce que cv ?
      <br/>
      <br/>
      --
      <br/>
      Augustin ROLET
      <br/>
      Software Engineer Student
      <br/>
      GitHub: github.com/teloryfrozy
      <br/>
      <br/>
     </div>
    </span>
   </font>
  </div>
 </body>
</html>
"""


# THIS SMALL CODE IS USED TO SPLIT MICROSOFT HTML
# html_content = re.sub(r"<head>[\s\S]*?</head>", "", html_content)
# html_content =html_content.replace("<html>", "")
# html_content = html_content.replace("</html>", "")
# html_content = re.sub(r"<body(.*?)>", "", html_content)
# html_content = html_content.replace("</body>", "")


# # Split the content
# split_html_content(html_content)

# ___________________________________________________________________________________________________________#
