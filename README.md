# 📈 Semiconductor Raw Material Demand Forecasting Platform

This project presents a demand forecasting platform tailored for the semiconductor manufacturing industry. With the growing complexity of global supply chains—especially amid geopolitical tensions and disruptions such as the U.S.-China trade war, Japan-Korea trade disputes, and the COVID-19 pandemic—accurate demand forecasting of semiconductor raw materials is critical to maintaining operational resilience.

Taiwan, as a key player in the global semiconductor supply chain, heavily relies on imported high-purity raw materials. Any disruption can result in costly production delays and inventory issues. This project aims to support strategic decision-making by applying both traditional time series models and modern machine learning techniques to forecast material needs.

---

## 🎯 Project Objective

To build a user-friendly forecasting tool that:
- Predicts demand for key semiconductor raw materials
- Compares performance across various statistical and machine learning models
- Provides a visual and interactive GUI for business users to upload, analyze, and forecast their own data

---

## 🛠️ Techniques & Tools Used

### 🔢 Forecasting Models
**Traditional Time Series Models:**
- Simple Moving Average (SMA)
- Simple Exponential Smoothing (SES)
- Autoregressive Models (AR)
- ARIMA (Autoregressive Integrated Moving Average)

**Machine Learning Models:**
- Multiple Linear Regression (MLR)
- Nonlinear Regression
- Random Forests
- Support Vector Machines (SVM)
- Adaptive Boosting (AdaBoost)

### 💻 Technologies
- **Language:** Python
- **Libraries:** pandas, scikit-learn, statsmodels, matplotlib, tkinter
- **GUI:** Tkinter (desktop app interface)
- **Data Source:** Proprietary demand data from a semiconductor manufacturer (simulated for this demo)

---

## 🖼️ GUI Screenshots

### 🧩 Forecasting Interface
Upload your historical demand data and select from multiple models to generate predictions.

![User GUI](GUI_image/user_interface.png)

---

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/mocalucy/project.git
   cd project
