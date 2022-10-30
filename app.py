from flask import Flask,render_template,request,redirect
from models import db,UniformModel
 
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
 
@app.before_first_request
def create_table():
    db.create_all()
 
@app.route('/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
 
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
        return redirect('/')
 
 
@app.route('/')
def RetrieveList():
    uniforms = UniformModel.query.all()
    return render_template('datalist.html',uniforms = uniforms)
 
@app.route('/<int:id>/edit',methods = ['GET','POST'])
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
        return redirect('/')
        return f"Uniform with id = {id} Does nit exist"
 
    return render_template('update.html', uniform = uniform)
 
 
@app.route('/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    uniforms = UniformModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if uniforms:
            db.session.delete(uniforms)
            db.session.commit()
            return redirect('/')
            
     
    return render_template('delete.html')
 
app.run(host='localhost', port=5000)

