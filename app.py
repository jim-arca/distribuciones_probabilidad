import streamlit as st
import numpy as np

# --- Configuración de la Página ---
# Esto se aplica a TODAS las páginas de la aplicación
st.set_page_config(
    page_title="Explorador de Distribuciones",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Contenido de la Página Principal (app.py) ---
# Esta será nuestra página de "Fundamentos".
# Streamlit la mostrará como la página principal.

st.title("Fundamentos de Probabilidad")
st.sidebar.success("Selecciona una distribución desde la barra lateral.")

st.markdown("Esta sección introduce los conceptos básicos necesarios para entender las distribuciones de probabilidad.")

st.header("Variable Aleatoria Discreta vs. Continua")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Variable Aleatoria Discreta")
    st.write("""
    Una variable aleatoria discreta es aquella que solo puede tomar un número finito o infinito contable de valores.
    Estos valores suelen ser enteros y a menudo provienen de un proceso de *conteo*.
    
    - **Ejemplo 1:** El número de caras obtenidas al lanzar una moneda 3 veces (valores: 0, 1, 2, 3).
    - **Ejemplo 2:** El número de clientes que llegan a una tienda en una hora (valores: 0, 1, 2, ...).
    - **Ejemplo 3:** El número de defectos en un lote de producción.
    """)
    
with col2:
    st.subheader("Variable Aleatoria Continua")
    st.write("""
    Una variable aleatoria continua es aquella que puede tomar un número infinito (no contable) de valores dentro de un rango.
    Estos valores suelen provenir de un proceso de *medición*.
    
    - **Ejemplo 1:** La altura de una persona (ej. 1.753... metros).
    - **Ejemplo 2:** El tiempo que tarda un programa en ejecutarse (ej. 12.45... segundos).
    - **Ejemplo 3:** La temperatura exacta en un momento dado.
    """)

st.header("Función de Masa de Probabilidad (PMF)")
st.write("""
Para una **variable aleatoria discreta** $X$, la Función de Masa de Probabilidad (PMF) nos da la probabilidad de que $X$ sea exactamente igual a un valor específico $k$.
""")
st.latex(r"p(k) = P(X = k)")
st.write("""
Propiedades de una PMF:
1. $0 \le p(k) \le 1$ para todo $k$.
2. La suma de las probabilidades para todos los valores posibles de $k$ debe ser 1: $\sum_{k} p(k) = 1$.
""")

st.header("Función de Densidad de Probabilidad (PDF)")
st.write("""
Para una **variable aleatoria continua** $X$, la Función de Densidad de Probabilidad (PDF), denotada como $f(x)$, describe la *densidad* de probabilidad en un punto $x$.

**Importante:** La PDF no es una probabilidad. $f(x)$ puede ser mayor que 1. La probabilidad de que $X$ sea *exactamente* igual a un valor es 0 (ej. $P(X = 1.5) = 0$).

La probabilidad se obtiene *integrando* la PDF sobre un rango:
""")
st.latex(r"P(a \le X \le b) = \int_{a}^{b} f(x) \,dx")
st.write("""
Propiedades de una PDF:
1. $f(x) \ge 0$ para todo $x$.
2. El área total bajo la curva de la PDF debe ser 1: $\int_{-\infty}^{\infty} f(x) \,dx = 1$.
""")

st.header("Función de Distribución Acumulada (CDF)")
st.write("""
La Función de Distribución Acumulada (CDF), $F(x)$, es válida para **ambos tipos** de variables (discretas y continuas).
Define la probabilidad de que la variable aleatoria $X$ tome un valor *menor o igual* a $x$.
""")
st.latex(r"F(x) = P(X \le x)")

st.subheader("Para variables discretas:")
st.latex(r"F(x) = \sum_{k \le x} P(X = k)")
st.write("La CDF es una función escalonada.")

st.subheader("Para variables continuas:")
st.latex(r"F(x) = \int_{-\infty}^{x} f(t) \,dt")
st.write("La CDF es una función continua y es la integral (antiderivada) de la PDF.")
