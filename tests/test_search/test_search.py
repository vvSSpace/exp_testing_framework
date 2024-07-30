import pprint
import allure
import pytest
from betterproto import Casing
from apis.dm_api_search_async import SearchRequest, SearchEntityType


@allure.suite("Тесты на проверку GRPC метода search")
@allure.sub_suite("Позитивные тесты")
@allure.severity(allure.severity_level.CRITICAL)
class TestGrpcSearch:
    @allure.title("Получение списка тем форума")
    def test_search(self, grpc_search):
        response = grpc_search.search(
            query='test_post',
            skip=0,
            size=10,
            search_across=['FORUM_TOPIC']
        )

    @allure.title("Получение списка тем форума (async)")
    @pytest.mark.asyncio
    async def test_search_async(self, grpc_search_async):
        response = await grpc_search_async.search(
            search_request=SearchRequest(
                query='test_post',
                skip=0,
                size=10,
                search_across=[SearchEntityType.FORUM_TOPIC]
            )
        )
        pprint.pprint(response.to_dict(casing=Casing.SNAKE))
