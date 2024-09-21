from app.storer.storer_interface import PageStorerInterface
from app.storer.coindesk_page_storer import CoindeskPageStorer, ConnectionInfo

coindesk_page_storer = CoindeskPageStorer(
    ConnectionInfo(
        # TODO: Move all this to secret/env variable
        dbname="eunice",
        user="eunice",
        host="eunice_challenge_db",
        password="eunice",
        port=5432
    )
)
