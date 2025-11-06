import streamlit as st
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Importamos la función de ayuda desde el archivo helpers.py
# El '..' le dice a Python que suba un nivel de directorio para encontrar helpers.py
# (Esto puede variar según el entorno, si falla, prueba 'from helpers import ...')
try:
    from helpers import plot_discrete_distribution
except ImportError:
    st.error("No se pudo importar 'helpers.py'. Asegúrate de que esté en el directorio raíz.")
    st.stop()


# --- Contenido de la Página de Bernoulli ---
# Nota: No hay 'def show_bernoulli():'
# El archivo se ejecuta directamente.

st.title("Distribución de Bernoulli")

# Usar pestañas para organizar el contenido
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teoría y Fórmulas", "Visualización", "Calculadora", "Ejemplos", "Ejercicios"
])

with tab1:
    st.header("Concepto Teórico")
    st.write("""
    La Distribución de Bernoulli es la distribución discreta más simple. Modela un experimento aleatorio que tiene exactamente dos resultados posibles: "éxito" (con probabilidad $p$) y "fracaso" (con probabilidad $1-p$).
    
    Un solo intento (ej. lanzar una moneda, un paciente sobrevive, un producto es defectuoso) se llama un **ensayo de Bernoulli**.
    
    - **Parámetro:** $p$ (probabilidad de éxito), donde $0 \le p \le 1$.
    - **Rango:** La variable $X$ solo puede tomar dos valores: $1$ (éxito) o $0$ (fracaso).
    """)

    st.header("Contexto Histórico y Casos de Uso")
    st.write("Nombrada en honor al matemático suizo **Jakob Bernoulli** (1654-1705), quien la introdujo en su obra *Ars Conjectandi* (El Arte de la Conjetura), publicada póstumamente en 1713.")
    st.markdown("""
    **Casos de Uso:**
    - El resultado de lanzar una moneda (Cara = 1, Sello = 0).
    - Un control de calidad (Producto defectuoso = 1, No defectuoso = 0).
    - Un paciente responde a un tratamiento (Responde = 1, No responde = 0).
    - Un cliente hace clic en un anuncio (Clic = 1, No clic = 0).
    """)

    st.header("Relación con Otras Distribuciones")
    st.write("""
    - **Binomial:** La Distribución Binomial es simplemente la **suma de $n$ ensayos de Bernoulli independientes** e idénticos. Una Binomial(n, p) describe el número total de éxitos en $n$ intentos.
    - **Geométrica:** Describe el número de ensayos de Bernoulli necesarios hasta obtener el *primer* éxito.
    """)

    st.header("Fórmulas Matemáticas")
    st.subheader("Función de Masa de Probabilidad (PMF)")
    st.latex(r"""
    P(X=k) = 
    \begin{cases} 
    p & \text{si } k=1 \text{ (éxito)} \\
    1-p & \text{si } k=0 \text{ (fracaso)}
    \end{cases}
    """)
    st.write("O de forma más compacta:")
    st.latex(r"P(X=k) = p^k (1-p)^{1-k} \quad \text{para } k \in \{0, 1\}")
    
    st.subheader("Media (Valor Esperado)")
    st.latex(r"\mu = E[X] = p")
    
    st.subheader("Varianza")
    st.latex(r"\sigma^2 = \text{Var}(X) = p(1-p)")

with tab2:
    st.header("Visualización Interactiva")
    st.write("Ajusta la probabilidad de éxito ($p$) para ver cómo cambian las probabilidades de éxito (k=1) y fracaso (k=0).")
    
    # key='bern_p_slider' es único para esta página, así que no hay conflicto
    p_slider = st.slider("Probabilidad de éxito (p)", min_value=0.0, max_value=1.0, value=0.5, step=0.01, key='bern_p_slider')
    
    # Validación
    if not (0 <= p_slider <= 1):
        st.error("La probabilidad 'p' debe estar entre 0 y 1.")
    else:
        try:
            dist = stats.bernoulli(p=p_slider)
            k_values = [0, 1]
            # Usamos la función de ayuda importada
            fig = plot_discrete_distribution(dist, k_values, f"PMF de Bernoulli (p={p_slider:.2f})")
            st.pyplot(fig)
            plt.close(fig) # Liberar memoria
        except Exception as e:
            st.error(f"Error al generar el gráfico: {e}")

