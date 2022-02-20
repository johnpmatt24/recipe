from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import user, recipe
from flask_app.controllers import users


@app.route("/create")
def create():
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id": session["user_id"]
    }
    return render_template("create.html")






@app.route("/create_recipe", methods = ["POST"])
def create_recipe():
    if "user_id" not in session:
        return redirect("/logout")
    
    if not recipe.Recipe.valid(request.form):
        return redirect('/create')
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "under_thirty" : request.form["under_thirty"],
        "date_made" : request.form["date_made"],
        "user_id": session["user_id"],    # when creating we need the foreign key. that foreing key will be the person in session
    }
    recipe.Recipe.save(data)
    return redirect("/dashboard")



@app.route("/update", methods = ["POST"])
def update_recipe():
    if "user_id" not in session:
        return redirect("/logout")
    
    if not recipe.Recipe.valid(request.form):
        return redirect('/create')
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "under_thirty" : request.form["under_thirty"],
        "date_made" : request.form["date_made"],
        "id": request.form["id"]    # when updating, we update based on id. This id represents the hidden input
    }
    
    recipe.Recipe.update_recipe(data)
    return redirect("/dashboard")



@app.route("/recipe/edit/<int:id>")
def edit_recipe(id):
    if "user_id" not in session:
        return redirect("/logout")
    
    data = {
        "id": id
    }
    
    user_data = {
        "id": session["user_id"]   # getting user based on the person in session/logged in
    }
    
    return render_template("edit.html", recipe = recipe.Recipe.get_recipe(data), user = user.User.get_user(user_data))



@app.route("/recipe/view/<int:id>")
def view_recipe(id):
    
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id": id
    }
    
    user_data = {
        "id": session["user_id"]
    }
    
    
    
    return render_template("view.html",  recipe = recipe.Recipe.get_recipe(data), user = user.User.get_user(user_data))



@app.route("/recipe/delete/<int:id>")
def delete_recipe(id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id" : id
    }
    recipe.Recipe.delete_recipe(data)
    return redirect("/dashboard")
