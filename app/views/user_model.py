from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.user import User

class UserModelView(ModelView):
    datamodel = SQLAInterface(User)
    