import pandas as pd
import json, redis
import numpy as np
import traceback
from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/get", methods=['GET'])
def get():
    return open("static/hello.csv").read()
@app.route("/", methods=['POST'])
def hello():
    try:
        resultDict = {}
        df = pd.read_excel("salesfunnel.xlsx")
        s=df.to_string
        columns_list = df.columns
        print columns_list
        columns_list_tmp=[]
        for i in columns_list:
            print i
            columns_list_tmp.append(i)
        print columns_list_tmp
        parameter = request.data
        #[u'Account', u'Name', u'Rep', u'Manager', u'Product', u'Quantity', u'Price', u'Status']
        parameter = """
                {
                "version":"1.0.0",
                "pre":{},
                "post":{},
                "default":
                {
                    "index_list":["Name"],
                    "columns_list":["Rep"],
                    "values_list":["Price"],
                    "fill_value":0,
                    "margins":"False",
                    "conditions":[]
                }
                }
        """
        param_json = json.loads(parameter)

        index_list = param_json['default']['index_list']
        columns_list = param_json['default']['columns_list'] 
        values_list = param_json['default']['values_list'] 
        fill_value = param_json['default']['fill_value'] 
        margins = param_json['default']['margins'] 
        conditions = param_json['default']['conditions'] 

        ret_vir_tab = pd.pivot_table(df,index=index_list,columns=columns_list,values=values_list,fill_value=fill_value,margins=margins)
        ret_vir_tab.to_csv("hello.csv")

        print ret_vir_tab

        resultDict['data'] = param_json['version'] 
        return json.dumps(resultDict)
    except:
        s = traceback.format_exc()
        print s
        return "error"

if __name__ == "__main__":
    
    app.run()
