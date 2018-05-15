from flask import Blueprint
main = Blueprint('main', __name__)
 
import json
import logging
import cherrypy
from engine import RecommendationEngine
from dao import Dao
from flask import Flask, request, Response
import cherrypy_cors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, POST, HEAD, PUT, DELETE"


cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)

 
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


@main.route("/login/<int:user_id>", methods=["POST"])
def login(user_id):
    enablecors()
    return 'abc'
    # return dbdao.login(user_id)


@main.route("/logout", methods=["POST"])
def logout():
    guid=request.cookies.get('guid')
    if guid is None:
        return -1
    else:
        return dbdao.logout(guid)


@main.route('/top_books/<int:num>', methods=['GET'])
def topbooks(num):
    return dbdao.get_top_books(num)

@main.route('/top_tags/<int:num>',methods=['GET'])
def toptags(num):
    return dbdao.get_top_tags(num)
 
@main.route('/top_tag_books/<int:tagid>/<int:num>',methods=['GET'])
def toptagbooks(tagid, num):
    return dbdao.get_top_tag_books(tagid,num)

def enablecors():
    cherrypy.response.headers["Content-Type"] = "application/javascript"
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, POST, HEAD, PUT, DELETE"

def create_app(spark_context, dataset_path):
    cherrypy_cors.install()
    global recommendation_engine,dbdao
    # recommendation_engine = RecommendationEngine(spark_context, dataset_path)    
    app = Flask(__name__)
    app.register_blueprint(main)
    dbdao=Dao()
    return app 
