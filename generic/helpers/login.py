import allure
from apis.dm_api_account.models import LoginCredentials


class Login:
    def __init__(self, facade):
        self.facade = facade

    def set_headers(self, headers):
        self.facade.login_api.client.session.headers.update(headers)

    def login_user(
            self,
            login: str,
            password: str,
            status_code: int,
            remember_me: bool = True
    ):
        with allure.step("Авторизация пользователя"):
            response = self.facade.login_api.post_v1_account_login(
                json=LoginCredentials(
                    login=login,
                    password=password,
                    rememberMe=remember_me
                ),
                status_code=status_code
            )
        return response

    def get_auth_token(self, login: str, password: str, remember_me: bool = True):
        response = self.login_user(login=login, password=password, remember_me=remember_me, status_code=200)
        token = {'X-Dm-Auth-Token': response.headers['X-Dm-Auth-Token']}
        return token

    def logout_user(self, status_code: int, **kwargs):
        with allure.step("Выход из учётной записи пользователя"):
            response = self.facade.login_api.del_v1_account_login(status_code=status_code, **kwargs)
        return response

    def logout_user_from_all_devices(self, status_code: int, **kwargs):
        with allure.step("Выход из учётной записи пользователя на всех устройствах"):
            response = self.facade.login_api.del_v1_account_login_all(status_code=status_code, **kwargs)
        return response

