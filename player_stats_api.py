#!/usr/bin/env python

from flask import Flask, app, jsonify
from flask.ext import restful
from flask.ext.restful import Api, Resource, reqparse
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import connection


app = Flask(__name__)
api = restful.Api(app)

get_args = reqparse.RequestParser()
get_args.add_argument("team_id", type=str, location="args", required=False)
get_args.add_argument("player", type=str, location="args", required=False)
get_args.add_argument("sport_type", type=str, location="args", required=False)
get_args.add_argument("player_id", type=str, location="args", required=False)


class GetSquad(restful.Resource):

        def __init__(self):

                conn = connection.get_mongo_connection()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.player_stats = db.player_stats

        def get(self):
                
                args = get_args.parse_args()
                squad = list(self.player_stats.find({'team_id':args['team_id']},projection={'_id':False,'team_name':True,'team_id':True,'player':True,'player_id':True,'image':True}))
                
                return {'success':True,
                        'error':False,
                        'data':sorted(squad),
                        }

class GetPlayerStats(restful.Resource):

        def __init__(self):
                conn = connection.get_mongo_connection()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.player_stats = db.player_stats

        def get(self):

                teams_played_for = {}

                args = get_args.parse_args()

                if len(list(self.player_stats.find({'player_id':args['player_id']})))>1:
                    stats = list(self.player_stats.find({'player_id':args['player_id']},projection={'_id':False,'team_name':True,'player':True,'player_id':True,'image':True,'stats':True,'info':True}))
                    for stat in stats:
                        teams_played_for.setdefault('teams_played_for',[]).append(stat['team_name'])
        
                    stats[0].update(teams_played_for)
                    stats[0].pop('team_name')
                    stats = stats[0]
                else:
                    stats = list(self.player_stats.find({'player_id':args['player_id']},projection={'_id':False,'team_name':True,'player':True,'player_id':True,'image':True,'stats':True,'info':True}))
                    teams_played_for.setdefault('teams_played_for',[]).append(stats[0].pop('team_name'))
                    stats[0].update(teams_played_for)
                    stats = stats[0]

                return {'success':True,
                        'error':False,
                        'data':stats,
                        }

        


api.add_resource(GetSquad,'/get_team_squad')
api.add_resource(GetPlayerStats, '/get_player_stats')

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5400 , debug = True)
