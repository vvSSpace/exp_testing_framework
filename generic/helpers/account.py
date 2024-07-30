import allure
from dm_api_account.models import Registration, ResetPassword, ChangePassword, ChangeEmail


class Account:
    def __init__(self, facade):
        from services.dm_api_account import Facade
        self.facade: Facade = facade

    def set_headers(self, headers):
        self.facade.account_api.client.session.headers.update(headers)

    def register_new_user(self, login: str, email: str, password: str, status_code: int):
        with allure.step("Регистрация нового пользователя"):
            response = self.facade.account_api.post_v1_account(
                json=Registration(
                    login=login,
                    email=email,
                    password=password
                ),
                status_code=status_code
            )
        return response

    def activate_registered_user(self, login: str, status_code: int):
        token = self.facade.mailhog.get_token_by_login(login=login)
        with allure.step("Активация пользователя"):
            response = self.facade.account_api.put_v1_account(
                token=token,
                status_code=status_code
            )
        return response

    def get_currents_user_info(self, status_code: int, **kwargs):
        with allure.step("Получение данных пользователя"):
            response = self.facade.account_api.get_v1_account(
                status_code=status_code,
                **kwargs
            )
        return response

    def reset_registered_user_password(self, login: str, email: str, status_code: int):
        with allure.step("Сброс пароля пользователя"):
            response = self.facade.account_api.post_v1_account_password(
                json=ResetPassword(
                    login=login,
                    email=email,
                ),
                status_code=status_code
            )
        return response

    def change_registered_user_password(self, login: str, old_password: str, new_password: str, status_code: int):
        token = self.facade.mailhog.get_token_by_login(login=login, reset_password=True)
        with allure.step("Изменение пароля пользователя"):
            response = self.facade.account_api.put_v1_account_password(
                json=ChangePassword(
                    login=login,
                    token=token,
                    oldPassword=old_password,
                    newPassword=new_password
                ),
                status_code=status_code
            )
        return response

    def change_registered_email(self, login: str, password: str, email: str, status_code: int):
        with allure.step("Изменение email пользователя"):
            response = self.facade.account_api.put_v1_account_email(
                json=ChangeEmail(
                    login=login,
                    password=password,
                    email=email
                ),
                status_code=status_code
            )
        return response
