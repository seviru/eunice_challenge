import typer

from app.orchestration import ParserOrchestrator
from app.orchestration.factory import OrchestrationConfigFactory

app = typer.Typer()

@app.command()
def parse_last_news(
        amount: int = typer.Option(20, help="The number of last news to parse"),
        exclude: str = typer.Option("markets,learn,consensus-magazine", help="Categories to exclude")
) -> None:
    """
    Parses the last X amount of news from coindesk, excluding certain categories by default
    """
    # Convert the exclude string to a list of categories
    exclude_categories = [category.strip() for category in exclude.split(',')]

    # Placeholder for the code that does the parsing
    ParserOrchestrator.execute(
        OrchestrationConfigFactory.create_last_articles_config(
            number_of_articles=amount,
            exclude_categories=exclude_categories
        )
    )

if __name__ == "__main__":
    app()
