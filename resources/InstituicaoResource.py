from flask_restful import Resource
from helpers.logging import logger


class InstituicoesResource(Resource):
    def get(self):
        logger.info("Get - Instituições")

    def post(self):
        logger.info("Post - Instituição")


class InstituicaoResource(Resource):
    def get(self, id):
        logger.info("Get por id- Instituições")

    def put(self, id):
        pass

    def delete(self, id):
        pass
