from flask import jsonify, Blueprint, url_for
from flask_restful import (Resource, Api, reqparse,
                           marshal_with, marshal, inputs, fields, abort)
import models

review_fields = {
    "id": fields.Integer,
    "for_course": fields.String,
    "rating": fields.String,
    "comment": fields.String(default=""),
    "created_at": fields.DateTime
}


def add_course(review):
    review.for_course = url_for('resources.courses.course', id=review.course.id)


def review_or_404(id):
    try:
        review = models.Review.get(models.Review.id == id)
    except models.Review.DoesNotExist:
        abort(404)
    else:
        return review


class ReviewList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'course',
            required=True,
            location=['form', 'json'],
            help="no course provided",
            type=inputs.positive
        )
        self.reqparse.add_argument(
            'rating',
            required=True,
            location=['form', 'json'],
            help="no rating provided",
            type=inputs.int_range(1, 5)
        )
        self.reqparse.add_argument(
            'comment',
            required=False,
            nullable=True,
            location=['form', 'json'],
            default=""
        )
        super().__init__()

    def get(self):
        reviews = [marshal(add_course(reviews),review_fields)
                   for reviews in models.Review.select()]
        return {"reviews": reviews}

    def post(self):
        args = self.reqparse.parse_args()
        review = models.Review.create(**args)
        return add_course(review)


class Review(Resource):
    marshal_with(review_fields)

    def get(self, id):
        return add_course(review_or_404(id))

    def put(self, id):
        return jsonify({"course": 1, "rating": 5})

    def delete(self, id):
        return jsonify({"course": 1, "rating": 5})


reviews_api = Blueprint("resources.reviews", __name__)
api = Api(reviews_api)
api.add_resource(
    ReviewList,
    '/reviews',
    endpoint="reviews"
)
api.add_resource(
    Review,
    '/reviews/<int:id>',
    endpoint="review"
)

