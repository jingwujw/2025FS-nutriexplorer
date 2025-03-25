# Import libraries
import requests
import streamlit as st

# Import the secrets
nutristorage_base_url = st.secrets["nutristorage_base_url"]
nutristorage_username = st.secrets["nutristorage_username"]
nutristorage_password = st.secrets["nutristorage_password"]


def get_product_by_gtin(
        gtin: str,
        retailer: str,
    ):
        """Retrieve a product by GTIN from Migros or Coop.

        Args:
            gtin: Gtin of the product to search
            retailer: Migros or Coop
        """
        response = requests.get(f"{nutristorage_base_url}/api/products/{retailer}/{gtin}", auth=(nutristorage_username, nutristorage_password))
        status_code = response.status_code
        if (status_code != 200) or (not response.content):
            print("Warning: something wrong or empty response")
            return None
        return response.json()

    
def get_products_from_a_NS_cat(retailer: str, 
                               min_nutri_score: str,
                               l2_cat: str):
    """Retrieve products with a minimum Nutri-Score from a retailer.

    Args:
        retailer: Migros or Coop
        min_nutri_score: Minimum Nutri-Score, A, B, C, D, or E
        l2_cat: Category in German
    """
    params = {
         "nutri-score-cutoff": min_nutri_score,
         "retailer": retailer,
         "dietcoach-category-l2-de":l2_cat
    }

    # Remove None values from the params
    valid_params = {k: v for k, v in params.items() if v is not None}

    response = requests.get(f"{nutristorage_base_url}/api/products", 
                            auth=(nutristorage_username, nutristorage_password),
                            params = valid_params)

    return response.json()