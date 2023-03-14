import json

from src.shopping_list_generator import DataConnector, ListGenerator
import streamlit as st
config_path = "config.json"


if __name__ == '__main__':
    # Create a connection object.
    config_path = "config.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    tables = DataConnector().fetch_data(config)
    required_quantities = tables["meal_plan"].join(
        tables["recipes"].set_index("recipe_name"), on="recipe_name", how="left"
    ).groupby("ingredient_name")["quantity"].sum()

    shopping_list = tables["inventory"].join(
        required_quantities, on="ingredient_name",
        how="outer",
        lsuffix="_inventory",
        rsuffix="_required"
    ).set_index(
        "ingredient_name"
    ).apply(
        lambda row: row["quantity_required"] - row["quantity_inventory"], axis=1
    ).apply(
        lambda quantity: quantity if quantity > 0 else None
    ).dropna()

    st.table(data=shopping_list)

    pass


