from app.extractor import PageExtractorInterface
from app.url_retriever import UrlRetrieverInterface
from app.storer import PageStorerInterface


class OrchestratorConfig:
    def __init__(
            self,
            pages_retriever: UrlRetrieverInterface,
            page_extractor: PageExtractorInterface,
            page_storer: PageStorerInterface
    ):
        self.page_retriever = pages_retriever,
        self.page_extractor = page_extractor,
        self.page_storer = page_storer


class ParserOrchestrator:
    @staticmethod
    def execute(orchestrator_configuration: OrchestratorConfig):
        urls = orchestrator_configuration.page_retriever.retrieve_pages()
        for url in urls:
            page = orchestrator_configuration.page_extractor.extract_page_data(url)
            orchestrator_configuration.page_storer.store_page(page)
