import os
from flask import Flask
from flask_wtf import CSRFProtect

def create_app(test_config=None, instance_path=None):
    # create and config the app
    app = Flask(__name__, instance_relative_config=True, instance_path=instance_path)
    app.config.from_mapping(
        SECRET_KEY='devtesthings',
        DATABASE=os.path.join(app.instance_path, 'imgwebapp.sqlite'),
        UPLOADED_PHOTOS_DEST='uploads',
        MAX_CONTENT_LENGTH = 1024 * 1024
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    try:
        os.makedirs(os.path.join(app.instance_path, app.config['UPLOADED_PHOTOS_DEST']))
    except OSError:
        pass

    csrf = CSRFProtect(app)
    
    from . import db
    db.init_app(app)

    from . import auth
    auth.bcrypt.init_app(app)
    app.register_blueprint(auth.bp)
    app.add_url_rule('/', endpoint='index')

    from . import image
    image.init_uploads(app)
    # configure_uploads(app,image.photos)
    app.register_blueprint(image.bp)
    app.add_url_rule('/gallery', endpoint='gallery')
    

    return app
