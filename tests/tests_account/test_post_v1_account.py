import string
import random
import allure
import pytest
from hamcrest import assert_that, has_entries


def generate_random_string(length, num: bool = False):
    if num:
        letters = string.ascii_letters + string.digits
    else:
        letters = string.ascii_letters
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length)).lower()


def generate_random_email(at: bool = True, domain: bool = True):
    if at:
        at_value = '@'
    else:
        at_value = ''
    if domain:
        domains_value = generate_random_string(random.randint(3, 6)) + '.' + generate_random_string(2)
    else:
        domains_value = ''
    generated_email = str(
        generate_random_string(random.randint(5, 10), num=True) +
        at_value +
        domains_value
    )
    return generated_email


@allure.suite("Тесты на проверку метода POST /v1/account")
@allure.sub_suite("Позитивные тесты")
@allure.severity(allure.severity_level.BLOCKER)
class TestPostV1Account:
    @allure.title("Проверка регистрации и активации пользователя")
    def test_post_v1_account(self, dm_api_facade, dm_orm_db, prepare_user, assertions):
        email = prepare_user.email
        login = prepare_user.login
        password = prepare_user.password
        dm_api_facade.mailhog.del_all_messages()
        dm_api_facade.account.register_new_user(email=email, login=login, password=password, status_code=201)
        assertions.check_user_was_created(login=login)
        dm_orm_db.get_user_by_login(login=login)
        dm_orm_db.activate_user_by_login(login=login)
        assertions.check_user_was_activation(login=login)
        dm_api_facade.login.login_user(login=login, password=password, status_code=200)
        dm_orm_db.del_user_by_login(login=login)

    @pytest.mark.parametrize('login, email, password, status_code, check', [
        # Валидные даныне
        (
                str(generate_random_string(random.randint(5, 10), num=True)),
                generate_random_email(),
                str(generate_random_string(random.randint(8, 12), num=True)),
                201,
                ''
        ),
        # Пароль менее или равен 5-ти символам
        (
                str(generate_random_string(random.randint(5, 10))),
                generate_random_email(),
                str(generate_random_string(random.randint(1, 5), num=True)),
                400,
                {"Password": ["Short"]}
        ),
        # Логин менее 2-х символов
        (
                str(generate_random_string(random.randint(1, 1))),
                generate_random_email(),
                str(generate_random_string(random.randint(8, 12), num=True)),
                400,
                {"Login": ["Short"]}
        ),
        # Email не содержит домен
        (
                str(generate_random_string(random.randint(5, 10))),
                generate_random_email(domain=False),
                str(generate_random_string(random.randint(8, 12), num=True)),
                400,
                {"Email": ["Invalid"]}
        ),
        # Email не содержит '@'
        (
                str(generate_random_string(random.randint(5, 10))),
                generate_random_email(at=False),
                str(generate_random_string(random.randint(8, 12), num=True)),
                400,
                {"Email": ["Invalid"]}
        )
    ])
    @allure.title("Дополнительная проверка на случайных данных")
    def test_create_and_activated_user_with_random_params(
            self,
            dm_api_facade,
            dm_orm_db,
            login,
            email,
            password,
            status_code,
            check
    ):
        dm_api_facade.mailhog.del_all_messages()
        response = dm_api_facade.account.register_new_user(
            email=email,
            login=login,
            password=password,
            status_code=status_code
        )
        if response.status_code == 201:
            dm_orm_db.activate_user_by_login(login=login)
            dm_orm_db.del_user_by_login(login=login)
        else:
            assert_that(response.json()["errors"], has_entries(check))
