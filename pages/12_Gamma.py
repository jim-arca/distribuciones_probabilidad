import streamlit as st
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Importamos la función de ayuda
try:
    from helpers import plot_continuous_distribution
except ImportError:
    st.error("No se pudo importar 'helpers.py'. Asegúrate de que esté en el directorio raíz.")
    st.stop()

# --- Contenido de la Página ---

st.title("Distribución Gamma")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teoría y Fórmulas", "Visualización", "Calculadora", "Ejemplos", "Ejercicios"
])

with tab1:
    st.header("Concepto Teórico")
    st.write("""
    La Distribución Gamma es una distribución continua de dos parámetros que es una generalización de la Exponencial.
    
    Mientras la Exponencial modela el tiempo de espera hasta *un* evento de Poisson, la Gamma modela el tiempo de espera hasta que ocurran $\alpha$ (alfa) eventos.
    
    Es una distribución muy flexible, definida solo para valores positivos, y puede ser sesgada (como la Exponencial) o tener forma de campana (parecida a la Normal).
    
    - **Parámetros:**
        - $\alpha$ (alfa): El parámetro de **forma** (o $k$). Controla la forma de la curva.
        - $\beta$ (beta): El parámetro de **escala** (o $\theta$). Controla la dispersión.
    - **Rango:** La variable $X$ puede tomar cualquier valor real $x \ge 0$.
    """)
    st.info("Nota: SciPy usa $\alpha$ como `a` y $\beta$ como `scale`.")

    st.header("Contexto Histórico y Casos de Uso")
    st.write("Se usa en una amplia variedad de campos para modelar tiempos de espera y variables sesgadas positivamente.")
    st.markdown("""
    **Casos de Uso:**
    - **Teoría de Colas:** El tiempo de espera hasta que 5 clientes ($\alpha=5$) han sido atendidos.
    - **Seguros:** Modelar el tamaño de las reclamaciones de un seguro.
    - **Climatología:** Modelar la cantidad de lluvia acumulada.
    - **Neurociencia:** Modelar el tiempo entre picos neuronales.
    """)

    st.header("Relación con Otras Distribuciones")
    st.write("""
    - **Exponencial:** La Gamma(α=1, β) es exactamente la Exponencial con escala $\beta$.
    - **Chi-Cuadrado:** La $\chi^2(k)$ es un caso especial de la Gamma($\alpha=k/2, \beta=2$).
    - **Normal:** Cuando $\alpha$ (forma) es grande, la Gamma se aproxima a una Normal.
    """)

    st.header("Fórmulas Matemáticas")
    st.subheader("Función de Densidad de Probabilidad (PDF)")
    st.latex(r"f(x) = \frac{x^{\alpha-1} e^{-x/\beta}}{\beta^\alpha \Gamma(\alpha)} \quad \text{para } x \ge 0")
    st.write(r"Donde $\Gamma(\alpha) = \int_{0}^{\infty} t^{\alpha-1} e^{-t} dt$ es la función Gamma (la generalización del factorial).")
    
    st.subheader("Media (Valor Esperado)")
    st.latex(r"\mu = E[X] = \alpha \beta")
    
    st.subheader("Varianza")
    st.latex(r"\sigma^2 = \text{Var}(X) = \alpha \beta^2")

with tab2:
    st.header("Visualización Interactiva")
    st.write("Ajusta $\alpha$ (forma) y $\beta$ (escala). Observa que si $\alpha=1$, es una Exponencial. Si $\alpha$ es grande, parece una Normal.")
    
    col1, col2 = st.columns(2)
    with col1:
        alpha_slider = st.slider("Forma (α)", min_value=0.1, max_value=20.0, value=2.0, step=0.1, key='gamma_alpha')
    with col2:
        beta_slider = st.slider("Escala (β)", min_value=0.1, max_value=5.0, value=1.0, step=0.1, key='gamma_beta')

    if alpha_slider <= 0 or beta_slider <= 0:
        st.error("Alfa (α) y Beta (β) deben ser positivos.")
    else:
        try:
            dist = stats.gamma(a=alpha_slider, scale=beta_slider)
            
            # Graficar hasta el percentil 99.8
            x_min = 0
            x_max = dist.ppf(0.998)
            
            fig = plot_continuous_distribution(dist, x_min, x_max, f"PDF Gamma (α={alpha_slider:.1f}, β={beta_slider:.1f})")
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.error(f"Error al generar el gráfico: {e}")

