# Học thêm tại: https://dash.plotly.com/

# Run this app with `python official_lab_v2.py` and

# visit http://127.0.0.1:8050/ in your web browser.

# BẤM CTRL '+' C ĐỂ TẮT APP ĐANG CHẠY

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# TẢI DỮ LIỆU TỪ FIRESTORE
cred = credentials.Certificate("./iuh-20089981-6c1f2-firebase-adminsdk-otxhy-9dcdeecc3f.json")
appLoadData = firebase_admin.initialize_app(cred)

dbFireStore = firestore.client()

queryResults = list(dbFireStore.collection(u'tblIUHSALES').stream())
listQueryResult = list(map(lambda x: x.to_dict(), queryResults))

df = pd.DataFrame(listQueryResult)

df["YEAR_ID"] = df["YEAR_ID"].astype("str")
df["QTR_ID"] = df["QTR_ID"].astype("str")

# TRỰC QUAN HÓA DỮ LIỆU WEB APP
app = Dash(__name__)

app.title = "Finance Data Analysis"

# CARD S
valueDoanhSoSale = df[["SALES"]].sum().astype("str")

df['LoiNhuan'] =  df['SALES'] - df['QUANTITYORDERED'] * df['PRICEEACH']
valueLoiNhuan = df[["LoiNhuan"]].sum().astype("str")

valueTopDoanhSo = df.groupby(['CATEGORY']).sum()['SALES'].max()
valueTopLoiNhuan = df.groupby(['CATEGORY']).sum()['LoiNhuan'].max()

df_DoanhSo = df.groupby("YEAR_ID").sum()
df_DoanhSo["YEAR_ID"] = df_DoanhSo.index

# CARD M

figDoanhSoTheoNam = px.bar(df_DoanhSo, x="YEAR_ID", y="SALES", title="Doanh số bán hàng theo năm",
labels= {"SALES": "Doanh số", "YEAR_ID": "Từ năm 2003, 2004 và 2005" },
color='YEAR_ID',
height=300)

figDoanhSo_SanPham = px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='SALES',
color='SALES',
labels={'parent':'Năm', 'labels':'Sản phẩm','SALES':'Doanh số'},
title='Tỉ lệ đóng góp doanh số theo từng danh mục',
height= 300
)

figLoiNhuanTheoNam = px.line(df_DoanhSo, x="YEAR_ID", y="LoiNhuan",
title= "Lợi nhuận bán hàng theo năm", labels={"YEAR_ID": "Năm","LoiNhuan": "Lợi nhuận"},
height= 300)

figLoiNhuan_SanPham = px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='LoiNhuan',
color='LoiNhuan',
labels={'parent':'Năm', 'labels':'Sản phẩm','LoiNhuan':'LoiNhuan'},
title='Tỉ lệ đóng góp lợi nhuận theo từng danh mục',
height= 300
)

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1( 
                            children="dashboard"
                        )
                    ], className="header-title"
                ),
                html.Div(
                    children=[
                        html.P(
                            children="Phan Hai Trieu"
                        )
                    ],className="header-description"
                )
            ],className="header"
        ),
        html.Div(
            children=[
                html.Div(
                    children= [
                        html.H4(
                            children= "DOANH SỐ SALES: "
                        ),
                        html.H4(
                            children= valueDoanhSoSale
                        )
                    ], className="value-1 card-s"
                ),
                
                html.Div(
                    children= [
                        html.H4(
                            children= "LỢI NHUẬN: "
                        ),
                        html.H4(
                            children= valueLoiNhuan
                        )
                    ], className="value-2 card-s"
                ),

                html.Div(
                    children= [
                        html.H4(
                            children= "TOP DOANH SỐ: "
                        ),
                        html.H4(
                            children= valueTopDoanhSo
                        )
                    ], className="value-3 card-s"
                ),

                html.Div(
                    children= [
                        html.H4(
                            children= "TOP LỢI NHUẬN: "
                        ),
                        html.H4(
                            children= valueTopLoiNhuan
                        )
                    ], className="value-4 card-s"
                ),
                

                html.Div(
                    children=dcc.Graph(
                    id='doanhsotheonam-graph',
                    figure=figDoanhSoTheoNam),
                    className="value-5 card-m"
                ),
                html.Div(
                    children=dcc.Graph(
                    id='DoanhSo_SanPham-graph',
                    figure=figDoanhSo_SanPham),
                    className="value-6 card-m"
                ),
                html.Div(
                    children=dcc.Graph(
                    id='LoiNhuantheonam-graph',
                    figure=figLoiNhuanTheoNam),
                    className="value-7 card-m"
                ),
                html.Div(
                    children=dcc.Graph(
                    id='LoiNhuan_SanPham-graph',
                    figure=figLoiNhuan_SanPham),
                    className="value-8 card-m"
                )     
            ], className="wrapper"
        )
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True, port=8090)