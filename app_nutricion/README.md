app_nutricion
==============================
ENGLISH

Nutrition specialist, K, uses an online app for managing and organizing her patients information, especially measurements, such as height, weight, and skin folds. However, said app has a limited functionality, i.e. it does not make certain graphs, it does not classify patients, and it makes data manipulation difficult overall.

An obvious solution is to download the data in csv format to complement the online app with other tools such as Excel or Google Sheets. Nevertheless, the app does not offer any such download option. Additionally, inspection of the app code revealed that it uses PHP to prevent easy access to the data, even if it belongs to the nutritionist. The most systematic way to access data is through downloading PDF files for each patient. Therefore, a program to read the PDFs, extract the data and write a csv file became necessary.

In line with those needs, this program intends to extract and manage information about patiens for clinical use. It takes PDFs as input and returns and saves several csv files. The data structure of this files considers at least 3 normal forms —information was initially stored in one table for each patient. Now we have 3 different databases: a) one with information about the patients, b) one with information about the visits, and c) one with information about each measurment that was made during each of those visits. Through the primary keys of this databases it is possible to connect and structure other practical views of the data without compromising their cleanliness.

==============================
SPANISH

La especialista en nutrición, K, utiliza una aplicación en línea para administrar y organizar la información de sus pacientes, especialmente, medidas como estatura, peso y pliegues cutáneos, entre otras. No obstante, dicha aplicación en línea tiene funcionalidades limitadas, en tanto que no elabora ciertos gráficos, no clasifica a los pacientes y, en general, hace difícil la manipulación de los datos.

Una solución obvia al problema es descargar los datos en formato csv y complementar el uso de la aplicación con herramientas en Excel o Google Sheets. Sin embargo, la aplicación no ofrece una descarga de los datos en formato csv. Inspeccionar el código de la aplicación revela que, adicionalmente, utiliza PHP para impedir el acceso fácil a los datos, a pesar de que pertenecen a la nutrióloga. La forma más sistemática de acceder a los datos resultó ser la descarga de archivos PDF. Por lo tanto, se volvió necesario un programa que lea los PDFs y extraiga los datos a un archivo csv.

A partir de lo anterior, esta aplicación pretende extraer y administrar información sobre pacientes de nutrición para uso clínico. Toma como materia prima archivos en formato PDF y extrae el texto para formar y guardar varios archivos csv. La estructura de estos archivos contempla, por lo menos, 3 formas normales de la estructura de datos, por lo que la información que inicialmente se dividía en tablas históricas para cada paciente se dividió en: a) una tabla con información de pacientes, b) una tabla con información de todas las visitas y c) una tabla con información de todas las medidas realizadas. Posteriormente será posible relacionar estas tablas mediante sus respectivas llaves primarias para generar vistas específicas.


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
