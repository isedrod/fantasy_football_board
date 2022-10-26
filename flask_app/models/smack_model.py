from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE
from flask_app.models.user_model import User

class Smack:
    def __init__( self , data ):
        self.id = data['id']
        self.playing_against = data ['playing_against']
        self.week = data['week']
        self.bet = data['bet']
        self.winning_by = data['winning_by']
        self.smack = data['smack']
        self.gif_or_photo = data['gif_or_photo']
        self.user_id = data['user_id']
        self.created_at = data ['updated_at']
        self.updated_at = data ['updated_at']

    @classmethod
    def create (cls, data ):
        query = " INSERT INTO smacks ( playing_against, week, bet, winning_by, smack, gif_or_photo, user_id ) "
        query += " VALUES( %(playing_against)s, %(week)s, %(bet)s, %(winning_by)s, %(smack)s, %(gif_or_photo)s, %(user_id)s ); "
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def get_all_with_users( cls ):
        query = " SELECT * "
        query += " FROM smacks "
        query += " JOIN users ON smacks.user_id = users.id;"

        results = connectToMySQL(DATABASE).query_db(query)

        list_smacks = []

        for row in results:
            current_smack = cls ( row )
            user_data = {
                **row,
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at'],
                "id" : row['users.id']
            }
            current_user = User( user_data )
            current_smack.user = current_user
            list_smacks.append( current_smack )
        return list_smacks

    @classmethod
    def get_one_with_user (cls, data):
        query = " SELECT * "
        query += " FROM smacks "
        query += " JOIN users ON smacks.user_id = users.id "
        query += " WHERE smacks.id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db( query, data)

        if len( result ) > 0:
            current_smack = cls( result [0])
            user_data = {
                **result[0],
                "created_at" : result[0]['users.created_at'],
                "updated_at" : result[0]['users.updated_at'],
                "id" : result[0]['users.id']
            }
            current_smack.user = User ( user_data )
            return current_smack
        else:
            return None

    @classmethod
    def update_one(cls, data):
        query = "UPDATE smacks "
        query += "SET playing_against = %(playing_against)s, week = %(week)s, bet = %(bet)s, "
        query += "winning_by = %(winning_by)s, smack = %(smack)s, gif_or_photo = %(gif_or_photo)s"
        query += "WHERE id = %(id)s; "
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def delete_one(cls,data):
        query = "DELETE FROM smacks "
        query += "WHERE id = %(id)s; "
        return connectToMySQL(DATABASE).query_db(query,data)

# VALIDATE
    @staticmethod
    def validate_smack(data):
        is_valid = True
        if data ['playing_against'] == "":
            flash ( "Playing Against must not be empty", "error_smack_playing_against")
            is_valid = False
        if data ['week'] == "":
            flash ( "What happened must not be empty", "error_smack_week")
            is_valid = False
        # if data ['bet'] == "":
        #     flash ( "Date of smack must not be empty", "error_smack_bet")
            is_valid = False
        # if len(data['playing_against']) < 3:
        #     flash("Playing Against must be at least 2 characters long", "error_smack_playing_against")
            is_valid = False
        # if len(data['week']) < 3:
        #     flash("What happened must be at least 3 characters long", "error_smack_week")
            is_valid = False


        return is_valid