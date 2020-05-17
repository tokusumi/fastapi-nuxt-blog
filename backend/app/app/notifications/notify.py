from typing import Dict, List
import sendgrid
import json
import urllib.parse
from sendgrid.helpers.mail import (
    From,
    Content,
    Mail,
    To,
)
from app.blogs.models import Post
from app.settings.configs import (
    SENDGRID_API_KEY,
    FROM_EMAIL,
    POST_NOFICATION_TEMPLATE,
    HOSTNAME,
)


def load_json(path: str) -> Dict[str, str]:
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def post_mail_notify(post: Post):
    data = {
        'author': post.author.username if post.author.username else post.author.email,
        'title': post.title,
        'url': urllib.parse.urljoin(HOSTNAME, f'/post/{post.id}/'),
        'to_emails': [f.email for f in post.author.friends]
    }
    return _mail_notify(**data)


def _mail_notify(author: str, title: str, url: str, to_emails: List[str]):
    if not SENDGRID_API_KEY:
        return None

    data = load_json(POST_NOFICATION_TEMPLATE)
    if not data.get('body'):
        raise KeyError('e-mail template does not contain body')

    sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
    from_email = From(FROM_EMAIL)
    subject = data.get('subject', '').format(author=author)
    content = Content("text/plain", data.get('body', '').format(title=title, author=author, url=url))
    for to_email in to_emails:
        to_email = To(to_email)
        mail = Mail(from_email, to_email, subject, content)
        sg.send(mail)