with tab3:
    st.header("Calculadora Interactiva (Conceptual)")
    st.write("Calcula la Media y Varianza. (Grupo 2)")
    
    st.subheader("Parámetros")
    col1, col2 = st.columns(2)
    with col1:
        calc_alpha = st.number_input("Forma (α)", min_value=0.01, value=2.0, step=0.1, key='gamma_calc_alpha')
    with col2:
        calc_beta = st.number_input("Escala (β)", min_value=0.01, value=1.0, step=0.1, key='gamma_calc_beta')

    if calc_alpha <= 0 or calc_beta <= 0:
        st.error("'α' y 'β' deben ser positivos.")
    else:
        try:
            dist = stats.gamma(a=calc_alpha, scale=calc_beta)
            
            st.subheader("Estadísticos:")
            st.markdown(f"**Media (μ = αβ):** `{dist.mean():.4f}`")
            st.markdown(f"**Varianza (σ² = αβ²):** `{dist.var():.4f}`")
            st.markdown(f"**Desviación Estándar (σ):** `{dist.std():.4f}`")
            
            st.subheader("Nota Pedagógica sobre Cálculo de Probabilidad")
            st.info("""
            **Esta distribución pertenece al GRUPO 2.**
            
            En la práctica, los valores de probabilidad (CDF) para la distribución Gamma no se calculan a mano. La CDF (Función de Distribución Acumulada) implica integrar la PDF, lo cual requiere métodos de aproximación numérica complejos (la "función gamma incompleta").
            
            Por esta razón, los valores se obtienen de tablas estándar o, más comúnmente, de **software estadístico** (como R, Python con SciPy, o Excel) que tienen estas funciones numéricas implementadas.
            """)
                
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

with tab4:
    st.header("Ejemplos Aplicados")
    st.markdown("""
    1.  **Tiempo de Espera:** Si los clientes llegan a $\lambda=2$ por minuto, el tiempo hasta que lleguen 5 clientes ($\alpha=5$) sigue una Gamma($\alpha=5, \beta=1/\lambda=0.5$).
    2.  **Seguros:** El total de reclamaciones anuales de un cliente puede modelarse con Gamma, donde $\alpha$ es el número de reclamaciones y $\beta$ el coste medio.
    3.  **Fiabilidad:** El tiempo hasta el 3er fallo ($\alpha=3$) de un componente cuyo tiempo entre fallos es Exponencial.
    """)

with tab5:
    st.header("Ejercicios Interactivos")
    
    st.subheader("Ejercicio 1: Media")
    st.write("El tiempo de espera para que lleguen $\alpha=3$ autobuses sigue una Gamma. El tiempo medio entre autobuses (Exponencial) es $\beta=10$ minutos. ¿Cuál es el tiempo medio *total* esperado?")
    ans1 = st.number_input("Tu respuesta (Media μ):", min_value=0.0, step=1.0, format="%.1f", key='gamma_ex1_ans')
    if st.button("Revisar 1", key='gamma_ex1_btn'):
        correct_ans = 3 * 10
        if np.isclose(ans1, correct_ans):
            st.success(f"¡Correcto! La media es {correct_ans:.1f} minutos.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.1f} minutos.")
        with st.expander("Ver Solución"):
            st.write(f"La media de una Gamma es $\mu = \alpha \beta$.")
            st.code(f"3 * 10 = 30.0")
    
    st.subheader("Ejercicio 2: Varianza")
    st.write("En el mismo escenario ($\alpha=3, \beta=10$), ¿cuál es la varianza $\sigma^2$ del tiempo de espera total?")
    ans2 = st.number_input("Tu respuesta (Varianza σ²):", min_value=0.0, step=1.0, format="%.1f", key='gamma_ex2_ans')
    if st.button("Revisar 2", key='gamma_ex2_btn'):
        correct_ans = 3 * (10**2)
        if np.isclose(ans2, correct_ans):
            st.success(f"¡Correcto! La varianza es {correct_ans:.1f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.1f}.")
        with st.expander("Ver Solución"):
            st.write(f"La varianza de una Gamma es $\sigma^2 = \alpha \beta^2$.")
            st.code(f"3 * (10 * 10) = 300.0")
            
    st.subheader("Ejercicio 3: Relaciones")
    st.write("¿Qué distribución obtienes si configuras una Gamma con $\alpha=1$ y $\beta=5$?")
    ans3 = st.text_input("Tu respuesta (Nombre de la distribución):", key='gamma_ex3_ans').strip().lower()
    if st.button("Revisar 3", key='gamma_ex3_btn'):
        if ans3 == "exponencial":
            st.success("¡Correcto! Es una Distribución Exponencial.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es 'Exponencial'.")
        with st.expander("Ver Solución"):
            st.write(f"La Distribución Exponencial es un caso especial de la Gamma con $\alpha=1$.")
            st.write("Gamma(1, $\beta$) = Exponencial(escala=$\beta$)")
