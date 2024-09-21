from app.articles.repository import ArticlesRepository
from app.articles.service import ArticlesService
from app.common.model import ConnectionInfo

articles_service = ArticlesService(
    data_layer_entrypoint=ArticlesRepository(
        ConnectionInfo(
            # TODO: Move all this to secret/env variable
            dbname="eunice",
            user="eunice",
            host="eunice_challenge_db",
            password="eunice",
            port=5432
        )
    )
)