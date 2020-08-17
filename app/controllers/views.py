from flask.views import View

auth_blueprint = Blueprint('auth', __name__, url_prefix="/auth")

class RenderTemplate(View):
    
    def render_register(self):
        return render_template('auth/register.html')
    

register_render_view = RenderTemplate.as_view('register_render')

auth_blueprint.add_url_rule('/users/', view_func= register_render_view)

# auth_blueprint.add_url_rule(
#     '/register',
#     view_func=registration_view,
#     methods=['POST', 'GET']
# )