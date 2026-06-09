import streamlit as st
import pandas as pd
import plotly.express as px

# 設定頁面風格
st.set_page_config(page_title="理智購車決策系統", layout="wide")

# 1. 核心數據庫
car_data = {
    "Volvo_XC60": {
        "maint": [0, 21000, 21000, 29769, 31704],
        "fuel": 32000, "tax": 17410, "ins": 25000, "tire": 35000
    },
    "KIA_Sportage": {
        "maint": [0, 6000, 6000, 6000, 12000],
        "fuel": 16216, "tax": 11920, "ins": 25000, "tire": 26000
    }
}

# 2. 側邊欄輸入
st.sidebar.header("⚙️ 參數微調")
years = st.sidebar.slider("評估年限 (年)", 1, 5, 5)

# 3. 主頁計算
v_m, v_f, v_t, v_i, v_tire = [sum(car_data["Volvo_XC60"]["maint"][:years]), 
                              car_data["Volvo_XC60"]["fuel"] * years, 
                              car_data["Volvo_XC60"]["tax"] * years, 
                              car_data["Volvo_XC60"]["ins"] * years, 
                              car_data["Volvo_XC60"]["tire"]]

k_m, k_f, k_t, k_i, k_tire = [sum(car_data["KIA_Sportage"]["maint"][:years]), 
                              car_data["KIA_Sportage"]["fuel"] * years, 
                              car_data["KIA_Sportage"]["tax"] * years, 
                              car_data["KIA_Sportage"]["ins"] * years, 
                              car_data["KIA_Sportage"]["tire"]]

# 4. 呈現美化
st.title("🚗 購車理智殺手系統")
col1, col2 = st.columns(2)

with col1:
    st.subheader("費用對比圖")
    df = pd.DataFrame({
        "項目": ["保養", "油錢", "稅金", "保險", "輪胎"],
        "Volvo (舊)": [v_m, v_f, v_t, v_i, v_tire],
        "KIA (新)": [k_m, k_f, k_t, k_i, k_tire]
    }).melt(id_vars="項目", var_name="車款", value_name="金額")
    
    fig = px.bar(df, x="項目", y="金額", color="車款", barmode="group", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("理智診斷")
    net_diff = (v_m + v_f + v_t + v_i + v_tire) - (k_m + k_f + k_t + k_i + k_tire)
    st.metric("換車 5 年累積省下營運費", f"{net_diff:,.0f} 元")
    
    if net_diff > 0:
        st.success("✅ 恭喜！新車營運成本更低，在燃油與保養上非常有優勢。")
    else:
        st.warning("⚠️ 警告：以目前的行駛里程，新車省下的費用不足以覆蓋車價折舊，建議三思。")
    
    st.info("💡 貼心提示：此處僅計算『營運成本』，尚未計入買車的貸款利息與車價折舊差額，請務必綜合考量。")