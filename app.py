# Install libraries
import streamlit as st
import nutristorage_api_client as ns
import utils

# Tab title and icon
st.set_page_config(page_title="NutriExplorer", page_icon="🥗")

# Title & Intro
st.title('NutriExplorer: Explore the NutriStorage World!')
st.write("""
Hi FCS students 👋👋👋
         
Welcome to this interactive Streamlit app NutriExplorer, integrated with the NutriStorage API.
NutriStorage is a food composition database containing 20,000+ Swiss general and branded food products.
""")
st.link_button("Go to NutriStorage", "https://www.nutristorage.ch")

# Input gtin
st.subheader("NutriSurprise: Meet your serendipity products of today!")

# Display the segmented control for minimum Nutri-Score and retailer
left, right = st.columns(2)

nutri_score_options = ["A", "B", "C", "D", "E"]
ns_selection = left.segmented_control(
    "Minimum Nutri-Score", nutri_score_options, selection_mode="single"
)

retailer_options = ["Migros", "Coop"]
retailer_selection = right.segmented_control(
    "Retailer", retailer_options, selection_mode="single"
)

# Provide a few food categories to choose from
l2_cat_options = ["Früchte", "Gemüse", "Käse & Käseprodukte", "Süsse Snacks", "Salzige Snacks", "Süssgetränke"]
l2_cat_selection = st.pills("Example Categories", l2_cat_options)

# Button to trigger the search
if st.button("Surprise me!"):
    products = ns.get_products_from_a_NS_cat(retailer_selection, ns_selection, l2_cat_selection)
    # Get the number of products
    num_products = products["meta"]["totalProducts"]
    st.write(f"""Found {num_products} products with Nutri-Score {ns_selection} from {retailer_selection} in the category {l2_cat_selection} in total.
             See the ones for you!""")
    
    # Display 3 random products
    random_3_products = utils.extract_random_3_product_info(products["products"])
    col1, col2, col3 = st.columns(3)
    if num_products >= 3:
        with col1:
            st.image(random_3_products[0]["image"])
            st.write(f"{random_3_products[0]['name']}")
            st.write(f"GTINs: {random_3_products[0]['gtins']}")
        with col2:
            st.image(random_3_products[1]["image"])
            st.write(f"{random_3_products[1]['name']}")
            st.write(f"GTINs: {random_3_products[1]['gtins']}")
        with col3:
            st.image(random_3_products[2]["image"])
            st.write(f"{random_3_products[2]['name']}")
            st.write(f"GTINs: {random_3_products[2]['gtins']}")
    elif num_products == 2:
        with col1:
            st.image(random_3_products[0]["image"])
            st.write(f"{random_3_products[0]['name']}")
            st.write(f"GTINs: {random_3_products[0]['gtins']}")
        with col2:
            st.image(random_3_products[1]["image"])
            st.write(f"{random_3_products[1]['name']}")
            st.write(f"GTINs: {random_3_products[1]['gtins']}")
    elif num_products == 1:
        with col1:
            st.image(random_3_products[0]["image"])
            st.write(f"{random_3_products[0]['name']}")
            st.write(f"GTINs: {random_3_products[0]['gtins']}")


st.subheader("Product Detective: Find Product Nutrition Information!")

left, right = st.columns(2)

retailer = left.selectbox("Retailer", ["migros", "coop"])
product_gtin = right.text_input("GTIN")

# Button to trigger the search
if st.button("Search by GTIN"):
    response = ns.get_product_by_gtin(product_gtin, retailer)
    if response is None:
        st.error(f"No product found with this GTIN from {retailer}.")
    else:
        # Parse information from the response json
        product_name = response["de"]["name"]
        product_url = response["en"]["url"]
        nutrients_base = response["nutrients"]["base"]
        nutrition_label_info = utils.extract_nutrition_label_info(response["nutrients"])

        # Display the product image and nutrition label
        st.text(f"We have found {product_name} for you in NutriStorage!")
        st.image(response["imageUrl"], width=200)
        st.text("Nutrition Facts:")
        st.table(nutrition_label_info.set_index(""))

        # Display a button to check the product directly on the retailer's website
        st.link_button(f"Check {product_name} directly on {retailer.capitalize()}", product_url)