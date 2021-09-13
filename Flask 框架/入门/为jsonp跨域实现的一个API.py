import json

from flask import Flask, request

app = Flask(__name__)


@app.route('/jsonp', methods=['GET'])
def index():
    func = request.args.get('callback')
    flight_name = request.args.get('code')

    # 航班信息
    flight = {
        "CA199202": {
            'price': 1200,
            'tickets': 37
        },
        "SA6532K": {
            'price': 900,
            'tickets': 60
        }
    }

    if flight.get(flight_name):
        # 以json字符串形式返回js脚本
        return func + "(" + json.dumps(flight.get(flight_name)) + ")"
    else:
        return func + "('无航班信息')"


if __name__ == '__main__':
    app.run()
