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
    

def create_csvs(work_directory:Path):
    data_path = os.path.join(work_directory,Path("./raw/data.json"))
    with open(data_path,"r") as my_file:
        data = json.load(my_file)
    
    data = dict(data)

    patients = PatientsDataFrame(data=data).patients
    visits = VisitsDataFrame(data=data,patients=patients).visits
    measures = MeasurementsDataFrame(data).dataframe

    measures = measures.merge(patients, how="left", on="nombre")
    measures = measures.merge(visits, how="left", on=["paciente_id","fecha"])
    measures["medida_id"] = range(1000000, 1000000 + len(measures))
    measures = measures[["medida_id","visita_id","paciente_id","medida","valor"]]

    patients.to_csv(os.path.join(work_directory,"pacientes.csv"),index=False, mode="w")
    visits.to_csv(os.path.join(work_directory,"visitas.csv"),index=False, mode="w")
    measures.to_csv(os.path.join(work_directory,"mediciones.csv"),index=False, mode="w")
        

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
