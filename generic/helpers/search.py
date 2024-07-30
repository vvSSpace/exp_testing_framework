from apis.dm_api_search.dm_api_search import DmApiSeach
from apis.dm_api_search.search_pb2 import SearchRequest


class Search:
    def __init__(self, target):
        self.grpc_search = DmApiSeach(target=target)

    def search(self, query: str, size: int, skip: int, search_across: list):
        response = self.grpc_search.search(
            request=SearchRequest(
                query=query,
                skip=skip,
                size=size,
                searchAcross=search_across
            )
        )
        return response

    def close(self):
        self.grpc_search.close()
