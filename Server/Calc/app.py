from flask import Blueprint
from flask_cors import CORS
main = Blueprint('main', __name__)
 
import json
import logging
import cherrypy
from engine import RecommendationEngine
from dao import Dao
from flask import Flask, request, Response
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@main.route("/ratings/top/<int:user_id>/<int:count>", methods=["GET"])
def top_ratings(user_id, count):
    rediskey='toprating_{0}_{1}'.format(user_id,count)
    cached=dbdao.get_redis(rediskey)
    if cached==None or cached=='':
        logger.debug("User %s TOP ratings requested", user_id)
        top_ratings = recommendation_engine.get_top_ratings(user_id,count)
        dbdao.set_redis(top_ratings)
        # strnames="'"+"','".join(list( map(lambda x: x['Title'], top_ratings)))+"'"
        # logger.debug(strnames)
        # result = dbdao.get_booksbyname(strnames)
        cached = json.dumps(top_ratings)
    return cached
    


@main.route("/ratings/<int:user_id>/<string:book_id>", methods=["GET"])
def book_ratings(user_id, book_id):
    logger.debug("User %s rating requested for book %s", user_id, book_id)
    rediskey = 'bookratings_{0}_{1}'.format(user_id, book_id)
    cached = dbdao.get_redis(rediskey)
    if cached == None or cached == '':
        hash_book_id = map(lambda x:  abs(hash(x)) % (10 ** 8), book_id.split(','))
        ratings = recommendation_engine.get_ratings_for_book_ids(user_id, hash_book_id)        
        dbdao.set_redis(ratings)
        cached = json.dumps(ratings)
    return cached


@main.route("/addratings/<int:user_id>", methods=["POST"])
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
    return dbdao.login(user_id)


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


@main.route('/top_user_books/<int:userid>/<int:num>', methods=['GET'])
def topuserbooks(userid, num):
    return dbdao.get_top_user_books(userid, num)

def create_app(spark_context, dataset_path):
    global recommendation_engine,dbdao
    recommendation_engine = RecommendationEngine(spark_context, dataset_path)    
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(main)
    dbdao=Dao()
    return app 
