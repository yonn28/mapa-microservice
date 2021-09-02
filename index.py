from flask import Flask, jsonify
import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

base_f = pd.read_csv('https://storage.googleapis.com/ds4all-test-bd1/base_target_final_180601.csv')

dpts_count_target1=base_f.query("Marca_Target_Reincidencia_F12M==1").groupby(['cod_dpto','nom_dpto','anno_encuesta']).size().to_frame('Count_Dpto_Rel').reset_index()
dpts_count_target2=base_f.query("Marca_Target_EntroEnDesnutricion_F12M==1").groupby(['cod_dpto','nom_dpto','anno_encuesta']).size().to_frame('Count_Dpto_Mal').reset_index()
dpts_count_total=base_f.groupby(['cod_dpto','nom_dpto','anno_encuesta']).size().to_frame('Count_Dpto_Total').reset_index()
dpts_count_1 = pd.merge(dpts_count_target1, dpts_count_target2, on=["cod_dpto", "nom_dpto", "anno_encuesta"])
dpts_count = pd.merge(dpts_count_1, dpts_count_total, on=["cod_dpto", "nom_dpto", "anno_encuesta"])
dpts_count["Relapse_Percentage"] = dpts_count["Count_Dpto_Rel"]/dpts_count["Count_Dpto_Total"]*100
dpts_count["Malnutrition_Percentage"] = dpts_count["Count_Dpto_Mal"]/dpts_count["Count_Dpto_Total"]*100
dpts_count['cod_dpto']=pd.to_numeric(dpts_count['cod_dpto'])
dpts_count['cod_dpto']=dpts_count['cod_dpto'].astype(int)
dpts_count['cod_dpto']=dpts_count['cod_dpto'].apply(lambda x: '{0:0>2}'.format(x))
dpts_count.rename(columns={'anno_encuesta': 'Año'}, inplace=True)


@app.route('/api/v1/maps', methods=['GET'])
def ploting_get_maps():
    return jsonify(dpts_count.to_dict("records"))


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0',port=8080) #change port to 8080 for deployment, and host = '0.0.0.0'