import re
import unicodedata
from datetime import datetime

def clean_text(text:str)->str:
    """
    Takes a text, replaces double line breaks with single ones,
    replaces double spaces with single ones and strips the text before returning
    the modified version.
    """
    double_linebreak_pattern = re.compile(r"\n+")
    text = double_linebreak_pattern.sub("\n",text)
    double_space_pattern = re.compile(r"\s+")
    text = double_space_pattern.sub(" ",text)
    
    return text.strip()


def lowercase_back_oneline(text:str)->str:
    """
    Sifts a text line by line joining lines that start in lower case 
    or special characters with the one before and cleans them to return 
    a string of multiple lines.
    """

    sub_composicion_corporal = re.compile(r"(?<=\d)\sCOMPOSICIÓN")

    if sub_composicion_corporal.findall(text):
        text = sub_composicion_corporal.sub("\nCOMPOSICIÓN", text)

    lines:list[str] = text.splitlines()
    resulting_lines:list[str] = []

    special_characters = "[ ] ( ) ! ¡ ? ¿ 1 2 3 4 5 6 7 8 9 0 /".split(" ")

    for line in lines:
        if len(line.strip()) < 1:
            pass
        elif line.strip()[0].islower() == False and line.strip()[0] not in special_characters:
            resulting_lines.append(line)
        else:
            resulting_lines[-1] = resulting_lines[-1].join([" ",line])
    
    return "\n".join([clean_text(line) for line in resulting_lines])


def stick_wchars_to_digits(text:str)->str:
    """
    Replaces all single spaces between a number and a letter with nothing.
    """
    search_pattern = re.compile(r"(?<=\d) (?=[a-z,A-Z])")

    return search_pattern.sub("",text)

    
def string_to_float(data_point:str):
    """
    Takes a string and attempts to convert it into a float if possible.
    """
    try:
        return float(data_point)
    except TypeError:
        return data_point
    

def remove_accents(text):
    """
    Normalizes characters in Spanish to avoid encoding problems.
    """
    normalized_text = unicodedata.normalize('NFKD', text)
    return "".join([c for c in normalized_text if not unicodedata.combining(c)])


def normalize_feature_text(text:str):
    """
    Makes sure that the word 'báscula' is replaced with 'kg' to homogenize the 
    feature tags.
    """
    parentheses = re.compile(r"\(.*?\)")
    new_text = parentheses.sub("",text).strip()
    new_text = new_text.lower().replace(" ","_").replace("bascula","kg")
    new_text = remove_accents(new_text)

    return new_text


def parse_date(spanish_date:str):
    """
    Reads a string with the Spanish format 'dd-mm-YYYY' and parses it to make it 
    into a datetime object and return it as a string again. NOTE: The datetime object
    could be use for some other things.
    """
    dia, mes, ano = spanish_date.split("-")
    dia = int(dia)
    mes = int(mes)
    ano = int("20"+ano) if len(ano) == 2 else int(ano)
    return datetime(ano,mes,dia).strftime("%Y-%m-%d") 
    
    
def get_digits(data:list[str])->list:
    result = []
    for d_point in data:
        search_digits = re.compile(r"\d+\.?\d*")
        number = search_digits.search(d_point)
        if number:
            number = string_to_float(number.group(0))
        result.append(number)
    
    return result


def absolute_relative_data(feature:str,data:list,measurement_unit:str)->dict:
    """
    Separates the datapoints that correspond to relative values, marked with '%'
    from absolute values (usually 'kg') where needed. This function only pays attention
    to whether the percentage sign follows the digits.
    """
    classified_data = dict()
    absolute_values = []
    relative_values = []

    for data_point in data:
        if data_point.endswith("%"):
            relative_values.append(data_point)
            classified_data.update({f"{feature}_%":get_digits(relative_values)})
        else:
            absolute_values.append(data_point)
            feature_name = f"{feature}_{measurement_unit}" if measurement_unit != "" else feature
            classified_data.update({feature_name:get_digits(absolute_values)})

    return classified_data


def clean_features(feature_data:dict, feature_unit:dict):
    """
    This matches features to values but making sure such features remain in lowercase
    with '_' instead of white space and with no parentheses.
    """
    new_dataset = dict()
    for key, value in feature_data.items():
        feature = normalize_feature_text(key)
        if feature == "fecha":
            new_dataset.update({feature:[parse_date(date) for date in feature_data["Fecha"]]})
        else:
            data = absolute_relative_data(feature,value,feature_unit[key])
            new_dataset.update(data)
        
    return new_dataset 