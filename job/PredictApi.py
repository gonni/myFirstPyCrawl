from flask import Flask
from flask_restx import Api, Resource
import ml.KosdaPredictPycaret as kpp

app = Flask(__name__)
api = Api(app)


@api.route('/hell')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@api.route('/predKosdaq')
class PredictKosdaq(Resource):
    def get(self):
        res = kpp.predict()
        pred = float(res['prediction_label'].iloc[0])
        return {'kosdaq3d': pred }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8088)