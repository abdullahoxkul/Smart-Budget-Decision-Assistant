import pandas as pd 
import numpy as np
from sklearn.linear_model import LinearRegression


def calculate_summary_statistics(df, income):
    if df.empty:
        return {
            "total_spent": 0.0,
            "daily_average": 0.0,
            "std_deviation": 0.0,
            "savings_rate": 0.0
        }
    date_col = df.columns[1]
    amount_col = df.columns[4]

    total_spent = float(df[amount_col].sum())

    daily_sums = df.groupby(date_col)[amount_col].sum()

    daily_average= float(daily_sums.mean())

    if len(daily_sums) > 1:
        std_deviation = float(daily_sums.std())
    else: 
        std_deviation = 0.0

    if income > 0: 
        savings_rate= float(((income- total_spent)/ income)*100)
    else: 
        savings_rate = 0.0
    
    return {
        "total_spent": total_spent,
        "daily_average": daily_average,
        "std_deviation": std_deviation,
        "savings_rate": savings_rate
    }

def predict_month_end_spend(df):
    if len(df) < 3:
        return None

    date_col = df.columns[1]
    amount_col = df.columns[4]

    df_sorted = df.copy()
    df_sorted[date_col] = pd.to_datetime(df_sorted[date_col])
    df_sorted = df_sorted.sort_values(by=date_col)

    first_date = df_sorted[date_col].min()
    df_sorted['day_index']= (df_sorted[date_col]- first_date).dt.days

    daily_data = df_sorted.groupby('day_index')[amount_col].sum().reset_index()
    daily_data['cumulative_spent'] = daily_data[amount_col].cumsum()

    X = daily_data[['day_index']].values
    y = daily_data['cumulative_spent'].values

    model = LinearRegression() 
    model.fit(X,y)

    predicted_value= model.predict([[30]])[0]
    
    return float(max(0.0 , predicted_value))


def evaluate_spending_rationality(proposed_amount, stats, remaining_balance, income):
    daily_average = stats.get("daily_average", 0.0)
    std_deviation = stats.get("std_deviation", 0.0)
    
    threshold = daily_average + (2 * std_deviation) if std_deviation > 0 else (daily_average * 1.5 if daily_average > 0 else 500.0)
    
    result = {
        "status": "",
        "message_tr": "",
        "message_en": ""
    }
    
    if proposed_amount > remaining_balance and remaining_balance > 0:
        result["status"] = "Critical"
        result["message_tr"] = f"🤖 KOÇ UYARISI (RED): Bu harcama ({proposed_amount:,.2f} TL), kalan bakiyenizi ({remaining_balance:,.2f} TL) aşıyor! Bu işlemi yaparsanız bütçeniz açık verecek."
        result["message_en"] = f"🤖 AI COACH (DENIED): This expense ({proposed_amount:,.2f} TL) exceeds your remaining balance ({remaining_balance:,.2f} TL)!"
        
    elif proposed_amount > (remaining_balance * 0.5) and remaining_balance > 0:
        result["status"] = "High Risk"
        result["message_tr"] = f"⚠️ KOÇ UYARISI (KRİTİK): Bakiyeniz yetiyor ancak tek bir harcamayla kalan paranızın %50'sinden fazlasını harcamak üzeresiniz! Ay sonuna kadar zorlanabilirsiniz."
        result["message_en"] = f"⚠️ AI COACH (CRITICAL): You are about to spend over 50% of your remaining balance in a single transaction! Proceed with caution."
        
    elif proposed_amount > threshold:
        result["status"] = "Medium Risk"
        result["message_tr"] = f"🔔 KOÇ UYARISI (ANOMALİ): Bakiyeniz bu işlem için yeterli. Ancak bu tutar sizin günlük harcama standartlarınızın çok üzerinde."
        result["message_en"] = f"🔔 AI COACH (ANOMALY): You have enough balance, but this amount is significantly higher than your usual daily spending habits."
        
    else:
        result["status"] = "Safe"
        result["message_tr"] = "✅ FİNANSAL KOÇ ONAYI: Harcama bütçenize, kalan bakiyenize ve harcama hızınıza tamamen uygun. Afiyet olsun!"
        result["message_en"] = "✅ AI COACH APPROVED: This expense fits well within your budget, balance, and spending velocity."
        
    return result

def detect_category_anomalies(df, current_month, cat_col, amount_col, month_col="Ay_Yıl"):
    """
    Geçmiş ayların kategori ortalamalarını bulup, seçili ayla kıyaslar ve anormallikleri tespit eder.
    """
    if df.empty or month_col not in df.columns:
        return []
        
    past_df = df[df[month_col] < current_month]
    current_df = df[df[month_col] == current_month]
    
    if past_df.empty or current_df.empty:
        return [] 
        
    past_months_count = past_df[month_col].nunique()
    
    past_cat_totals = past_df.groupby(cat_col)[amount_col].sum()
    past_cat_avg = past_cat_totals / past_months_count
    
    current_cat_totals = current_df.groupby(cat_col)[amount_col].sum()
    
    anomalies = []
    for cat, current_total in current_cat_totals.items():
        if cat in past_cat_avg and past_cat_avg[cat] > 0:
            past_avg = past_cat_avg[cat]
            if current_total > past_avg * 1.2: 
                percentage_inc = ((current_total - past_avg) / past_avg) * 100
                anomalies.append({
                    "category": cat,
                    "percentage": percentage_inc,
                    "current": current_total,
                    "past_avg": past_avg
                })
                
    anomalies = sorted(anomalies, key=lambda x: x["percentage"], reverse=True)
    return anomalies