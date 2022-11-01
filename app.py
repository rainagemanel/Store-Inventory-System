from flask import Flask,render_template,request,redirect,session,g,url_for
from models import db,UniformModel


import os


app = Flask(__name__, template_folder='./templates',static_url_path='', static_folder='./static')

app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
 
@app.before_first_request
def create_table():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)

        if request.form['password'] == 'password':
            session['user'] = request.form['username']
            return redirect(url_for('protected'))

    return render_template(login.html)


@app.route("/index")
def index():
    if g.user:
        return render_template('index.html',user=session['user'])
    return redirect(url_for('login'))

@app.route("/about")
def about():
    if g.user:
        return render_template('about.html',user=session['user'])
    return redirect(url_for('login'))

@app.route('/create' , methods = ['GET','POST'])
def create():
    if g.user:
        return render_template('create.html',user=session['user'])
    
    if request.method == 'GET':
        return render_template('create.html')
 
    if request.method == 'POST':
        dep_name = request.form['dep_name']
        course_name = request.form['course_name']
        type = request.form['type']
        stock = request.form['stock']
        sizes = request.form['sizes']
        
        uniforms = UniformModel(
            dep_name=dep_name,
            course_name=course_name,
            type=type,
            stock=stock,
            sizes = sizes
        )
        db.session.add(uniforms)
        db.session.commit()
        return redirect('/index')
    return redirect(url_for('login'))
 
@app.route('/datalist')
def RetrieveList():
    uniforms = UniformModel.query.all()
    if g.user:
        return render_template('datalist.html',user=session['user'],uniforms = uniforms)
    return redirect(url_for('login'))
    
@app.route('/<int:id>/edit', methods = ['GET','POST'])
def update(id):
    uniform = UniformModel.query.filter_by(id=id).first()

    if request.method == 'POST':
        if uniform:
            db.session.delete(uniform)
            db.session.commit()

        dep_name = request.form['dep_name']
        course_name = request.form['course_name']
        type = request.form['type']
        stock = request.form['stock']
        sizes = request.form['sizes']

        uniform = UniformModel(
            dep_name=dep_name,
            course_name=course_name,
            type=type,
            stock=stock,
            sizes=sizes
        )
        db.session.add(uniform)
        db.session.commit()
        return redirect('/index')
 
    return render_template('update.html', uniform = uniform)
 
 
@app.route('/<int:id>/delete', methods=['GET','POST'])
def delete(id):

    uniforms = UniformModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if uniforms:
            db.session.delete(uniforms)
            db.session.commit()
            return redirect('/index')
            
    return render_template('delete.html')
 
if __name__ == '__main__':
    app.run(debug=True, port=8000)

