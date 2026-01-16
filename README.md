# PEC4 – Statistical Analysis of University Student Performance in Catalonia

This project corresponds to Exercise 4 of the subject *Programación para la Ciencia de Datos*.  
The objective is to build a modular Python project that loads, cleans, merges and analyzes datasets related to university student performance and dropout rates in Catalonia, and generates a structured statistical report in JSON format.


## Project Structure

-> src/
    -> data/ --> Input datasets
    -> img/ --> Generated plots
    -> report/ --> Generated JSON reports
        -> analisi_estadistic.json
    -> modules/ --> Project modules
        -> analysis.py
        -> exercises.py
        -> load_dataset.py
        -> merge_dataset.py
        -> visualization.py
        -> args_parser_helper.py
-> tests/ --> Unit tests
-> doc/ --> Generated HTML documentation
-> screenshots/ --> Screenshots required in the PEC
-> main.py --> Entry point of the project
-> requirements.txt --> Project dependencies
-> .pylintrc --> Linter configuration
-> .gitignore --> Ignored files and folders
-> LICENSE --> Project license
-> README.md --> This file


---

## Installation

It is recommended to use a virtual environment.

### 1. Create a virtual environment:

```bash
python -m venv venv
```
### 2. Activate it:

```bash
.\venv\Scripts\activate
```

### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Execution

The main entry point of the project is:

```bash
python main.py # This will execute all the exercises sequentially.
```

```bash
python main.py -ex 2 # This will execute exercises from 1 to 2.
```

```bash
python main.py -m # This will execute all exercises using manual dataset loading.
```

To see the help:
```bash
python main.py -h
```

### 5. Output

The statistical analysis of Exercise 4 generates a JSON file:

src/report/analisi_estadistic.json


This file contains:

Global statistics

Correlation between dropout and performance

Analysis by academic branch

Trend detection

Rankings

### 6. Testing

To run all tests:


```bash
pytest
```

To check test coverage:

```bash
coverage run -m pytest
coverage report
coverage html
```

The HTML coverage report will be generated in:

```bash
htmlcov/
```

### 7. Documentation

The project is fully documented using docstrings.
To generate the HTML documentation:


```bash
sphinx-build -b html src doc/
```

The documentation will be generated in the doc/ folder.

### 8. Code Style (Linter)

The project follows PEP8 style using pylint.

To run pylint:

```bash
pylint *.py
```

### 9. Requirements

To install all required libraries:
```bash
pip install -r .\requirements.txt
```

### 10. License

This project is distributed under the license specified in the LICENSE file.