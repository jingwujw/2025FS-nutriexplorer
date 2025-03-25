#  Install libraries
import json
import re
import pandas as pd
import requests
from PIL import Image
import requests
from io import BytesIO
import random

def extract_nutrition_label_info(nutrients: json):
    """Extract the nutrition label information from the response"""

    def format_nutrient(keyword, unit = "g"):
        available_keys = ["kj", "kcal", "fatsG", "saturatedFatsG", "carbohydratesG", "sugarsG", "fibersG", "proteinsG", "saltG"]
        # Check if the keyword is available
        if keyword not in available_keys:
            return ""
        
        # Get the prefix if it exists
        prefix = nutrients.get(f"{keyword}Prefix")
        if prefix is None:
             prefix = ""

        # Get the value
        value = nutrients.get(keyword)
        if value is None: 
            keyword_without_unit = re.sub(r'(Mg|G)$', '', keyword).strip()
            value = nutrients.get(keyword_without_unit, "")
        # Format and return
        return f"{prefix}{value} {unit}"

    nutrition_label_info = {
        "Energy": f"{format_nutrient('kj', 'kJ')} ({format_nutrient('kcal', 'kcal')})",
        "Fats": format_nutrient("fatsG"),
        "of which saturates": format_nutrient("saturatedFatsG"),
        "Carbohydrates": format_nutrient("carbohydratesG"),
        "of which sugars": format_nutrient("sugarsG"),
        "Fibres": format_nutrient("fibersG"),
        "Proteins": format_nutrient("proteinsG"),
        "Salt": format_nutrient("saltG"),
    }

    df = pd.DataFrame({
    "": nutrition_label_info.keys(),
    "Content per 100g product": nutrition_label_info.values()
    })
    
    return df


def extract_random_3_product_info(products: json):
    """Extract random 3 products from all products"""

    random_3_products = random.sample(products, min(3, len(products)))

    product_ls = []
    for p in random_3_products:
        # Parse certain information 
        name = p["en"]["name"]
        gtins = p["gtins"]

        # Get the image and resize it
        image_url = p["imageUrl"]
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        resized_image = image.resize((200, 200))

        # Append to the list
        product_ls.append({
            "name": name.capitalize(),
            "gtins": gtins,
            "image": resized_image
        })
    
    return product_ls