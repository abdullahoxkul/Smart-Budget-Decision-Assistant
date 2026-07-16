import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from database import create_table, add_expense, get_all_expenses, delete_expense, set_income, get_income

import analysis as an

st.set_page_config(page_title="Smart Budget Assistant", page_icon="💰", layout="wide")
create_table()

texts = {
    "Türkçe": {
        "title": "💰 Akıllı Bütçe ve Karar Asistanı",
        "subtitle": "Harcamalarını takip et ve bütçeni veriyle yönet!",
        "income_for": "🏦 {month} Ayı Geliri (TL)",
        "update_income": "Geliri Kaydet / Güncelle",
        "new_expense": "Yeni Harcama Ekle",
        "date": "Tarih",
        "desc": "Harcama Açıklaması",
        "cat": "Kategori",
        "amount": "Tutar (TL)",
        "save": "Harcamayı Kaydet",
        "success": "✅ Başarılı! {name} kaydedildi.",
        "error": "Lütfen harcama adını ve geçerli bir tutar girin.",
        "summary": "📊 Aylık Bütçe Özeti",
        "select_month": "İncelenecek Ayı Seçin",
        "total_income": "Toplam Gelir",
        "total_spent": "Toplam Harcama",
        "remaining": "Kalan Bakiye",
        "history": "**Seçili Ayın Harcama Geçmişi:**",
        "distribution": "**Seçili Ayın Harcama Dağılımı:**",
        "empty": "Bu ay için kaydedilmiş bir harcama bulunmuyor.",
        "categories": ["Yemek", "Ulaşım", "Spor", "Eğitim", "Oyun & Eğlence", "Yatırım", "Diğer"],
        "col_date": "Tarih",
        "col_name": "İsim",
        "col_cat": "Kategori",
        "col_amount": "Miktar",
        "del_title": "🗑️ Harcama Sil",
        "del_select": "Silmek İstediğiniz Harcamayı Seçin",
        "del_btn": "Harcamayı Sil",
        "insights_title": "🧠 Akıllı Analiz & Öngörüler",
        "deviation_label": "Bütçe Dalgalanması (Standart Sapma)",
        "deviation_desc": "Düşük değer harcama disiplininizin kararlı olduğunu gösterir.",
        "savings_label": "Tasarruf Oranı"
    },
    "English": {
        "title": "💰 Smart Budget & Decision Assistant",
        "subtitle": "Track your expenses and manage your budget with data!",
        "income_for": "🏦 Income for {month} (TL)",
        "update_income": "Save / Update Income",
        "new_expense": "Add New Expense",
        "date": "Date",
        "desc": "Expense Description",
        "cat": "Category",
        "amount": "Amount (TL)",
        "save": "Save Expense",
        "success": "✅ Success! {name} has been saved.",
        "error": "Please enter a valid name and amount.",
        "summary": "📊 Monthly Budget Summary",
        "select_month": "Select Month to Review",
        "total_income": "Total Income",
        "total_spent": "Total Spent",
        "remaining": "Remaining Balance",
        "history": "**Expense History for Selected Month:**",
        "distribution": "**Expense Distribution for Selected Month:**",
        "empty": "No expenses recorded for this month.",
        "categories": ["Food", "Transport", "Sports", "Education", "Gaming", "Investment", "Other"],
        "col_date": "Date",
        "col_name": "Name",
        "col_cat": "Category",
        "col_amount": "Amount",
        "del_title": "🗑️ Delete Expense",
        "del_select": "Select an Expense to Delete",
        "del_btn": "Delete Expense",
        "insights_title": "🧠 Smart Insights & Forecasts",
        "deviation_label": "Budget Fluctuation (Std Deviation)",
        "deviation_desc": "Lower values indicate stable spending discipline.",
        "savings_label": "Savings Rate"
    }
}

st.sidebar.title("⚙️ Ayarlar / Settings")
selected_language = st.sidebar.selectbox("🌐 Language / Dil", ["Türkçe", "English"])
t = texts[selected_language]

st.title(t["title"])
st.write(t["subtitle"])
st.divider()

all_expenses = get_all_expenses()
current_month_str = date.today().strftime("%Y-%m")

