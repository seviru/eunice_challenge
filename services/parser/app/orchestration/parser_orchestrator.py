from app.orchestration import OrchestratorConfig


class ParserOrchestrator:
    @staticmethod
    def execute(orchestrator_configuration: OrchestratorConfig):
        urls = orchestrator_configuration.page_retriever.retrieve_urls()
        for url in urls:
            page = orchestrator_configuration.page_extractor.extract_page_info(url)
            orchestrator_configuration.page_storer.store_page(page)
