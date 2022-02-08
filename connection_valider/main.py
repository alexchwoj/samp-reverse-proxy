from weakref import proxy
from xml.dom.domreg import registered
from flask import Flask, request, abort, jsonify

# Flask
app = Flask(__name__)
validator_key = 'Y$Lga#5p@ZPG8fex4rNVwuEQSFsvTRnWM+Hbm2KUByJk93tq7D'

# Register
registered_clients = {
    "4222222": {
        "address": "127.0.0.1:422",
        "payload": "12345898765432"
    }
}

registered_proxies = {
    "12345898765432": {
        "address": "127.0.0.1:422"
    }
}

@app.errorhandler(404)
@app.errorhandler(500)
def app_error(e):
	print(f'[Error] {e}')
	return '0'

@app.route('/proxy/register/player', methods = ['POST'])
def proxy_register_player():
    if not request.headers['Authorization'] == validator_key:
        abort(403, description = "Invalid secret key")
    
    content = request.get_json(silent = True)

    address_seed = content["payload"]
    registered_proxies[address_seed] = {'address': None}
    registered_proxies[address_seed]['address'] = content['address']

    print(f"[Validated player]: Address: {content['address']}, Payload: {content['payload']}")
    return jsonify({'message': 'ok'})

@app.route('/proxy/register/proxied_player', methods = ['POST'])
def proxy_register_proxied_player():
    if not request.headers['Authorization'] == validator_key:
        abort(403, description = "Invalid secret key")
    
    content = request.get_json(silent = True)

    address_seed = content["address"]
    registered_clients[address_seed] = {'address': None, 'payload': None}
    registered_clients[address_seed]['address'] = content['address']
    registered_clients[address_seed]['payload'] = content['payload']

    print(f"[Validated proxy]: Address: {content['address']}, Payload: {content['payload']}")
    return jsonify({'message': 'ok'})

@app.route('/address/real/<ip_address>', methods = ['GET'])
def address_real(ip_address):
    address_data = registered_clients.get(ip_address)
    if address_data:
        proxy_data = registered_proxies.get(address_data['payload'])
        if proxy_data:
            return proxy_data['address'].split(':')[0]

    return 'N'

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 60422, debug = False)