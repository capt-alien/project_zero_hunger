from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

doners = [{
    'name': 'Jacklebees',
    'items': [{'name':'my item', 'quantity': 22 }]
},
    {'name': 'Pizza_smut',
    'items': [{'name':'pizza', 'quantity': 3.14 }]
},
    {'name': 'McJackinthecrack',
    'items': [{'name':'cheezzeeburgerz', 'quantity': 500 }]
},
    {'name': 'burrito_joes',
    'items': [{'name':'taco', 'quantity': 42 }]
}
]

#Home route to "hello Earth"
@app.route('/')
def home():
    return render_template('index.html', token='Flask + React')

#post /sotre data:d {name :}
@app.route('/doner', methods=['POST'])
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
    for doner in doners:
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


if __name__ == '__main__':
    app.run(port=5000, debug=True)
