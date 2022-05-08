import os

from flask import Flask, url_for, request, render_template, session, redirect
import requests
import random

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='template')


@app.route('/', methods=['POST', 'GET'])
def form_sample():
    if request.method == 'GET':
        return render_template('anketa2.html')
    else:
        print(request.form.get(key='v'))
        if request.form.get(key='v') == 'Войти':

            return redirect("/v", code=302)
        else:
            return redirect("/reg", code=302)



@app.route('/v', methods = ['POST', 'GET'])
def v():
    if request.method == 'GET':
        return render_template('vhod.html')
    else:
        sp_itog = []
        sp = []
        all = User.query.all()
        for el in all:
            sp.append(el.number)
            sp.append(el.password)
            sp_itog.append(sp)
            sp = []
        num = request.form['number']
        pas = request.form['password']
        for i in range(len(sp_itog)):
            print('Правильный логин')
            if num == sp_itog[i][0]:
                if pas == sp_itog[i][1]:
                    session['vhod'] = 1
                    return redirect('/travel')

                else:
                    return redirect('/incorrect')
        return redirect('/notreg')
@app.route('/reg', methods = ['POST', 'GET'])
def reg():
    if request.method == 'GET':
        return render_template('reg.html')
    else:
        print(request.form['name'])
        user = User(name=request.form['name'], number=request.form['number'], password=request.form['password'])
        db.session.add(user)
        db.session.commit()
        print(User.query.filter(User.id).all())


        return redirect('/')

@app.route('/travel', methods = ['POST', 'GET'])
def travel():
    sp_travel = []
    sp = []
    sp_travel = []
    if session.get('vhod') == 1:
        if request.method == 'GET':
            all_travel = Travel.query.all()
            for el in all_travel:
                sp.append(el.id)
                sp.append(el.name)
                sp.append(el.opisanie[0:45])
                sp.append(el.opisanie)
                sp.append(el.data)
                sp.append(el.suit)
                sp.append(el.price)

                sp_travel.append(sp)
                sp = []

            return render_template('travel.html', sp_travel=sp_travel)
        else:
            print(request.form.get('create'))
            if request.form.get('create travel') == 'Создать свое путешествие':
                return render_template('create.html')

            if request.form.get('create') == 'Создать':
                print(request.form)
                travel = Travel(name=request.form['name'], opisanie=request.form['opisanie'], data=request.form['data'], suit=request.form['suit'], price=request.form['price'])
                db.session.add(travel)
                db.session.commit()
                return redirect('/travel')
    else:
        return "Вы не авторизованы"

@app.route('/<id>', methods = ['POST', 'GET'])
def id(id):
    sp = []
    sp_travel = []
    if request.method == 'GET':
        all_travel = Travel.query.all()
        for el in all_travel:
            if str(el.id) == id:
                print(el)
                name = el.name
                data = el.data
                opisanie = el.opisanie
                suit = el.suit
                price = el.price
                return render_template('podrobnee.html', el=opisanie, name=name, data=data, suit=suit, price=price)

@app.route('/incorrect', methods = ['POST', 'GET'])
def incor():
    if request.method == 'GET':
        return render_template('incorrect.html')
    else:
        return redirect('/')

@app.route('/notreg', methods = ['POST', 'GET'])
def notreg():
    if request.method == 'GET':
        return render_template('notreg.html')
    else:
        return redirect('/')

if __name__ == '__main__':
    app.secret_key = os.urandom(21)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///application.bd"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db = SQLAlchemy(app)
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(64), primary_key=False, nullable=False)
        number = db.Column(db.String(64), primary_key=False, nullable=False)
        password = db.Column(db.String(200), primary_key=False, nullable=False)

        def __repr__(self):
            return str(self.id) + ' ' + str(self.name) + ' ' + str(self.number) + ' ' + str(self.password)

    class Travel(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(64), primary_key=False, nullable=False)
        data = db.Column(db.String(64), primary_key=False, nullable=False)
        opisanie = db.Column(db.String(5000), primary_key=False, nullable=False)
        suit = db.Column(db.String(5000), primary_key=False, nullable=False)
        price = db.Column(db.String(5000), primary_key=False, nullable=False)

        def __repr__(self):
            return str(self.id) + ' ' + str(self.name) + ' ' + str(self.data) + ' ' + str(self.opisanie) + ' ' + str(self.suit) + ' ' + str(self.price)


    db.create_all()
    app.run(host='127.0.0.1')
