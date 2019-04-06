from flask import Flask, Jsonify, request, render_template

app = Flask(__name__)

doners = [{
    'name': 'Jacklebees',
    'items': [{'name':'my item', 'price': 15.99 }]
}]

#Home route to "hello Earth"
@app.rount('/')
def home():
    return render_template('index.html')

#post /sotre data: {name :}
@app.route('/doner', method=['POST'])
def create_doner():
    request_data = request.get_json()
    new_doner = {
        'name':request_data['name'],
        'items':[]
                }
    doners.append(new_doner)
    return jsonify(new_doner)

# get /doners/<name> data: {name :}/
@app.route('/doner/<string:name>')
def get_doner(name):
    for doner in donres:
        if doner['name']== name:
            return jsonify(doner)
    return jsonify({'message': 'doner not found'})

#get /doner
@app.route('/doner')
def get_doners():
    return jsonify({'doners': doners})


#post /doners/<name> data: {name :}
@app.route('/doner/<string:name>/item' , methods=['POST'])
def create_items_from_doner(name):
  request_data = request.get_json()
  for doner in doners:
    if doner['name'] == name:
        new_item = {
            'name': request_data['name'],
            'quantity': request_data['quantity']
        }
        doner['items'].append(new_item)
        return jsonify(new_item)
  return jsonify ({'message' :'doner not found'})
  #pass

#get /doner/<name>/item data: {name :}
@app.route('/doner/<string:name>/item')
def get_donation_from_doner(name):
  for doner in doners:
    if doner['name'] == name:
        return jsonify( {'items':doner['items'] } )
  return jsonify ({'message':'doner not found'})




app.run(port=5000)
