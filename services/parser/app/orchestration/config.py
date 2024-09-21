from app.extractor import PageExtractorInterface
from app.storer import PageStorerInterface
from app.url_retriever import UrlRetrieverInterface


class OrchestratorConfig:
    def __init__(
            self,
            pages_retriever: UrlRetrieverInterface,
            page_extractor: PageExtractorInterface,
            page_storer: PageStorerInterface
    ):
        self.page_retriever = pages_retriever
        self.page_extractor = page_extractor
        self.page_storer = page_storer
