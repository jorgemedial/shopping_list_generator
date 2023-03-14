import pandas as pd
import streamlit as st
from gsheetsdb import connect


class DataConnector:
    def __init__(self):
        self.conn = connect()

    #@st.cache_data(ttl=30)
    def fetch_data(self, config):
        return {
            "ingredients": self._fetch_ingredients(config),
            "recipes": self._fetch_recipe(config),
            "meal_plan": self._fetch_meal_plan(config),
            "inventory": self._fetch_inventory(config),
            "nutritional_requirements": self._fetch_nutritional_requirements(config)
        }

    def update_data(self, data):
        pass
    def _query_dataframe(self, table_name: str, columns: list) -> pd.DataFrame:
        sheet_url = st.secrets[table_name]
        query = f'SELECT * FROM "{sheet_url}"'
        rows = self.conn.execute(query, headers=1)
        rows = rows.fetchall()
        df_as_dict = {column_name: column_values for column_name, column_values in zip(columns, zip(*rows))}
        return pd.DataFrame(df_as_dict)

    def _fetch_recipe(self, config: dict):
        table_name = "recipe"
        return self._query_dataframe(table_name, columns=config["columns"][table_name])

    def _fetch_meal_plan(self, config: dict):
        table_name = "meal_plan"
        return self._query_dataframe(table_name, columns=config["columns"][table_name])

    def _fetch_inventory(self, config):
        table_name = "inventory"
        return self._query_dataframe(table_name, columns=config["columns"][table_name])


    def _fetch_ingredients(self, config: dict):
        table_name = "ingredient"
        return self._query_dataframe(table_name, columns=config["columns"][table_name])


    def _fetch_nutritional_requirements(self, config):
        return None

class ListGenerator:
    pass