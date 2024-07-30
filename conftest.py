import pytest
import structlog
import allure
from generic.assertions.post_v1_account import AssertionsPostV1Account
from generic.helpers.search import Search
from services.dm_api_account import Facade
from generic.helpers.orm_db import OrmDatabase
from generic.helpers.mailhog import MailhogApi
from collections import namedtuple
from vyper import v
from pathlib import Path
from data.post_v1_account import PostV1AccountData as user_data
from apis.dm_api_search_async import SearchEngineStub
from grpclib.client import Channel

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)

options = (
    'service.dm_api_account',
    'service.mailhog',
    'database.dm3_5.host',
    'database.dm3_5.port',
    'database.dm3_5.database',
    'database.dm3_5.user',
    'database.dm3_5.password'
)


@pytest.fixture(autouse=True)
def set_config(request):
    config = Path(__file__).parent.joinpath('config')
    config_name = request.config.getoption('--env')
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(option, request.config.getoption(f'--{option}'))


def pytest_addoption(parser):
    parser.addoption('--env', action='store', default='stg')
    for option in options:
        parser.addoption(f'--{option}', action='store', default=None)


@pytest.fixture()
def grpc_search():
    client = Search(target=v.get('service.grpc'))
    yield client
    client.close()


@pytest.fixture()
def grpc_search_async():
    channel = Channel(host='192.168.2.167', port=5052)
    client = SearchEngineStub(channel)
    yield client
    channel.close()


@allure.step("Подготовка тестового пользователя")
@pytest.fixture
def prepare_user(dm_api_facade, dm_orm_db):
    user = namedtuple('User', 'email, login, password')
    User = user(email=user_data.email, login=user_data.login, password=user_data.password)
    return User


@pytest.fixture
def mailhog():
    return MailhogApi(
        host=v.get('service.mailhog')
    )


@pytest.fixture
def dm_api_facade(mailhog):
    return Facade(
        host=v.get('service.dm_api_account'),
        mailhog=mailhog
    )


@pytest.fixture
def dm_orm_db():
    orm = OrmDatabase(
        host=v.get('database.dm3_5.host'),
        port=v.get('database.dm3_5.port'),
        database=v.get('database.dm3_5.database'),
        user=v.get('database.dm3_5.user'),
        password=v.get('database.dm3_5.password')
    )
    yield orm
    orm.orm.close_connection()


@pytest.fixture
def assertions(dm_orm_db):
    return AssertionsPostV1Account(dm_orm_db)
