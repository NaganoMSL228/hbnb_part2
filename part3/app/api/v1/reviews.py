from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @jwt_required()  # Add JWT requirement
    def post(self):
        """Register a new review"""
        review_data = api.payload
        current_user = get_jwt_identity()

        try:
            # Set the user_id to the current authenticated user
            review_data['user_id'] = current_user['id']

            # Get the place to check ownership
            place = facade.get_place(review_data['place_id'])
            if not place:
                return {'error': 'Place not found'}, 404

            # Check if the user owns the place
            if place.owner.id == current_user['id']:
                return {'error': 'You cannot review your own place'}, 400

            # Check if the user has already reviewed this place
            if facade.has_user_reviewed_place(current_user['id'], place.id):
                return {'error': 'You have already reviewed this place'}, 400

            # Create the review
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id,
                'place_id': new_review.place.id
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id} for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()  # Add JWT requirement
    def put(self, review_id):
        """Update a review's information (author or admin only)"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        review_data = api.payload

        try:
            # Get the review
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404

            # Check if current user is the author of the review or an admin
            if review.user.id != current_user['id'] and not is_admin:
                return {'error': 'Unauthorized action'}, 403

            # Update the review
            updated_review = facade.update_review(review_id, review_data)
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user.id,
                'place_id': updated_review.place.id
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()  # Add JWT requirement
    def delete(self, review_id):
        """Delete a review (author or admin only)"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)

        # Get the review
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # Check if current user is the author of the review or an admin
        if review.user.id != current_user['id'] and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        # Delete the review
        if facade.delete_review(review_id):
            return {'message': 'Review deleted successfully'}, 200
        return {'error': 'Review not found'}, 404

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [{'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user.id} for review in reviews], 200
        except ValueError as e:
            return {'error': str(e)}, 404