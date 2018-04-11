from flask import Blueprint
main = Blueprint('main', __name__)
 
import json
from engine import RecommendationEngine
 
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
from flask import Flask, request
 
@main.route("/<int:user_id>/ratings/top/<int:count>", methods=["GET"])
def top_ratings(user_id, count):
    logger.debug("User %s TOP ratings requested", user_id)
    top_ratings = recommendation_engine.get_top_ratings(user_id,count)
    return json.dumps(top_ratings)
 
@main.route("/<int:user_id>/ratings/<string:book_id>", methods=["GET"])
def book_ratings(user_id, book_id):
    logger.debug("User %s rating requested for book %s", user_id, book_id)
    hash_book_id = abs(hash(book_id)) % (10 ** 8)
    ratings = recommendation_engine.get_ratings_for_book_ids(user_id, [hash_book_id])
    return json.dumps(ratings)
 
 @main.route("/<int:num>/ratings", methods = ["POST"])
 def top_books(num):
     return []

 
@main.route("/<int:user_id>/ratings", methods = ["POST"])
def add_ratings(user_id):
    # get the ratings from the Flask POST request object
    ratings_list = request.form.keys()[0].strip().split("\n")
    ratings_list = map(lambda x: x.split(","), ratings_list)
    # create a list with the format required by the negine (user_id, book_id, rating)
    ratings = map(lambda x: (user_id, int(x[0]), float(x[1])), ratings_list)
    # add them to the model using then engine API
    recommendation_engine.add_ratings(ratings)
 
    return json.dumps(ratings)
 
 
def create_app(spark_context, dataset_path):
    global recommendation_engine 

    recommendation_engine = RecommendationEngine(spark_context, dataset_path)    
    
    app = Flask(__name__)
    app.register_blueprint(main)
    return app 