if all_expenses:
    df = pd.DataFrame(all_expenses, columns=["rowid", t["col_date"], t["col_name"], t["col_cat"], t["col_amount"]])
    df["Date_Obj"] = pd.to_datetime(df[t["col_date"]])
    df["Ay_Yıl"] = df["Date_Obj"].dt.strftime("%Y-%m")
    unique_months = sorted(df["Ay_Yıl"].unique(), reverse=True)
else:
    df = pd.DataFrame()
    unique_months = []

if current_month_str not in unique_months:
    unique_months.insert(0, current_month_str)

st.subheader(t["summary"])
selected_month = st.selectbox(t["select_month"], unique_months)

saved_income = get_income(selected_month)

st.sidebar.divider()
st.sidebar.markdown(f"**{t['income_for'].format(month=selected_month)}**")

new_income = st.sidebar.number_input("", value=float(saved_income), min_value=0.0, step=100.0, format="%g")

if st.sidebar.button(t["update_income"]):
    set_income(selected_month, new_income)
    st.rerun()

if not df.empty:
    filtered_df = df[df["Ay_Yıl"] == selected_month]
    total_spent = filtered_df[t["col_amount"]].sum()
    
    stats = an.calculate_summary_statistics(filtered_df, saved_income)
    std_dev = stats["std_deviation"]
    savings_rate = stats["savings_rate"]
else:
    filtered_df = pd.DataFrame()
    total_spent = 0.0
    std_dev = 0.0
    savings_rate = 0.0
    stats = {"daily_average": 0.0, "std_deviation": 0.0}

remaining_balance = saved_income - total_spent

col1, col2, col3 = st.columns(3)
col1.metric(t["total_income"], f"{saved_income:,.2f} TL")
col2.metric(t["total_spent"], f"{total_spent:,.2f} TL")
col3.metric(t["remaining"], f"{remaining_balance:,.2f} TL", delta=float(remaining_balance))

if not filtered_df.empty:
    st.markdown(f"### {t['insights_title']}")
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    
    with col_stats1:
        st.info(f"📊 **{t['deviation_label']}:**\n\n{std_dev:,.2f} TL\n\n*{t['deviation_desc']}*")
        
    with col_stats2:
        st.success(f"📈 **{t['savings_label']}:**\n\n%{savings_rate:.1f}")
        
    with col_stats3:
        prediction = an.predict_month_end_spend(filtered_df)
        if prediction is not None:
            pred_text_tr = f"🔮 **Ay Sonu Öngörüsü:**\n\n{prediction:,.2f} TL\n\n*Mevcut gidişata göre tahmin edilen toplam bütçe.*"
            pred_text_en = f"🔮 **Month-End Forecast:**\n\n{prediction:,.2f} TL\n\n*Estimated budget usage based on current trends.*"
            st.warning(pred_text_tr if selected_language == "Türkçe" else pred_text_en)
        else:
            info_tr = "🔮 **Öngörü Modeli:**\n\nEn az 3 farklı günün harcama verisi girildiğinde tahmin çalışacaktır."
            info_en = "🔮 **Forecasting Model:**\n\nNeed at least 3 different days of data to forecast."
            st.info(info_tr if selected_language == "Türkçe" else info_en)

st.divider()

with st.expander(t["new_expense"], expanded=True):
    with st.form("expense_form", clear_on_submit=True):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            expense_date = st.date_input(t["date"], date.today())
            expense_name = st.text_input(t["desc"])
        with col_f2:
            selected_category = st.radio(t["cat"], t["categories"], horizontal=True)
            expense_amount = st.number_input(t["amount"], min_value=0.0, step=10.0, format="%g")
        
        if expense_amount > 0:
            st.markdown("---")
            coach_title = "🤖 Akıllı Bütçe Koçu Analizi:" if selected_language == "Türkçe" else "🤖 Smart Budget Coach Analysis:"
            st.markdown(f"#### {coach_title}")
            
            rationality = an.evaluate_spending_rationality(expense_amount, stats, remaining_balance, saved_income)
            msg = rationality["message_tr"] if selected_language == "Türkçe" else rationality["message_en"]
            status = rationality["status"]
            
            if status == "Critical":
                st.error(msg)
            elif status == "High Risk":
                st.warning(msg)
            elif status == "Medium Risk":
                st.info(msg)
            else:
                st.success(msg)
                
            after_expense_balance = remaining_balance - expense_amount
            sim_text_tr = f"💡 **İşlem Sonrası Tahmini Kalan Bakiye:** {after_expense_balance:,.2f} TL"
            sim_text_en = f"💡 **Estimated Balance After Transaction:** {after_expense_balance:,.2f} TL"
            
            if after_expense_balance < 0:
                st.caption(f"🚨 :red[{sim_text_tr if selected_language == 'Türkçe' else sim_text_en}]")
            else:
                st.caption(f":green[{sim_text_tr if selected_language == 'Türkçe' else sim_text_en}]")
            st.markdown("---")
                
        save_button = st.form_submit_button(t["save"])

    if save_button:
        if expense_name and expense_amount > 0:
            add_expense(expense_date.strftime("%Y-%m-%d"), expense_name, selected_category, expense_amount)
            st.success(t["success"].format(name=expense_name))
            st.rerun()
        else:
            st.error(t["error"])

