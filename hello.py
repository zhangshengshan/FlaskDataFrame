import pandas as pd
import json, redis
import numpy as np
import traceback

from flask import Flask
from flask import request
app = Flask(__name__)


@app.route("/", methods=['POST'])
def hello():
    try:
        resultDict = {}
        df = pd.read_excel("salesfunnel.xlsx")
        s=df.to_string
        parameter = request.data
        param_json = json.loads(parameter)
        print param_json["helloworld"]
        resultDict['data'] = param_json['helloworld'] 
        return json.dumps(resultDict)
    except:
        s = traceback.format_exc()
        print s
        return "error"

if __name__ == "__main__":
    
    app.run()
