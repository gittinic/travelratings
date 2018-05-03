import json
from flask import Flask
from flask_restful import Resource, Api, request, abort
import numpy as np

# Get country list

# Generate dictionary
feedback_db = dict((score, {}) for score in ['Affordability', 'Safety', 'Tourism'])


# API
userFeedback = Flask(__name__)
api = Api(userFeedback)



def abort_if_not_exist(score: str, country: str):
    if get_country_user_feedback(score, country) is None:
        abort(404, message="Journal entry {} doesn't exist".format(score, country))


def get_country_user_feedback(score: str, country: str):
    return feedback_db[score][country]


# def get_country_user_feedback_average(score: str, country: str):
#     feedback = get_country_user_feedback(score, country)
#     return np.mean(feedback).round(1)
#
#
# def get_country_user_feedback_total(country: str):
#     feedback_affordability = get_country_user_feedback_average('Affordability', country)
#     feedback_safety = get_country_user_feedback_average('Safety', country)
#     feedback_tourism = get_country_user_feedback_average('Tourism', country)
#     return np.sum([feedback_affordability, feedback_safety, feedback_tourism])


def add_user_feedback(score: str, country: str, value):
    feedback_db[score].setdefault(country, []).append(float(value))
    return feedback_db[score][country]


class FeedbackList(Resource):
    def get(self):
        return feedback_db


class Feedback(Resource):
    def get(self, score: str, country: str):
        abort_if_not_exist(score, country)
        fb = get_country_user_feedback(score, country)
        return fb, 200

    def put(self, score: str, country: str):
        # abort_if_not_exist(score, country)
        value = request.form['value']
        new_fb = add_user_feedback(score, country, value)
        return new_fb, 200

api.add_resource(FeedbackList, '/feedback')
api.add_resource(Feedback, '/feedback/<score>/<country>')

userFeedback.run()

