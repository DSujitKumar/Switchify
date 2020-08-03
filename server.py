from flask import Flask
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask import request,jsonify
from werkzeug.security import generate_password_hash,check_password_hash


app = Flask(__name__)
app.secret_key='Secretkey'

app.config['MONGO_DBNAME'] = 'MongoDBClient'
app.config['MONGO_URI'] = 'mongodb+srv://MongoDB:MongoDB@mongodbclient.ffcqc.mongodb.net/Sujit?retryWrites=true&w=majority'
mongo = PyMongo(app)

@app.route('/add', methods=['POST'])
def add_Switch():
    _json=request.json
    _phone=_json['phone']
    _name=_json['name']
    _desc=_json['desc']
    if _name and _phone and request.method=='POST':
        switch = mongo.db.switch
        id=switch.insert_one({'phone':_phone,'name':_name,'desc':_desc})
        res=jsonify('Key Added Sucessfully.')
        res.status_code=200
        return res
    else:
        return not_found()
@app.errorhandler(404)
def not_found(error=None):
    message ={
        'Status':404,
        'Message':'Not found '+request.url
    }
    resp=jsonify(message)
    resp.status_code=404
    return resp
@app.route('/switch/<phone>')
def findswitch(phone):
    switch = mongo.db.switch.find({'phone':phone})
    resp=dumps(switch)
    return resp

@app.route('/switchId/<id>')
def findswitchId(id):
    switch = mongo.db.switch.find_one({'_id':ObjectId(id)})
    resp=dumps(switch)
    return resp

@app.route('/deleteswitch/<id>',methods=['DELETE'])
def Delete_Switch(id):
    mongo.db.switch.delete_one({'_id':ObjectId(id)})
    resp=jsonify('Switch Deleted Successfully..')
    resp.status_code=200
    return resp

@app.route('/update/<id>',methods=['PUT'])
def update_switch(id):
    _id=id
    _json=request.json
    _name=_json['name']
    _desc=_json['desc']
    _phone=_json['phone']
    if _phone and _name and _id and request.method =='PUT':
        # r=mongo.db.switch.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':_name,'phone':_phone,'desc':_desc}})
        # print(r)
        new_val={'name':_name,'phone':_phone,'desc':_desc}
        mongo.db.switch.update_one({"_id" : ObjectId(id)},{'$set':new_val},upsert=True)
        resp=jsonify('Switch is updated')
        resp.status_code=200
        return resp
    else:
        return not_found
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)