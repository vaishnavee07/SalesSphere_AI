import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="SalesSphere AI",
    layout="centered"
)

st.title("SalesSphere AI")
st.subheader("Demand Forecasting System")

st.write(
    "Predict product demand based on customer behaviour, pricing, discounts and seasonal trends."
)

df = pd.read_csv("data/SalesSphereAI_Realistic_Dataset.csv")

model = joblib.load("xgb_demand_model.pkl")

training_columns = joblib.load(
    "training_columns.pkl"
)

product_list = sorted(
    df["Product_Name"].unique()
)

category_list = sorted(
    df["Product_Category"].unique()
)

season_list = sorted(
    df["Season"].unique()
)

product_name = st.selectbox(
    "Select Product",
    product_list
)

product_category = st.selectbox(
    "Select Category",
    category_list
)

base_price = st.number_input(
    "Base Price",
    min_value=1.0,
    value=100.0,
    step=10.0
)

discount_percentage = st.slider(
    "Discount Percentage",
    0,
    50,
    10
)

season = st.selectbox(
    "Season",
    season_list
)

st.markdown("### Product Configuration")

col1, col2 = st.columns(2)

with col1:
    st.write(
        f"**Product:** {product_name}"
    )

    st.write(
        f"**Category:** {product_category}"
    )

with col2:
    st.write(
        f"**Base Price:** ₹{base_price:.2f}"
    )

    st.write(
        f"**Discount:** {discount_percentage}%"
    )

st.write(
    f"**Season:** {season}"
)

predict_button = st.button(
    "Predict Demand"
)

if predict_button:

    simulation_df = df.copy()

    simulation_df["Product_Category"] = product_category
    simulation_df["Product_Name"] = product_name
    simulation_df["Base_Price"] = base_price
    simulation_df["Discount_Percentage"] = discount_percentage
    simulation_df["Season"] = season

    simulation_X = simulation_df[
        [
            "Age",
            "Gender",
            "City",
            "Income",
            "Membership_Level",
            "Product_Category",
            "Product_Name",
            "Base_Price",
            "Discount_Percentage",
            "Season",
            "Payment_Method"
        ]
    ].copy()

    simulation_X = pd.get_dummies(
        simulation_X,
        columns=[
            "Gender",
            "City",
            "Membership_Level",
            "Product_Category",
            "Product_Name",
            "Season",
            "Payment_Method"
        ],
        drop_first=True
    )

    simulation_X = simulation_X.reindex(
        columns=training_columns,
        fill_value=0
    )

    probabilities = model.predict_proba(
        simulation_X
    )[:, 1]

    buyers = (
        probabilities >= 0.5
    ).sum()

    total_customers = len(
        probabilities
    )

    demand_percentage = (
        buyers / total_customers
    ) * 100

    avg_probability = (
        probabilities.mean()
    ) * 100

    st.success(
        "Prediction Completed!"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Potential Buyers",
            f"{buyers:,}"
        )

    with col2:
        st.metric(
            "Demand %",
            f"{demand_percentage:.2f}%"
        )

    with col3:
        st.metric(
            "Average Purchase Probability",
            f"{avg_probability:.2f}%"
        )

    st.write(
        f"Total Customers Evaluated: {total_customers:,}"
    )