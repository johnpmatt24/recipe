from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)  


class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_thirty = data["under_thirty"]
        self.date_made = data["date_made"]
        self.user_id = data["user_id"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('recipes_schema').query_db(query)
        # Create an empty list to append our instances
        recipes = []
        # Iterate over the db results and create instances
        for recipe in results:
            recipes.append( cls(recipe) )
        return recipes
    
    
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO recipes ( name , description, instructions , user_id, under_thirty, date_made,  created_at, updated_at ) VALUES ( %(name)s , %(description)s , %(instructions)s , %(user_id)s, %(under_thirty)s, %(date_made)s, NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('recipes_schema').query_db( query, data ) # returns an id

    @classmethod
    def get_recipe(cls, data):
        query = "SELECT * from recipes where id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return cls(results[0])


    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_thirty = %(under_thirty)s, date_made = %(date_made)s, created_at = NOW(), updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query, data)
        
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE from recipes where id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query, data)
    
    
    
    @staticmethod
    def valid(recipe):
        is_valid = True # we assume this is true
        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False
        if len(recipe["instructions"]) < 3:
            flash('Instructions must be at least 3 chracaters.')
            is_valid = False
        if recipe["under_thirty"] == None:
            flash('All areas must be filled.')
            is_valid = False
        if recipe["date_made"] == None:
            flash('All areas must be filled.')
            is_valid = False
        return is_valid