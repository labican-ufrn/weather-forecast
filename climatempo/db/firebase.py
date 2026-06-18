import os
import json
import firebase_admin
from firebase_admin import credentials, db

class BancoFirebase:
    def __init__(self, caminho_credenciais=None, url_banco=None):
        self.caminho_credenciais = caminho_credenciais or os.environ.get("FIREBASE_CREDENCIAIS")
        self.credenciais_json = os.environ.get("FIREBASE_CREDENCIAIS_JSON")
        self.url_banco = url_banco or os.environ.get("FIREBASE_URL")
        self._inicializado = False

    def inicializar(self):
        if self._inicializado:
            return

        if (not self.caminho_credenciais and not self.credenciais_json) or not self.url_banco:
            raise ValueError(
                "Defina FIREBASE_URL e uma credencial: FIREBASE_CREDENCIAIS (arquivo) "
                "ou FIREBASE_CREDENCIAIS_JSON (conteudo JSON)"
            )

        if not firebase_admin._apps:
            if self.credenciais_json:
                cred = credentials.Certificate(json.loads(self.credenciais_json))
            else:
                cred = credentials.Certificate(self.caminho_credenciais)
            firebase_admin.initialize_app(cred, {"databaseURL": self.url_banco})
        self._db = db
        self._inicializado = True

    def definir(self, caminho, dados):
        self.inicializar()
        ref = self._db.reference(caminho)
        ref.set(dados)

    def inserir(self, caminho, dados):
        self.inicializar()
        ref = self._db.reference(caminho)
        return ref.push(dados)

    def obter(self, caminho):
        self.inicializar()
        ref = self._db.reference(caminho)
        return ref.get()

    def deletar(self, caminho):
        self.inicializar()
        ref = self._db.reference(caminho)
        ref.delete()
