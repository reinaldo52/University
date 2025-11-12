
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar dataset
df = pd.read_csv('university_student_data.csv')

st.title("Panel Interactivo de Indicadores Universitarios")

# Filtros interactivos
years = st.multiselect("Seleccione el año:", sorted(df["Year"].unique()), default=df["Year"].unique())
terms = st.multiselect("Seleccione el semestre:", df["Term"].unique(), default=df["Term"].unique())
departments = ["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"]
selected_dept = st.selectbox("Seleccione un departamento:", departments)

# Filtrar datos según selección
filtered_df = df[(df["Year"].isin(years)) & (df["Term"].isin(terms))]

# KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("Promedio Retención (%)", round(filtered_df["Retention Rate (%)"].mean(), 2))
col2.metric("Satisfacción Promedio (%)", round(filtered_df["Student Satisfaction (%)"].mean(), 2))
col3.metric(f"Total {selected_dept.split()[0]} Enrolled", int(filtered_df[selected_dept].sum()))

# Gráfico de línea: Tasa de Retención 
st.subheader("Tendencia de la Tasa de Retención por Año")
retention = filtered_df.groupby("Year")["Retention Rate (%)"].mean().reset_index()
fig1, ax1 = plt.subplots()
sns.lineplot(data=retention, x="Year", y="Retention Rate (%)", marker="o", ax=ax1)
ax1.set_title("Tendencia de Retención")
st.pyplot(fig1)

# Gráfico de barras: Satisfacción Estudiantil 
st.subheader("Satisfacción Estudiantil por Semestre")
satisfaction = filtered_df.groupby("Term")["Student Satisfaction (%)"].mean().reset_index()
fig2, ax2 = plt.subplots()
sns.barplot(data=satisfaction, x="Term", y="Student Satisfaction (%)", palette="coolwarm", ax=ax2)
ax2.set_title("Satisfacción Estudiantil por Semestre")
st.pyplot(fig2)

# Gráfico circular: Distribución por Departamento 
st.subheader("Distribución de Estudiantes por Departamento")
dept_data = filtered_df[departments].sum()
fig3, ax3 = plt.subplots()
ax3.pie(dept_data, labels=[d.split()[0] for d in departments], autopct='%1.1f%%', startangle=90)
ax3.axis("equal")
st.pyplot(fig3)

st.caption("Los gráficos y métricas se actualizan dinámicamente según los filtros seleccionados.")
