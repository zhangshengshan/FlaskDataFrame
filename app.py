import pandas as pd
import json, redis
import numpy as np
import traceback
from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)

@app.route("/logout", methods=['GET'])
def logout():
    return "logout"
@app.route("/login", methods=['GET'])
def login():
    return render_template("aa.html")
@app.route("/get", methods=['GET'])
def get():
    return open("static/hello.csv").read()
@app.route("/", methods=['GET','POST'])
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
        if request.method == 'POST':
            parameter = request.data
        else:
            #[u'Account', u'Name', u'Rep', u'Manager', u'Product', u'Quantity', u'Price', u'Status']
            parameter = """
                    {
                        "version":"1.0.0",
                        "pre":{},
                        "post":{},
                        "default":
                            {
                                "index_list":["Product"],
                                "columns_list":["Status"],
                                "values_list":["Price","Quantity"],
                                "fill_value":0,
                                "margins":"False",
                                "aggfunc":
                                    {
                                        "Price":["default","count"],
                                        "Quantity":["max","mean"]
                                    },
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
        
        margins = False

        # margins and aggfunc should be judged to testify whether it is wright to solve!!!1

        conditions = param_json['default']['conditions'] 

        FUNC_DICT={
                "default":np.sum,
                "mean":np.mean,
                "count":len,
                "max":np.max,
                "min":np.min
                }

        aggfunc_dict = {}
        origin_aggfunc_config = param_json['default']['aggfunc']
        for i in values_list:
            if i in origin_aggfunc_config and len(origin_aggfunc_config[i]) != 0:
                aggfunc_dict[i]=[]
                for j in origin_aggfunc_config[i]:
                    aggfunc_dict[str(i)].append(FUNC_DICT[j])
            else:
                aggfunc_dict[i]=[FUNC_DICT['default']]
        print aggfunc_dict
        ret_vir_tab = pd.pivot_table(df,index=index_list,columns=columns_list,values=values_list,fill_value=fill_value,margins=margins,aggfunc=aggfunc_dict)
        print ret_vir_tab
        ret_vir_tab.to_html("aa.html")
        print aggfunc_dict
        table_content  = open("aa.html").read()
        print table_content
        resultDict['data'] = param_json['version'] 
        return render_template('index.html', name="hello", table=table_content)
    except:
        s = traceback.format_exc()
        print s
        return "error"

if __name__ == "__main__":
    app.debug = True
    app.run()
