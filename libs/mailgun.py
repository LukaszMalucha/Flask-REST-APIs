import os
from typing import List
from requests import Response, post

class Mailgun:
    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
    FROM_TITLE = "Bookstore REST API"
    MAILGUN_EMAIL = os.environ.get('MAILGUN_EMAIL')


    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html: str) -> Response:

        return post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.MAILGUN_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html
            },
        )