import cloudscraper
import langid
import os
import re
import requests
import smtplib
import ssl
from ebooklib import epub
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from readability import Document
from urllib.parse import urlparse


# E-mail credentials
SENDER_ADDRESS = os.environ.get("SENDER_ADDRESS")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
RECEIVER_ADDRESS = os.environ.get("RECEIVER_ADDRESS")


def html2epub2kindle(url):
    # Get article
    print("Getting article")

    user_agent = ("Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101"
                  " Firefox/89.0")
    scraper = cloudscraper.create_scraper()
    res = scraper.get(url, headers={"User-Agent": user_agent})

    res.encoding = res.apparent_encoding

    html_article = Document(res.text)

    # Get clean filename
    # See https://github.com/django/django/blob/main/django/utils/text.py#L237
    filename = re.sub(
        r'(?u)[^-\w.]', '', str(html_article.short_title().strip() + ".epub").replace(' ', '_'))

    # Get article's language
    print("Detecting article's language")

    lang = langid.classify(html_article.summary())[0]

    # Create epub
    print("Converting html article to epub")

    # set metadata
    epub_article = epub.EpubBook()
    epub_article.set_title(html_article.title())
    epub_article.set_language(lang)
    epub_article.add_author(urlparse(url).netloc)

    # create chapter
    chapter = epub.EpubHtml(
        title="Article", file_name="article.xhtml", lang="hr")
    chapter.content = (html_article.summary())

    # add chapter
    epub_article.add_item(chapter)

    # add default Nav file
    epub_article.add_item(epub.EpubNav())

    # define spine
    epub_article.spine = ['nav', chapter]

    # write to the file
    epub.write_epub("/tmp/" + filename, epub_article, {})

    # Send epub file to Send-to-Kindle e-mail address
    message = MIMEMultipart()
    message['Subject'] = html_article.title()
    port = 465

    print(f"Sending epub file to receiver address")

    with open("/tmp/" + filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment", filename=filename)
        message.attach(part)

    message["To"] = RECEIVER_ADDRESS
    text = message.as_string()
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(
        "smtp.gmail.com", port, context=context
    ) as server:
        server.login(SENDER_ADDRESS, SENDER_PASSWORD)
        server.sendmail(SENDER_ADDRESS, RECEIVER_ADDRESS, text)
    print("\nDone\n")

    # Delete epub file
    os.remove("/tmp/" + filename)
