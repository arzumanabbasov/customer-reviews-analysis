import json
import pandas as pd
from flask import Flask, jsonify
from utils.features.feature_engineering import FeatureEngineering
from utils.models.model import Modeling
from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

conn = mysql.connector.connect(host='',
                               user='',
                               password='',
                               database='',
                               ssl_ca='',
                               ssl_verify_identity=True,
                               )

cursor = conn.cursor()
cursor.execute("SET SESSION MAX_EXECUTION_TIME=50")

app = Flask(__name__)


class App:
    def __init__(self):
        self.df = FeatureEngineering(
            connection=conn,
            QUERY="SELECT * FROM reviews_test;"
        ).run()
        self.modeling = Modeling(
            df=self.df
        )

    def run(self):
        return self.modeling.run()


app_instance = App()


@app.route('/')
def index():
    df = app_instance.run()

    flat_df = df.drop(columns=['text']).join(df['text'].apply(lambda x:
                                                              pd.Series(app_instance.modeling.apply_vader(
                                                                  pd.Series([x]))[0])))

    json_data = json.loads(flat_df.to_json(orient='records'))
    return jsonify(json_data)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))

    is_prod = os.environ.get('RAILWAY_ENVIRONMENT_NAME') is not None

    app.run(host='0.0.0.0', port=port, debug=not is_prod)
