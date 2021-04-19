from flask import Flask, render_template,request,redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():

    app = Flask(__name__)

    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    #Init Plug-ins (SQL / Login)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth_bp.login'
    login_manager.init_app(app)


    @app.before_request
    def before_request():
        session.permanent = False
      

    with app.app_context():
        from . import auth
        from . import routes
        from .models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # Register Blueprints
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)

        db.create_all()

        #create admin upon app creation
        if User.query.all() == '' or User.query.all() == None:
            email = 'johncrowley547@gmail.com'
            name = 'admin'
            password = 'admin'
            admin = True
            our_admin = User(email=email,name=name,password=generate_password_hash(password, method='sha256'),admin=admin)
            db.session.add(our_admin)
            db.session.commit()

        return app