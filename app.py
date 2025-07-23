from helpers.database import db
from helpers.application import app, api
from helpers.CORS import cors

from resources.IndexResource import IndexResource
from resources.InstituicaoResource import InstituicoesResource, InstituicaoResource
from resources.AlunoResource import AlunosResource

cors.init_app(app)

api.add_resource(IndexResource, '/')
api.add_resource(InstituicoesResource, '/instituicoes')
api.add_resource(InstituicaoResource, '/instituicoes/<int:id>')

api.add_resource(AlunosResource, '/instituicoes')


with app.app_context():
    db.create_all()
