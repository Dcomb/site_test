import flask
from flask import Flask, render_template, redirect, jsonify

from . import db_session
from .games import Games

blueprint = flask.Blueprint(
    'games_api',
    __name__,
    template_folder='templates'
)

'''@blueprint.route('/game_check')
def get_news(game_name):
    db_sess = db_session.create_session()
    game = db_sess.query(Games).filter(Games.email == Games.email.data).first()
    if game:
        return redirect(f"/games/{game_name}")
    else:
        return redirect("/games")'''
