from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from app.api.v1.services import facade
import jwt
from flask import current_app, request

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Model for token input
token_model = api.model('Token', {
    'token': fields.String(required=True, description='JWT token (without Bearer prefix)')
})

# Add token parameter to Swagger docs
token_param = api.parser()
token_param.add_argument('token', type=str, required=True, help='JWT token', location='query')

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload  # Get the email and password from the request payload

        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])

        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})

        # Step 4: Return the JWT token to the client
        return {'access_token': access_token}, 200

@api.route('/protected')
class ProtectedResource(Resource):
    @api.expect(token_param)
    @api.response(200, 'Valid token')
    @api.response(401, 'Invalid token')
    def get(self):
        """Protected endpoint that accepts a token as a query parameter"""
        token = request.args.get('token')

        if not token:
            return {'error': 'Token is required'}, 401

        try:
            # Manually decode token
            decoded_token = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=["HS256"]
            )

            # Extract user identity
            if isinstance(decoded_token['sub'], dict):
                user_id = decoded_token['sub']['id']
            else:
                user_id = decoded_token['sub']

            return {'message': f'Hello, user {user_id}'}, 200
        except Exception as e:
            return {'error': 'Invalid token'}, 401