st.divider()

col_chart, col_table = st.columns([1, 1])

with col_chart:
    st.write(t["distribution"])
    
    anomalies = an.detect_category_anomalies(df, selected_month, t["col_cat"], t["col_amount"])
    if anomalies:
        for anomaly in anomalies:
            cat_name = anomaly["category"]
            perc = anomaly["percentage"]
            
            if selected_language == "Türkçe":
                st.warning(f"🚨 **{cat_name}** kategorisinde normalin çok üstündesiniz! Geçmiş ayların ortalamasına göre **%{perc:.1f}** daha fazla harcama yaptınız.")
            else:
                st.warning(f"🚨 Spending in **{cat_name}** is well above normal! You've spent **{perc:.1f}%** more than your historical average.")
    
    if not filtered_df.empty:
        category_df = filtered_df.groupby(t["col_cat"])[t["col_amount"]].sum().reset_index()
        fig = px.pie(category_df, values=t["col_amount"], names=t["col_cat"], hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(t["empty"])
        
with col_table:
    st.write(t["history"])
    if not filtered_df.empty:
        display_df = filtered_df.drop(columns=["rowid", "Date_Obj", "Ay_Yıl"])
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info(t["empty"])
        
st.divider()

title_trend = "**Günlük Harcama Trendi:**" if selected_language == "Türkçe" else "**Daily Spending Trend (Burn-down):**"

st.write(title_trend)
if not filtered_df.empty:
    daily_trend = filtered_df.groupby(t["col_date"])[t["col_amount"]].sum().reset_index()
    daily_trend = daily_trend.sort_values(by=t["col_date"])
    daily_trend["Kümülatif"] = daily_trend[t["col_amount"]].cumsum()
    
    fig_trend = px.line(
        daily_trend, 
        x=t["col_date"], 
        y="Kümülatif", 
        markers=True,
        labels={t["col_date"]: t["date"], "Kümülatif": t["total_spent"]}
    )
    
    fig_trend.update_traces(line_color="#EF553B", marker=dict(size=8))
    
    y_max = max(saved_income, daily_trend["Kümülatif"].max()) * 1.1 if saved_income > 0 else daily_trend["Kümülatif"].max() * 1.2
    
    fig_trend.update_layout(
        yaxis=dict(range=[0, y_max]),
        xaxis=dict(
            tickformat="%Y-%m-%d",
            dtick="86400000"
        )
    )

    if saved_income > 0:
        limit_text = "Aylık Gelir Limiti" if selected_language == "Türkçe" else "Monthly Income Limit"
        fig_trend.add_hline(
            y=saved_income, 
            line_dash="dash", 
            line_color="#00CC96", 
            annotation_text=limit_text, 
            annotation_position="top left"
        )
        
    st.plotly_chart(fig_trend, use_container_width=True)
else:
    st.info(t["empty"])

st.divider()

if not filtered_df.empty:
    st.subheader(t["del_title"])
    expense_options = {f"{row[t['col_date']]} | {row[t['col_name']]} | {row[t['col_amount']]} TL": row["rowid"] for index, row in filtered_df.iterrows()}
    
    selected_for_deletion = st.selectbox(t["del_select"], list(expense_options.keys()))
    delete_button = st.button(t["del_btn"])
    
    if delete_button:
        row_id_to_delete = expense_options[selected_for_deletion]
        delete_expense(row_id_to_delete)
        st.rerun()