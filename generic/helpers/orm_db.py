import allure
from typing import List
from sqlalchemy import select, update, delete
from common_libs.orm_client.orm_client import OrmClient
from generic.helpers.orm_models import User
from hamcrest import assert_that, has_entries


class OrmDatabase:
    def __init__(self, host, port, database, user, password):
        self.orm = OrmClient(host, port, database, user, password)

    def get_all_users(self):
        query = select([User])
        dataset = self.orm.send_query(query)
        return dataset

    def get_user_by_login(self, login: str) -> List[User]:
        with allure.step("Получение данных пользователя"):
            query = select([User]).where(User.Login == login)
            dataset = self.orm.send_query(query=query)
        return dataset

    def activate_user_by_login(self, login: str):
        with allure.step("Активация пользователя через БД"):
            query = update(User).where(User.Login == login).values(Activated=True)
            self.orm.send_bulk_query(query=query)

    def del_user_by_login(self, login: str):
        with allure.step("Удаление пользователя"):
            query = delete(User).where(User.Login == login)
            self.orm.send_bulk_query(query=query)
            self.confirm_del_user_by_login(login=login)

    def confirm_del_user_by_login(self, login: str):
        with allure.step("Проверка что пользователь был удалён из БД"):
            query = select([User]).where(User.Login == login)
            dataset = self.orm.send_query(query=query)
            assert len(dataset) == 0, f'Пользователь {login} не был удалён из базы данных'

    def del_all_users(self):
        query = delete(User)
        self.orm.send_bulk_query(query=query)
