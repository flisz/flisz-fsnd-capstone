from flask import redirect, url_for, flash, session, request, render_template, jsonify, current_app
from flask_login import login_user, logout_user, current_user, login_required

from project.setup.loggers import LOGGERS
from project.auth import requires_sign_in, AuthError
from project.models.base import ApiDatabaseError


class ApiError(Exception):
    """
    AuthError Exception
        A standardized way to communicate auth failure modes
    """
    def __init__(self, status_code, message):
        self.message = message
        self.status_code = status_code


def init_routes(app=None):
    """Initializes application route handlers."""
    if app is None:
        raise ValueError('cannot init views without app object')

    # Handle HTTP errors
    register_frontend_handlers(app)
    register_api_handlers(app)
    register_error_handlers(app)


def register_api_handlers(app=None):
    """Register app frontend handlers.

    Raises error if app is not provided.
    """
    if app is None:
        raise ValueError('cannot register error handlers on an empty app')


def register_frontend_handlers(app=None):
    """Register app frontend handlers.

    Raises error if app is not provided.
    """
    if app is None:
        raise ValueError('cannot register error handlers on an empty app')

    @app.route('/')
    def index():
        return render_template('pages/home.html', current_user=current_user, current_app=current_app)

    @app.route('/login')
    @app.route('/login/')
    def login():
        if current_user.is_anonymous:
            auth0_domain = current_app.config['SETUP'].AUTH0_DOMAIN
            api_audience = current_app.config['SETUP'].AUTH0_API_AUDIENCE
            client_id = current_app.config['SETUP'].AUTH0_CLIENT_ID
            callback_url = current_app.config['SETUP'].AUTH0_CALLBACK_URL

            link = f'https://{auth0_domain}/authorize' \
                   f'?audience={api_audience}' \
                   f'&response_type=token' \
                   f'&client_id={client_id}' \
                   f'&redirect_uri={callback_url}'
            return redirect(link)
        else:
            flash('I redirected over here')
            return redirect(url_for('index'))

    @app.route('/logout')
    @app.route('/logout/')
    @login_required
    def logout():
        LOGGERS.Login.debug(f'trying log out')
        logout_user()
        return render_template('pages/logout_callback.html')

    @app.route('/auth/callback')
    @app.route('/auth/callback/')
    def callback():
        LOGGERS.Login.debug(f'made it to the callback!')
        if current_user.is_anonymous:
            return render_template('pages/login_callback.html')
        else:
            LOGGERS.Login.debug(f'already logged in!')
            return redirect(url_for('index'))

    @app.route('/auth/finalize')
    @app.route('/auth/finalize/')
    @requires_sign_in
    def finalize(user=None):
        LOGGERS.Login.debug(f'made it to the finalizer!')
        flash('Login Successful!')
        return jsonify({'success': True,
                        'redirect_url': url_for('index')})


def register_error_handlers(app=None):
    """Register app error handlers.

    Raises error if app is not provided.
    """
    if app is None:
        raise ValueError('cannot register error handlers on an empty app')

    @app.errorhandler(ApiError)
    def api_error(e):
        data = {
            'success': False,
            'status_code': e.status_code,
            'message': e.message
        }
        return jsonify(json.dumps(data)), e.status_code

    @app.errorhandler(ApiDatabaseError)
    def api_database_error(e):
        data = {
            'success': False,
            'status_code': e.status_code,
            'message': e.message
        }
        return jsonify(json.dumps(data)), e.status_code

    @app.errorhandler(AuthError)
    def authorization_error(e):
        data = {
            'success': False,
            'status_code': e.status_code,
            'message': e.message
        }
        return jsonify(json.dumps(data)), e.status_code