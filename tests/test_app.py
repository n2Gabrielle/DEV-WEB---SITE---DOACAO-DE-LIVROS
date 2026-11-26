import tempfile
import unittest
from pathlib import Path

from app import create_app
from extensions import db
from models import Doador, Livro, SolicitacaoDoacao


class DonationAppTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_uri = f"sqlite:///{Path(self.temp_dir.name) / 'test.db'}"
        self.config = {
            "TESTING": True,
            "SECRET_KEY": "test-key",
            "SQLALCHEMY_DATABASE_URI": self.database_uri,
        }
        self.app = create_app(self.config)
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_application_has_at_least_five_routes(self):
        rules = {
            rule.rule
            for rule in self.app.url_map.iter_rules()
            if rule.endpoint != "static"
        }
        self.assertGreaterEqual(len(rules), 5)

    def test_donation_persists_after_recreating_the_app(self):
        response = self.client.post(
            "/doar",
            data={
                "titulo": "A cidade e as serras",
                "autor": "Eça de Queirós",
                "categoria": "Romance",
                "nome": "Ana Leitura",
                "email": "ana@example.com",
                "telefone": "",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        restarted_app = create_app(self.config)
        response_after_restart = restarted_app.test_client().get("/livros")
        self.assertIn("A cidade e as serras".encode(), response_after_restart.data)

    def test_request_is_persisted_and_book_is_no_longer_listed_as_available(self):
        with self.app.app_context():
            donor = Doador(nome="Pessoa doadora", email="doadora@example.com")
            book = Livro(
                titulo="Livro de teste",
                autor="Autora",
                categoria="Ficção",
                doador=donor,
            )
            db.session.add_all([donor, book])
            db.session.commit()
            book_id = book.id

        response = self.client.post(
            f"/livros/{book_id}/solicitar",
            data={
                "nome": "Pessoa leitora",
                "email": "leitora@example.com",
                "mensagem": "Tenho interesse.",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            self.assertEqual(SolicitacaoDoacao.query.count(), 1)
            self.assertEqual(db.session.get(Livro, book_id).status, "solicitado")

        response = self.client.get("/livros")
        self.assertNotIn("Livro de teste".encode(), response.data)


if __name__ == "__main__":
    unittest.main()