with tab3:
    st.header("Calculadora Interactiva")
    st.write("Calcula la probabilidad para un único ensayo de Bernoulli.")
    
    calc_p = st.number_input("Probabilidad de éxito (p)", min_value=0.0, max_value=1.0, value=0.5, step=0.01, key='bern_calc_p')
    
    # Validación
    if not (0 <= calc_p <= 1):
        st.error("La probabilidad 'p' debe estar entre 0 y 1.")
    else:
        try:
            dist = stats.bernoulli(p=calc_p)
            st.subheader("Resultados:")
            st.markdown(f"**P(X = 1) (Éxito):** `{dist.pmf(1):.4f}`")
            st.markdown(f"**P(X = 0) (Fracaso):** `{dist.pmf(0):.4f}`")
            
            st.subheader("Estadísticos:")
            st.markdown(f"**Media (μ):** `{dist.mean():.4f}`")
            st.markdown(f"**Varianza (σ²):** `{dist.var():.4f}`")
            st.markdown(f"**Desviación Estándar (σ):** `{dist.std():.4f}`")
            
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

with tab4:
    st.header("Ejemplos Aplicados")
    st.markdown("""
    1.  **Medicina:** Un nuevo fármaco tiene una probabilidad de 0.75 de curar a un paciente. El resultado de un solo paciente (curado o no) sigue una distribución de Bernoulli(p=0.75).
    2.  **Marketing:** Un correo electrónico de marketing tiene una tasa de apertura del 15%. Que un destinatario específico abra o no el correo sigue una Bernoulli(p=0.15).
    3.  **Juegos de Azar:** La probabilidad de que una ruleta (europea) caiga en 'Rojo' es 18/37 (aprox. 0.486). Una sola apuesta al 'Rojo' es un ensayo de Bernoulli(p=0.486).
    """)

with tab5:
    st.header("Ejercicios Interactivos")
    
    st.subheader("Ejercicio 1")
    st.write("Si la probabilidad de que un estudiante apruebe un examen es del 80% (p=0.8), ¿cuál es la probabilidad de que *falle* (k=0)?")
    ans1 = st.number_input("Tu respuesta (P(X=0)):", min_value=0.0, max_value=1.0, step=0.01, format="%.2f", key='bern_ex1_ans')
    if st.button("Revisar 1", key='bern_ex1_btn'):
        if np.isclose(ans1, 0.20):
            st.success("¡Correcto!")
        else:
            st.error(f"Incorrecto. La respuesta correcta es 0.20.")
        with st.expander("Ver Solución"):
            st.write("Si $p$ (éxito) = 0.8, entonces $1-p$ (fracaso) = 1 - 0.8 = 0.20.")
    
    st.subheader("Ejercicio 2")
    st.write("Un ensayo de Bernoulli tiene una varianza de 0.21. ¿Cuál es la probabilidad de éxito $p$? (Pista: $p(1-p) = 0.21$).")
    ans2 = st.number_input("Tu respuesta (p > 0.5):", min_value=0.0, max_value=1.0, step=0.01, format="%.2f", key='bern_ex2_ans')
    if st.button("Revisar 2", key='bern_ex2_btn'):
        if np.isclose(ans2, 0.70) or np.isclose(ans2, 0.30):
            st.success("¡Correcto! Las dos posibles soluciones son 0.3 y 0.7. Si asumimos p > 0.5, es 0.7.")
        else:
            st.error(f"Incorrecto. Intenta resolver $p - p^2 = 0.21$.")
        with st.expander("Ver Solución"):
            st.write("Resolvemos la ecuación cuadrática $p^2 - p + 0.21 = 0$. Las raíces son $(1 \pm \sqrt{1 - 4(0.21)}) / 2 = (1 \pm \sqrt{0.16}) / 2 = (1 \pm 0.4) / 2$. Las soluciones son $p=0.7$ y $p=0.3$.")

    st.subheader("Ejercicio 3")
    st.write("¿Cuál es la media (valor esperado) de una distribución de Bernoulli con p=0.45?")
    ans3 = st.number_input("Tu respuesta (Media μ):", min_value=0.0, max_value=1.0, step=0.01, format="%.2f", key='bern_ex3_ans')
    if st.button("Revisar 3", key='bern_ex3_btn'):
        if np.isclose(ans3, 0.45):
            st.success("¡Correcto!")
        else:
            st.error(f"Incorrecto. La respuesta es 0.45.")
        with st.expander("Ver Solución"):
            st.write("Para una distribución de Bernoulli, la media (μ) es simplemente igual a $p$. Por lo tanto, μ = 0.45.")
