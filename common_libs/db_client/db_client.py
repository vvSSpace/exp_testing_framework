import allure
import records
import structlog
import uuid


def allure_attach(fn):
    def wrapper(*args, **kwargs):
        query = kwargs.get('query')
        allure.attach(
            str(query.compile(compile_kwargs={"literal_binds": True})),
            name='SQL request',
            attachment_type=allure.attachment_type.TEXT
        )
        dataset = fn(*args, **kwargs)
        if dataset is not None:
            allure.attach(
                str(dataset),
                name='SQL response',
                attachment_type=allure.attachment_type.TEXT
            )
        return dataset

    return wrapper


class DbClient:
    def __init__(self, host, port, database, user, password, isolation_level='AUTOCOMMIT'):
        connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
        self.db = records.Database(connection_string, isolation_level=isolation_level)
        self.log = structlog.get_logger(self.__class__.__name__).bind(service='db')

    @allure_attach
    def send_query(self, query):
        print(query)
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event='request',
            query=query
        )
        dataset = self.db.query(query=query).as_dict()
        log.msg(
            event='response',
            dataset=dataset
        )
        return dataset

    @allure_attach
    def send_bulk_query(self, query):
        print(query)
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event='request',
            query=query
        )
        self.db.bulk_query(query=query)
