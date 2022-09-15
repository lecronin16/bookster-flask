from flask import Blueprint, request
from ..apiauthhelper import token_required
from app.models import Book, Review, User, db
from flask_login import current_user
from sqlalchemy import func

shelf = Blueprint('shelf', __name__, template_folder='shelftemplates')
reviews = Blueprint('reviews', __name__, template_folder='reviewtemplates')

@reviews.route('/api/reviews')
def getAllreviewsAPI():
        reviews = Review.query.order_by(Review.date_reviewed.desc())
        all_reviews = [r.to_dict() for r in reviews]
        return {'status': 'ok', "reviews": all_reviews}


@reviews.route('/api/reviews/good')
def getGoodReviewsAPI():
        reviews = Review.query.order_by(Review.rating_value.desc())
        all_reviews = [r.to_dict() for r in reviews]
        return {'status': 'ok', "reviews": all_reviews}

# @reviews.route('/api/reviews/high')
# def getGoodReviewsAPI():
#         reviews = db.session.query(func.max(Review.rating_value))
#         goodReviews = reviews
#         returnReviews = [r.to_dict() for r in goodReviews]
#         return {'status': 'ok', "reviews": goodReviews}
#         return reviews

@reviews.route('/api/reviews/<int:review_id>')
def getSinglereviewsAPI(review_id):
    review = Review.query.filter_by(review_id=review_id)
    if review:
        return {
            'status': 'ok',
            'total_results': 1,
            "review": review.to_dict()
            }
    else:
        return {
            'status': 'not ok',
            'message': f"A review with the id : {id} does not exist."
        }


@reviews.route('/api/reviews/create', methods=["POST"])
@token_required
def createReviewAPI(user):
    data = request.json

    title = data['title']
    img_url = data['imgUrl']
    review_capt = data['reviewCapt']
    rating_value = data['ratingValue']

    review = Review(title, img_url, review_capt, rating_value, user.id)
    review.save()

    return {
        'status': 'ok',
        'message': "review was successfully created."
    }

@reviews.route('/api/reviews/update', methods=["POST"])
@token_required
def updateReviewAPI(user):
    data = request.json 

    review_id = data['reviewId']

    review = Review.query.get(review_id)
    if Review.user_id != user.id:
        return {
            'status': 'not ok',
            'message': "You cannot update another user's review!"
        }

    title = data['title']
    review_capt = data['reviewCapt']
    img_url = data['imgUrl']
    rating_value = data['ratingValue']

    review.updatereviewInfo(title, img_url, review_capt, rating_value)
    review.saveUpdates()

    return {
        'status': 'ok',
        'message': "review was successfully updated."
    }

# @reviews.route('/api/follow/<int:user_id>')
# @token_required
# def followUser(user_id):
#     user = User.query.get(user_id)
#     current_user.follow(user)

# @reviews.route('/api/unfollow/<int:user_id>')
# @token_required
# def unfollowUser(user_id):
#     user = User.query.get(user_id)
#     current_user.unfollow(user)


@shelf.route('/api/shelf/create', methods=["POST"])
@token_required
def addBookAPI(user):
    data = request.json

    title = data['title']
    # author = data['author']
    img_url = data['imgUrl']
    shelf = data['shelf']

    shelf = Book(title, img_url, shelf, user.id)
    shelf.save()

    return {
        'status': 'ok',
        'message': "shelf was successfully created."
    }

@shelf.route('/api/shelf/<int:user_id>')
def getShelfAPI(user_id):
        shelf = Book.query.filter_by(user_id = user_id)
        my_shelf = [s.to_dict() for s in shelf]
        return {'status': 'ok', 'shelf': my_shelf}

@reviews.route('/api/reviews/user/<int:user_id>')
def getMyReviewsAPI(user_id):
        new_reviews = Review.query.filter_by(user_id = user_id)
        my_reviews = [r.to_dict() for r in new_reviews]
        return {'status': 'ok', 'reviews': my_reviews}

