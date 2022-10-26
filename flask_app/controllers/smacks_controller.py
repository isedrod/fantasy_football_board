from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.smack_model import Smack

@app.route('/smacks')
def display_smacks():
    if 'email' not in session:
        return redirect('/')
    list_smacks = Smack.get_all_with_users()
    return render_template( 'smacks.html', list_smacks = list_smacks )

@app.route( '/smack/new')
def display_create_smack():
    if 'email' not in session:
        return redirect('/')
    return render_template( "create_smack.html" )

@app.route ( '/smack/create', methods = ['POST'] )
def create_smack():
    if Smack.validate_smack( request.form) == False:
        return redirect ('/smack/new')

    data = {
        **request.form,
        "user_id": session ['user_id']
    }
    Smack.create(data)
    return redirect( '/smacks' )


@app.route( '/smacks/<int:id>')
def display_one(id):
    if 'email' not in session:
        return redirect('/')
    data = {
        "id" : id
    }
    current_smack = Smack.get_one_with_user(data)
    return render_template("smack.html", current_smack = current_smack)

@app.route( '/smacks/<int:id>/update')
def display_update_smack(id):
    if 'email' not in session:
        return redirect('/')
    data = {
        "id" : id
    }
    current_smack = Smack.get_one_with_user(data)
    return render_template("update_smack.html", current_smack = current_smack)

@app.route('/smack/update/<int:id>', methods = ['POST'])
def update_smack (id):
    if Smack.validate_smack( request.form) == False:
        return redirect (f'/smacks/{id}/update')
    smack_data ={
        **request.form,
        "id" : id
    }
    Smack.update_one(smack_data)
    return redirect('/smacks')


@app.route('/smacks/<int:id>/delete')
def delete_smack(id):
    data ={
        "id" : id
    }
    Smack.delete_one(data)
    return redirect('/smacks')