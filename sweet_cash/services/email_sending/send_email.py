import logging
import smtplib
import ssl
import jwt

from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sweet_cash.settings import Settings

logger = logging.getLogger(name="email sending")


# TODO Перенести в интеграции
class SendEmail(object):

    def __call__(self, email: str):
        try:
            server = smtplib.SMTP_SSL(host=Settings.SMTP_HOST)
            # server.starttls(context=ssl.create_default_context())
            server.login(Settings.EMAIL_ADDRESS, Settings.EMAIL_PASSWORD)

            msg = MIMEMultipart()

            msg['From'] = Settings.EMAIL_ADDRESS
            msg['To'] = email
            msg['Subject'] = 'Подтверждение регистрации Sweet Cash'

            expires_delta = timedelta(24)
            confirmation_code = self._create_access_token(data={"sub": email}, expires_delta=expires_delta)

            content = f"""\
                    <html>
                      <body>
                        <p>Привет!<br>
                           Для завершения регистрации на Sweet Cash перейдите по
                           <a href="http://127.0.0.1:5000/api/v1/auth/confirm?email={email}&code={confirmation_code}">ссылке</a>.
                        </p>
                      </body>
                    </html>
                    """

            msg.attach(MIMEText(content, 'html'))

            server.send_message(msg)

            del msg

        except Exception as e:
            print(e)

        logger.info(f'Email sent to address {email}')

        return "Ok"

    @staticmethod
    def _create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
        return encoded_jwt
