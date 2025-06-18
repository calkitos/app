from pypdf import PdfReader, PageObject
import re
import json
import warnings
import os
from pathlib import Path
from utils import clean_features,lowercase_back_oneline,stick_wchars_to_digits


def read_alldocs(pdfs_folder)->list[PageObject]:
    """
    Reads through all files in a folder and makes PDF PageObjects from the
    pypdf module.
    """
    pages = list()

    for doc in os.listdir(pdfs_folder):
        doc_path = os.path.join(pdfs_folder,Path(doc))
        reader = PdfReader(doc_path)
        if len(reader.pages)>1:
            warnings.warn(f"\n====\nPdfReader corresponding to file: {doc} has more pages than expected.\n====",UserWarning)
        pages.append(reader.pages[0])

    return pages


class PatientLog:
    def __init__(self, pdf_file:PageObject):
        self.patient_file = pdf_file
        self.data_as_text = lowercase_back_oneline(pdf_file.extract_text())
        self.data_as_lines = self.data_as_text.splitlines()

    
    def get_patient_name(self)->str:
        name_pattern:re.Pattern[str] = re.compile(r"(?<=NOMBRE:)(.*)")
        f"""
        Matches and returns the stripped string after 'NOMBRE:' in
        self.data_as_text using the regular expression pattern {name_pattern}
        """
        name_is:re.Match = name_pattern.search(self.data_as_text)
        name:str = name_is.group(0) if name_is else "NO_NAME"
        
        return name.strip()
    

    def get_features(self)->list[str]:
        """
        Returns a list of the features available in a given document. These may
        be different accross documents. Some may be missing and some may have 
        a different writing.
        """
        find_features_pattern = re.compile(r"[A-Z][a-z]*.*?(?=\s\d)")
        iter_results = find_features_pattern.finditer(self.data_as_text)
        list_of_features:list = []
        for result in iter_results:
            list_of_features.append(result.group(0))

        return list_of_features
    

    def get_values(self)->dict:
        """
        Uses the get_features method of this same class to return a dictionary
        of all the values corresponding to each feature.
        """
        measurements = dict()
        features = self.get_features()

        for feature in features:
            search_for = f"(?<=\n{re.escape(feature)}\s).*"
            search_pattern = re.compile(search_for)

            my_match = search_pattern.findall(self.data_as_text)
            measure = my_match[0] if my_match else ""
            data = stick_wchars_to_digits(measure).split(sep=" ")
            measurements.update({feature:data})

        return measurements


def get_measurement_unit_from_dict(source:dict)->dict:
    units = dict()
    for key in source.keys():
        units.update({key:list()})

    #Search in keys
    search_parentheses = re.compile(r"(?<=\().*?(?=\))")
    search_wcharacters = re.compile(r"(?<=\d)[a-z]+$")

    for key,value in source.items():
        my_match = search_parentheses.search(key)
        value_matches = [search_wcharacters.search(data) for data in value]
        if my_match:
            unit = my_match.group(0)
            units[key].append(unit)

    #Search in values
        for match in value_matches:
            if match:
                units[key].append(match.group(0))

        set_of_units = list(set(units[key]))
        units[key] = set_of_units[0] if len(set_of_units) > 0 else ""
    return units


def analyze_pdfs(input_folder:Path,output_folder:Path):
    all_docs = read_alldocs(pdfs_folder=input_folder)
    new_folder = os.path.join(output_folder,Path("./raw"))
    my_repository = dict()
    clean_text = ""

    if not os.path.isdir(new_folder): os.mkdir(new_folder) 

    for doc in all_docs:#Analize PDFs data
        log = PatientLog(doc)
        name = log.get_patient_name()
        values = log.get_values()
        units = get_measurement_unit_from_dict(values)
        measurements = clean_features(values,units)
        my_repository.update({name:measurements})
        clean_text += "\n===\n\n" + log.data_as_text

    txt_file_path = os.path.join(new_folder,"text.txt")
    json_file_path = os.path.join(new_folder,"data.json")

    with open(txt_file_path,"w",encoding="utf-8") as my_file:#Write a txt file
        print("WRITING FILE...")
        my_file.write(clean_text)
        print(f"THE FILE {txt_file_path} HAS BEEN MODIFIED.")   

    with open(json_file_path,"w",encoding="utf-8") as my_file:#Write a json file
        print("WRITING FILE...")
        json.dump(my_repository,my_file)
        print(f"THE FILE {json_file_path} HAS BEEN MODIFIED.")        
    
    
def main():
    pdfs_folder = Path("app_nutricion/data/raw/pdfs")
    raw_folder = Path("app_nutricion/data/raw")
    text_file_name = "texts.json"
    text_path = os.path.join(raw_folder,text_file_name)

    all_docs = read_alldocs(pdfs_folder=pdfs_folder)

    my_repository = dict()

    for doc in all_docs:
        log = PatientLog(doc)
        name = log.get_patient_name()
        values = log.get_values()
        units = get_measurement_unit_from_dict(values)
        measurements = clean_features(values,units)
        my_repository.update({name:measurements})

    # print(my_repository)

    with open(text_path,"w",encoding="utf-8") as my_file:
        print("WRITING FILE...")
        json.dump(my_repository,my_file)


if __name__=="__main__":
    main()
