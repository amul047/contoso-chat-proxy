# In production RAG apps, this tool would query a database or an API to get the customer's order history.
# For the purpose of this demo, we are using local JSON files and Pandas DataFrames to simulate the customer's order history.

import os
from promptflow.core import tool
import pandas as pd


def get_customer_order_history(customerId):
    path = r"../data/customer_info/"
    big_df = pd.concat(
        [
            pd.read_json(path + file)
            for file in os.listdir(path)
            if file.endswith(".json")
        ],
        ignore_index=True,
    )
    return big_df[big_df["id"] == int(customerId)]


@tool
def customer_lookup(customerId: str) -> str:
    rows = get_customer_order_history(customerId)
    if not rows.empty:
        response = rows.iloc[0].to_dict()
        response["orders"] = [row["orders"] for _, row in rows.iterrows()][:2]
        return response

    return {}
