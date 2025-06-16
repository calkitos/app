import pandas as pd
import json
import numpy as np
import os
from pathlib import Path


class PatientsDataFrame:
    def __init__(self, data:dict):
        patients = pd.DataFrame(np.array(list(data.keys())),columns=["nombre"])
        patients["paciente_id"] = range(1000,1000+len(patients))

        self.patients = patients[["paciente_id","nombre"]]


class VisitsDataFrame:
    def __init__(self, data:dict, patients:pd.DataFrame):
        my_array = [[[name, date] for date in data[name]["fecha"]] for name in data.keys()]
        new_array = []
        for value in my_array:
            for val in value:
                new_array.append(val)
        self.array = np.array(new_array)
        visits = pd.DataFrame(self.array, columns=["nombre","fecha"])
        visits = visits.merge(patients.loc[:,["nombre","paciente_id"]],how="right",on="nombre", validate="many_to_one")
        visits["visita_id"] = range(100000, 100000 + len(visits))
        self.visits = visits[["visita_id","paciente_id","fecha"]]


class MeasurementsDataFrame:
    def __init__(self, data:dict):
        self.data = data
        self.dataframe = self.process_patients()        


    def get_features(self, patient_name:str):
        data_keys = self.data[patient_name].keys()
        excluded_ones = ["fecha","composicion_corporal"]
        features = [feature for feature in data_keys if feature not in excluded_ones]
        
        return features

    
    def process_measurements(self, patient_name:str, feature:str):
        fechas = self.data[patient_name]["fecha"]
        medidas = self.data[patient_name][feature]
        dataframe = pd.DataFrame()
        # dataframe.columns=["paicente_nombre","fecha","medida","valor"]
               
        for fecha, medida in zip(fechas, medidas):
            new_entry = pd.DataFrame([[
                patient_name,
                fecha,
                feature,
                medida
            ]], columns=["nombre","fecha","medida","valor"])
            dataframe = pd.concat([dataframe, new_entry], axis=0)

        return dataframe

    
    def process_patients(self):
        all_measurements = pd.DataFrame()
        # all_measurements.columns=["paicente_nombre","fecha","medida","valor"]
        for patient in self.data.keys():
            for feature in self.get_features(patient_name=patient):
                new_entry = self.process_measurements(patient_name=patient,feature=feature)
                all_measurements = pd.concat([all_measurements,new_entry], axis=0)
        
        all_measurements["medicion_id"] = range(100000,100000+len(all_measurements))

        return all_measurements
        

def main():
    with open("data/raw/texts.json","r") as my_file:
        data = json.load(my_file)

    all_data = dict(data)
    patients = PatientsDataFrame(data=all_data).patients
    visits = VisitsDataFrame(data=all_data,patients=patients).visits
    measures = MeasurementsDataFrame(all_data).dataframe

    measures = measures.merge(patients, how="left", on="nombre")
    measures = measures.merge(visits, how="left", on=["paciente_id","fecha"])
    measures = measures[["visita_id","paciente_id","medida","valor"]]

    directory = Path("app_nutricion/data/processed/")

    patients.to_csv(os.path.join(directory,"pacientes.csv"))
    visits.to_csv(os.path.join(directory,"visitas.csv"))
    measures.to_csv(os.path.join(directory,"mediciones.csv"))


if __name__=="__main__":
    main()

    
    



# features:list[str] = []

# measurement:dict = {
#     "measurement_id":None,
#     "visit_id":None,
#     "feature":None,
#     "unit":None,
#     "value":None
# }#[measurement_id:int, visit_id:int, feature:str, unit:str, value:float]

# visit:dict = {
#     "visit_id":None,
#     "patient_id":None,
#     "date":None
# }# [visit_id:int, patient_id:int, date:date]

# patient:dict = {
#     "patient_id":None,
#     "name":None,
#     "gender":None,
#     "age":None,
#     "height_last":None,
#     "weight_last":None,
#     "patient_type":None
# }#[patient_id:int, name:str, gender:str, age:int, height_last:float, weight_last:float, patient_type_id:int]

# measurements = pd.DataFrame(None,columns=measurement.keys())

# visits = pd.DataFrame(visit)

# patients = pd.DataFrame(patient)

# print(measurements)
# print(visits)
# print(patients)





# # -*- coding: utf-8 -*-
# import click
# import logging
# from pathlib import Path
# from dotenv import find_dotenv, load_dotenv


# @click.command()
# @click.argument('input_filepath', type=click.Path(exists=True))
# @click.argument('output_filepath', type=click.Path())
# def main(input_filepath, output_filepath):
#     """ Runs data processing scripts to turn raw data from (../raw) into
#         cleaned data ready to be analyzed (saved in ../processed).
#     """
#     logger = logging.getLogger(__name__)
#     logger.info('making final data set from raw data')


# if __name__ == '__main__':
#     log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     logging.basicConfig(level=logging.INFO, format=log_fmt)

#     # not used in this stub but often useful for finding various files
#     project_dir = Path(__file__).resolve().parents[2]

#     # find .env automagically by walking up directories until it's found, then
#     # load up the .env entries as environment variables
#     load_dotenv(find_dotenv())

#     main()
