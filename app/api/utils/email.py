from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from app.config import settings
from jinja2 import Environment, select_autoescape, PackageLoader
from app.api.schemas.all import UserDB
from fastapi import HTTPException, status


env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


class Email:
    def __init__(self, username: str, url: str, email: List[EmailStr]):
        self.name = username
        self.url = url
        self.email = email

    async def send_mail(self, subject, template):
        # Define the config
        conf = ConnectionConfig(
            MAIL_USERNAME=settings.EMAIL_USERNAME,
            MAIL_PASSWORD=settings.EMAIL_PASSWORD.get_secret_value(),
            MAIL_FROM=settings.EMAIL_FROM,
            MAIL_PORT=settings.EMAIL_PORT,
            MAIL_SERVER=settings.EMAIL_HOST,
            MAIL_STARTTLS=False,
            MAIL_SSL_TLS=True,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        # Generate the HTML template base on the template name
        template = env.get_template(f'{template}.html')

        html = template.render(
            url=self.url,
            first_name=self.name,
            subject=subject
        )

        # Define the message options
        message = MessageSchema(
            subject=subject,
            recipients=self.email,
            body=html,
            subtype="html"
        )

        # Send the email
        fm = FastMail(conf)
        await fm.send_message(message)

    async def send_code(self, subject: str, valid_min: int):
        await self.send_mail(f'Your {subject} (valid for {valid_min} min)', 'verification')


class SendEmail:
    @staticmethod
    async def send_email(
            subject: str,
            url: str,
            user: UserDB,
     ) -> bool:
        try:
            await (Email(user.username, url, [user.email]).
                   send_code(subject, int(settings.VERIFY_TIME.seconds / 60)))
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='There was an error sending email')
        return True

