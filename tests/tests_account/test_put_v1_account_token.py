import allure


@allure.suite("Тесты на проверку метода PUT /v1/account{token}")
@allure.title("Проверка авторизации пользователя")
@allure.severity(allure.severity_level.BLOCKER)
def test_put_v1_account_token(dm_api_facade, dm_orm_db, prepare_user):
    email = prepare_user.email
    login = prepare_user.login
    password = prepare_user.password
    dm_api_facade.mailhog.del_all_messages()
    dm_api_facade.account.register_new_user(email=email, login=login, password=password, status_code=201)
    dm_api_facade.account.activate_registered_user(login=login, status_code=200)
    dm_orm_db.del_user_by_login(login=login)