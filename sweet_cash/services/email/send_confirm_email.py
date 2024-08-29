
import asyncio
import logging

from aiosmtplib import SMTP
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sweet_cash.settings import Settings
from sweet_cash.auth.utils import create_access_token
from sweet_cash.errors import APIError

logger = logging.getLogger(name="email sending")


class SendConfirmRegistrationEmail(object):

    def __init__(self, smtp: SMTP) -> None:
        self.smtp = smtp
    
    async def __call__(self, email: str) -> None:
        
        # Переподключение smtp, если оно пропало. Таймаут 10 секунд
        if self.smtp.protocol is None:
            try:
                await asyncio.wait_for(self.smtp.connect(), 10)
            except asyncio.exceptions.TimeoutError:
                raise APIError("Smtp connection timed out")

        try:
            msg = MIMEMultipart()

            msg['From'] = Settings.EMAIL_ADDRESS
            msg['To'] = email
            msg['Subject'] = 'Подтверждение регистрации Sweet Cash'

            expires_delta = timedelta(24)
            confirmation_code = create_access_token(data={"sub": email}, expires_delta=expires_delta)

            content = f"""\
                    <html>
                      <body>
                        <p>Привет!<br>
                           Для завершения регистрации в Sweet Cash перейдите по
                           <a href="{Settings.HOST}/confirm?email={email}&code={confirmation_code}">ссылке</a>.
                        </p>
                      </body>
                    </html>
                    """

            msg.attach(MIMEText(content, 'html'))

            await self.smtp.send_message(msg)

            del msg

        except Exception as e:
            print(e)

        logger.info(f'Email for confirm registration sent to address {email}')
