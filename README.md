## NutriExplorer ([Streamlit](https://docs.streamlit.io/) app with [NutriStorage API](https://www.nutristorage.ch/api/docs/))


Welcome to the Explorer app! 

Tailored for the FCS students at HSG, this app demonstrates how you can use streamlit and the NutriStorage API to build an interactive dashboard.

### Features 
- Get 3 random seprenditipy products with optional filters
- Search a product by GTIN and retailer. If the product is found, it will also be possible to redirect to the product on the website of the chosen retailer.

### Getting Started
#### Demo
https://nutri-explorer.streamlit.app/

#### Prerequisites

- Python 3.12 (to be compatible with streamlit deployment)
- [Conda installation](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

#### Installation
***1. Clone this repository***

```bash
git clone https://github.com/jingwujw/2025FS-nutriexplorer
```
***2. Create a conda env*** 
```bash 
conda create -n streamlit_nutristorage_app python=3.12
conda activate streamlit_nutristorage_app
```

***3. Install dependencies***
```
pip install -r requirements.txt
```

***4. Install dependencies***
```
streamlit run app.py
```
