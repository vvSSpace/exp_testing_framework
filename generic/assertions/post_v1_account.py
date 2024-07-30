import allure
from hamcrest import assert_that, has_entries
from generic.helpers.orm_db import OrmDatabase


class AssertionsPostV1Account:
    def __init__(self, dm_orm_db: OrmDatabase):
        self.dm_orm_db = dm_orm_db

    def check_user_was_created(self, login):
        with allure.step("Проверка что пользователь был создан"):
            dataset = self.dm_orm_db.get_user_by_login(login=login)
            for row in dataset:
                assert_that(row, has_entries(
                    {
                        'Login': login,
                        'Activated': False
                    }
                ))

    def check_user_was_activation(self, login):
        with allure.step("Проверка что пользователь был активирован через БД"):
            dataset = self.dm_orm_db.get_user_by_login(login=login)
            for row in dataset:
                assert_that(row, has_entries(
                    {
                        'Activated': True
                    }
                ))
