import json
import time
import allure
from requests import Response
from common_libs.restclient.restclient import Restclient


def decorator(fn):
    def wrapper(*args, **kwargs):
        for i in range(5):
            response = fn(*args, **kwargs)
            emails = response.json()['items']
            if len(emails) < 1:
                print(f'attempt {i}')
                continue
            else:
                return response

    return wrapper


class MailhogApi:
    def __init__(self, host):
        self.host = host
        self.client = Restclient(host=host)

    @decorator
    def get_api_v2_messages(self, limit: int = 50) -> Response:
        """
        Get messages by limit
        :param limit: 
        :return: 
        """
        response = self.client.get(
            path="/api/v2/messages",
            params={
                'limit': limit
            }
        )
        return response

    def get_token_from_last_email(self) -> str:
        """
        Get user activation token from last email
        :return:
        """
        emails = self.get_api_v2_messages(limit=1).json()
        token_url = json.loads(emails['items'][0]['Content']['Body'])['ConfirmationLinkUrl']
        token = token_url.split('/')[-1]
        return token

    def get_token_by_login(self, login: str, attempt=5, reset_password: bool = False):
        if reset_password:
            text_error = 'сброса пароля'
            item = 'ConfirmationLinkUri'
        else:
            text_error = 'регистрации'
            item = 'ConfirmationLinkUrl'
        if attempt == 0:
            raise AssertionError(f'Не удалось получить письмо с подтверждением {text_error} для {login}')
        with allure.step("Получение токена из письма на почте"):
            emails = self.get_api_v2_messages(limit=50).json()['items']
            for email in emails:
                user_data = json.loads(email['Content']['Body'])
                if login == user_data.get('Login'):
                    token = user_data[item].split('/')[-1]
                    return token
            time.sleep(2)
        return self.get_token_by_login(login=login, attempt=attempt - 1)

    def del_all_messages(self):
        with allure.step("Удаление всех сообщений на почте"):
            response = self.client.delete(path='/api/v1/messages')
        return response
