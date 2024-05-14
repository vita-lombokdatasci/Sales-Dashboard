import pandas as pd
import plotly.express as px
import streamlit as st

#TOP
st.set_page_config(
    page_title="SALES DASHBOARD APOTEK",
    page_icon=":bar_chart:",
    layout="wide"
)

dataset1 = pd.read_excel(
    io='ArsipTransaksi.xlsm',
    engine='openpyxl',
    sheet_name='DATA TRANSAKSI',
    usecols='A:I',
    header=1
)
df_month = dataset1.groupby(by=dataset1.Tanggal.dt.month).Jumlah.sum()

dataset2 = pd.read_excel(
    io='ArsipTransaksi.xlsm',
    engine='openpyxl',
    sheet_name='BARANG MASUK',
    usecols='B:M',
    header=4
)
dataset2["Tanggal"] = pd.to_datetime(dataset2["Tanggal"])
df2 = dataset2.groupby(by=dataset2.Tanggal.dt.month).Nilai.sum()

#MAIN PAGE
st.title(":bar_chart: SALES DASHBOARD APOTEK")
st.markdown("####")

#SIDEBAR

#Penjualan
st.sidebar.header("DATA SALES TH BERJALAN")

df_month["Bulan"]=dataset1["Tanggal"].dt.month
tgl = st.sidebar.multiselect(
    "Pilih Bulan",
    options=df_month["Bulan"].unique(),
    default=df_month["Bulan"].unique()
)
df_selection = df_month.to_frame()
df_selection=df_selection.query(
    "Tanggal==@tgl"
)

#Pembelian Obat
st.sidebar.header("PEMBELIAN STOK OBAT")

tgl_beli = st.sidebar.multiselect(
    "pilih Bulan: ",
    options=dataset2["Tanggal"].dt.month.unique(),
    default=dataset2["Tanggal"].dt.month.unique()                  
)
df2["Tanggal"]=dataset2["Tanggal"].dt.month
df2_selection=df2.to_frame()
df2_selection = df2_selection.query(
    "Tanggal==@tgl_beli"
)

#TOP KPI's
total_sales = df_selection["Jumlah"].sum()
total_order =df2_selection["Nilai"].sum() 
gross_profit = total_sales-total_order

top_col1 ,top_col2, top_profit =st.columns(3)
with top_col1:
    st.subheader("Total penjualan:")
    st.subheader(f"Rp. {total_sales:,}")
with top_col2:
    st.subheader("Total pembelian:")
    st.subheader(f"Rp. {total_order:,}")
with top_profit:
    st.subheader("Profit:")
    st.subheader(f"Rp. {gross_profit:,}") 

st.markdown("---")

#Sub KPI
col1, col2,col3,col4 =st.columns(4)
with col1:
    st.markdown("##### Penjualan:")
    st.dataframe(df_selection)
with col2:
    st.markdown("##### Grafik:") 
    sales_grafik = (dataset1.groupby(by=dataset1.Tanggal.dt.month).Jumlah.sum()
                    )
    fig_sales_grafik = px.bar(
        sales_grafik,
        x=sales_grafik.index,
        y="Jumlah",
        orientation="v",
        title="<b>Penjualan th berjalan</b>",
        color_discrete_sequence=["#0083B8"]*len(sales_grafik),
        template="plotly_white",
        )
    st.plotly_chart(fig_sales_grafik)

st.markdown("---")

col2_1, col2_2,col2_3,col2_4 =st.columns(4)
with col2_1:    
        st.markdown("##### Pembelian:")
        st.dataframe(df2_selection) 
with col2_2:
    order_grafik = (dataset2.groupby(by=dataset2.Tanggal.dt.month).Nilai.sum()
                    )
    fig_order_grafik = px.area(
         order_grafik,
         x=order_grafik.index,
         y="Nilai",
         orientation="v",
         title="<b>Pembelian obat th berjalan</b>",
         color_discrete_sequence=["#0083B8"]*len(order_grafik),
         template="plotly_white",
        )
    st.plotly_chart(fig_order_grafik)
        
    
#Style
dashbd_style="""
        <style>
        #MainMenu {visibility : hidden;}
        footer {visibility : hidden;}
        header {visibility : hidden;}
        </style>
        """

st.markdown(dashbd_style, unsafe_allow_html=True)