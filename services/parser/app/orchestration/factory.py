from app.extractor import CoindeskExtractor
from app.orchestration import OrchestratorConfig
from app.storer import coindesk_page_storer
from app.url_retriever import LastCoindeskArticlesRetriever


class OrchestrationConfigFactory:
    @staticmethod
    def create_last_articles_config(number_of_articles: int, exclude_categories: list[str]) -> OrchestratorConfig:
        return OrchestratorConfig(
            pages_retriever=LastCoindeskArticlesRetriever(
                number_of_articles=number_of_articles,
                exclude_categories=exclude_categories
            ),
            page_extractor=CoindeskExtractor(),
            page_storer=coindesk_page_storer,
        )