import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pickle
import plotly.express as px
import datetime as dt
from babel.numbers import format_currency
from sklearn.metrics import confusion_matrix
sns.set(style='dark')

@st.cache_resource
def load_model():
    with open("model/fraud_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()
df = pd.read_csv("data/Fraudulent_E-Commerce_Transaction_Data.csv")

# X_train = df.drop('Is Fraudulent', axis=1)   # Misal kolom label bernama 'label'
# y_train = df['Is Fraudulent']

def dashboard():
    with st.sidebar:
    # Logo dan Nama Aplikasi (center)
        st.markdown(
            """
            <div style='text-align: center;'>
                <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Shield_icon.svg/1024px-Shield_icon.svg.png' width='50'/>
                <h3>SafePayAI</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Avatar dan Nama Pengguna (center)
        st.markdown(
            """
            <div style='text-align: center;'>
                <div style='font-size: 40px;'>🟤</div>
                <p><strong>Salma Aulia Nazhira</strong></p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")
        st.subheader("Discover")

        selected = st.radio(
            "",
            ["Home", "Browse", "Prediksi Transaksi"],
            index=0,
            format_func=lambda x: f"🏠 {x}" if x == "Home" else "🔍 Browse" if x == "Browse" else "📡 Prediksi Transaksi"
        )

        st.markdown("---")

    if selected == "Home":
        st.title("Home - Dashboard")
        st.subheader('Random Forest Model')
    
        col1, col2, col3 = st.columns(3)
    
        with col1:
            # total_orders = daily_orders_df.order_count.sum()
            # st.metric("Tittle", value="Value")
            st.markdown(f"""
            <div style='border:1px solid #ccc; border-radius:10px; padding:15px; text-align:center;'>
                <div style='font-size:20px; color:gray;'>Accuracy</div>
                <div style='font-size:28px; font-weight:bold;'>"acc:.2f</div>
            </div>
            """, unsafe_allow_html=True)
    
        with col2:
            # total_revenue = format_currency(daily_orders_df.revenue.sum(), "AUD", locale='es_CO') 
            # st.metric("Tittle", value="Value")
            st.markdown(f"""
            <div style='border:1px solid #ccc; border-radius:10px; padding:15px; text-align:center;'>
                <div style='font-size:20px; color:gray;'>Accuracy</div>
                <div style='font-size:28px; font-weight:bold;'>"acc:.2f</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            # total_revenue = format_currency(daily_orders_df.revenue.sum(), "AUD", locale='es_CO') 
            # st.metric("Tittle", value="Value")
            st.markdown(f"""
            <div style='border:1px solid #ccc; border-radius:10px; padding:15px; text-align:center;'>
                <div style='font-size:20px; color:gray;'>Accuracy</div>
                <div style='font-size:28px; font-weight:bold;'>"acc:.2f</div>
            </div>
            """, unsafe_allow_html=True)
        
        # y_pred = model.predict(X_train)
        # cm = confusion_matrix(y_train, y_pred)
        st.subheader("Confusion Matrix Model")
        # fig, ax = plt.subplots(figsize=(16, 8))
        # sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax, 
        #     xticklabels=['Normal', 'Fraud'], yticklabels=['Normal', 'Fraud'])
        st.pyplot(fig)
        
        st.subheader("ROC & Precision-Recall Curve")
    
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
    
        colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    
        sns.barplot(x="quantity_x", y="product_name", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
        ax[0].set_ylabel(None)
        ax[0].set_xlabel("Number of Sales", fontsize=30)
        ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
        ax[0].tick_params(axis='y', labelsize=35)
        ax[0].tick_params(axis='x', labelsize=30)
        
        sns.barplot(x="quantity_x", y="product_name", data=sum_order_items_df.sort_values(by="quantity_x", ascending=True).head(5), palette=colors, ax=ax[1])
        ax[1].set_ylabel(None)
        ax[1].set_xlabel("Number of Sales", fontsize=30)
        ax[1].invert_xaxis()
        ax[1].yaxis.set_label_position("right")
        ax[1].yaxis.tick_right()
        ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
        ax[1].tick_params(axis='y', labelsize=35)
        ax[1].tick_params(axis='x', labelsize=30)
        
        st.pyplot(fig)

        st.subheader("Feature Important (Model)")
        fig, ax = plt.subplots(figsize=(16, 8))
        ax.plot(
            daily_orders_df["order_date"],
            daily_orders_df["order_count"],
            marker='o', 
            linewidth=2,
            color="#90CAF9"
        )
        ax.tick_params(axis='y', labelsize=20)
        ax.tick_params(axis='x', labelsize=15)
        st.pyplot(fig)
    
    elif selected == "Browse":
        st.title("Browse Data Transaksi")
        st.write("Fitur ini untuk melihat transaksi secara detail...")

    elif selected == "Prediksi Transaksi":
        st.title("Deteksi Transaksi Fraud")
        st.write("Fitur ini akan menampilkan prediksi transaksi mencurigakan menggunakan model ML...")
        
        with st.form("fraud_form"):
            amount = st.number_input("Amount", min_value=0.0, format="%.2f")
            hour = st.selectbox("Transaction Hour (0-23)", list(range(24)))
            location_match = st.selectbox("Location Match (1 = Ya, 0 = Tidak)", [1, 0])
            device_type = st.selectbox("Device Type", ["Desktop", "Mobile", "Tablet"])
            transaction_type = st.selectbox("Transaction Type", ["Online", "POS", "Transfer"])

            # Jika model pakai encoding, ubah jadi angka:
            device_map = {"Desktop": 0, "Mobile": 1, "Tablet": 2}
            transaction_map = {"Online": 0, "POS": 1, "Transfer": 2}

            device_type_encoded = device_map[device_type]
            transaction_type_encoded = transaction_map[transaction_type]

            submitted = st.form_submit_button("🔍 Prediksi")

            if submitted:
                # Gabungkan fitur jadi array
                input_features = np.array([[amount, hour, location_match, device_type_encoded, transaction_type_encoded]])
                
                # Prediksi dengan model
                prediction = model.predict(input_features)[0]
                pred_proba = model.predict_proba(input_features)[0][int(prediction)]

                if prediction == 1:
                    st.error(f"🚨 Transaksi terindikasi **FRAUD** dengan probabilitas {pred_proba:.2%}")
                else:
                    st.success(f"✅ Transaksi **aman** dengan probabilitas {pred_proba:.2%}")

dashboard()