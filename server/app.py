#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = [article.to_dict() for article in Article.query.all()]
    return make_response(articles, 200)

@app.route('/articles/<int:id>', methods=['GET'])
def show_article(id):
    # Initialize page_views in session
   
    session["page_views"] = session.get("page_views", 0) + 1  #This line is trying to tell us this: session['page_views'] = session['page_views'] if 'page_views' in session else 0. It is considrered a ternary operation. This line checks if 'page_views' exists in session. If it does, it uses that value; if not, it sets it to 0.So, while session.get('page_views', 0) isn’t technically a ternary operator, it serves a similar purpose of providing a default value when the key is not found. The plus one is allowing us to increment the view count right after fetching it from the session.


    # Check if user exceeded the limit
    if session["page_views"] > 3:
        return jsonify({"message": "Maximum pageview limit reached"}), 401

    article = Article.query.filter_by(id=id).first()
    if article:
        return make_response(article.to_dict(), 200)
    else:
        return jsonify({"message": "Article not found"}), 404 #in case the article does not exist

if __name__ == '__main__':
    app.run(port=5555)
