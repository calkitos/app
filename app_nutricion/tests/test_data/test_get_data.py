import pytest
from app_nutricion.src.get_data import lowercase_back_oneline, one_liner, read_alldocs, look_for_feature, get_values, format_features, build_dictionary
from pathlib import Path


@pytest.fixture
def all_my_docs():
    return read_alldocs(Path("data/raw/pdfs"))


@pytest.fixture
def my_text()->str:
    my_text = """
    This is   
    an example         script 

    that should end up ordered in one line.

    With an added line in
    caps.
    """
    return my_text


@pytest.fixture
def mock_patient():
    """
    Es importante notar que algunos documentos no incluyen el paréntesis (bascula)
    después de masa grasa y masa muscular. Es necesario implementar una condición altenativa.
    """
    return "EVALUACIÓN Y SEGUIMIENTO DE LA COMPOSICIÓN CORPORAL NOMBRE: MOCK PATIENT HAPPY CLAVEL SUMATORIA DE PLIEGUES MEDICIONES CORPORALES Fecha 28-01-25 03-03-25 08-04-25 Peso (kg) 82.3 81.3 79.8 Estatura (cm) 160 160 - IMC (kg/m2) 32.1 31.8 31.2 Masa grasa (bascula) 48.5% 39.9 kg 48% 39 kg 47.8% 38.1 kg Masa muscular (bascula) 19.1% 15.7 kg 19.4% 15.8kg 22.2% 17.71 Grasa visceral 10 10 10 Brazo relajado (cm) 33 33 32.5 Brazo contraído (cm) 31.1 31.2 30.6 Cintura (cm) 96 97.4 93.3 Caderas (cm) 118.5 119.9 117.3 Pantorrilla (cm) 39.8 39.8 40 Sumatoria de pliegues cutáneos (mm) 107 100.5 88 COMPOSICIÓN CORPORAL 4 COMPONENTES"


@pytest.fixture
def my_features():
    features = [
        "Fecha",
        "Peso (kg)",
        "Estatura (cm)",
        "IMC (kg/m2)",
        "Masa grasa (bascula)",
        "Masa muscular (bascula)",
        "Grasa visceral",
        "Brazo relajado (cm)",
        "Brazo contraído (cm)",
        "Cintura (cm)",
        "Caderas (cm)",
        "Pantorrilla (cm)",
        "Sumatoria de pliegues cutáneos (mm)"
    ]
    return features


def test_lower_backonline(my_text):
    expected_result = """This is an example script that should end up ordered in one line.\nWith an added line in caps."""
    assert lowercase_back_oneline(my_text) == expected_result


def test_one_liner(my_text):
    """
    Verifies by several means that the length of the line after implementing this
    function is zero.
    """
    assert "\n" not in one_liner(my_text)
    assert one_liner(my_text).count("\n") == 0
    assert len(one_liner(my_text).splitlines()) == 1


def test_read_alldocs_warning():
    """
    Implementing this allows to make sure that the expected warning pops up.
    """
    assert read_alldocs(Path("data/raw/pdfs"))


def test_all_lines_are_docs(all_my_docs):
    """
    Makes sure that all the documents to be used are being converted into strings.
    """
    lines:list = [one_liner(page.extract_text()) for page in all_my_docs]
    # print([type(line) for line in lines])
    assert all(type(line) == str for line in lines)
    

def test_all_features_are_indocuments(all_my_docs,my_features):
    """
    Makes sure that all the features are found across all documents.
    """
    lines:list = [one_liner(page.extract_text()) for page in all_my_docs]
    for feature in my_features:
        matches = [look_for_feature(feature=feature,text=line) for line in lines]

        assert len(matches) == len(lines)


def test_feats_are_found(mock_patient,my_features):
    """
    Checks that all the features are found within a patients document.
    """
    for feature in my_features:
        print(get_values(feature=feature,text=mock_patient))
        result = get_values(feature=feature,text=mock_patient)
        assert result is not None
        assert len(result) > 0

    
def test_feats_in_doc(mock_patient,my_features):
    """
    Makes sure that there are no empty values in the features dictionary of a
    mock document.
    """
    features_dict = format_features(mock_patient,my_features)
    assert type(features_dict) is dict
    for value in features_dict.values():
        assert len(value) > 0

    for feature in my_features:
        assert feature in features_dict.keys()
    for key in list(features_dict.keys()):
        assert key in my_features


def test_doc_dictionary(mock_patient):
    my_dict = build_dictionary(mock_patient)
    assert type(my_dict) is dict
    for feat in ["Fechas","Mediciones"]:
        assert feat in my_dict.keys()


