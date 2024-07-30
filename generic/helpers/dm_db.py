import allure

from common_libs.db_client import DbClient


class DmDatabase:
    def __init__(self):
        self.db = DbClient()

    def get_all_users(self):
        query = 'SELECT * FROM "public"."Users"'
        dataset = self.db.send_query(query=query)
        return dataset

    def get_user_by_login(self, login: str):
        with allure.step("Проверка что пользователь был создан"):
            query = f'''
            SELECT * 
            FROM "public"."Users" 
            WHERE "Login" = '{login}'
            '''
            dataset = self.db.send_query(query=query)
        return dataset

    def del_user_by_login(self, login: str):
        with allure.step("Удаление пользователя"):
            query = f'''
            DELETE FROM "public"."Users" 
            WHERE "Login" = '{login}'
            '''
            self.db.send_bulk_query(query=query)
            self.confirm_del_user_by_login(login=login)

    def del_all_users(self):
        query = 'DELETE FROM "public"."Users"'
        self.db.send_bulk_query(query=query)

    def activate_user_by_login(self, login):
        with allure.step("Активация пользователя через БД"):
            query = f'''
            UPDATE "public"."Users" 
            SET "Activated" = True
            WHERE "Login" = '{login}'
            '''
            self.db.send_bulk_query(query=query)
            self.confirm_activate_user_by_login(login=login)

    def confirm_del_user_by_login(self, login: str):
        with allure.step("Проверка что пользователь был удалён из БД"):
            query = f'''
            SELECT * 
            FROM "public"."Users" 
            WHERE "Login" = '{login}'
            '''
            dataset = self.db.send_query(query=query)
            assert len(dataset) == 0, f'Пользователь {login} не был удалён из базы данных'

    def confirm_activate_user_by_login(self, login: str):
        with allure.step("Проверка что пользователь был активирован через БД"):
            query = f'''
            SELECT * 
            FROM "public"."Users" 
            WHERE "Login" = '{login}'
            '''
            dataset = self.db.send_query(query=query)
            for row in dataset:
                assert row['Activated'] is True, f'Пользователь {login} не был активирован'
