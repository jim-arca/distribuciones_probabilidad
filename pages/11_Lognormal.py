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

st.title("Distribución Lognormal")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teoría y Fórmulas", "Visualización", "Calculadora", "Ejemplos", "Ejercicios"
])

with tab1:
    st.header("Concepto Teórico")
    st.write("""
    Una variable aleatoria $X$ sigue una Distribución Lognormal si su logaritmo natural, $Y = \ln(X)$, sigue una Distribución Normal.
    
    Mientras la Normal modela procesos *aditivos* (la suma de muchos factores), la Lognormal modela procesos *multiplicativos* (el producto de muchos factores).
    
    Es una distribución continua, **solo definida para valores positivos** ($X > 0$) y tiene una **fuerte asimetría positiva** (cola larga a la derecha).
    
    - **Parámetros:** Se define por los parámetros de la distribución normal subyacente:
        - $\mu_{\log}$: La **media de $\ln(X)$**.
        - $\sigma_{\log}$: La **desviación estándar de $\ln(X)$** ($\sigma_{\log} > 0$).
    - **Rango:** La variable $X$ puede tomar cualquier valor real $x > 0$.
    """)
    st.info("Nota: SciPy usa $s = \sigma_{\log}$ y $scale = e^{\mu_{\log}}$.")


    st.header("Contexto Histórico y Casos de Uso")
    st.write("Usada extensamente en finanzas (modelo Black-Scholes) y en ciencias donde el crecimiento es proporcional al tamaño actual.")
    st.markdown("""
    **Casos de Uso:**
    - **Economía:** Distribución de la riqueza o ingresos en una población.
    - **Finanzas:** Precios de acciones (se asume que los *retornos logarítmicos* son normales).
    - **Biología:** El tamaño de organismos vivos, o el tiempo de incubación de enfermedades.
    - **Ingeniería:** Tiempos de fallo de sistemas mecánicos (fatiga de material).
    """)

    st.header("Relación con Otras Distribuciones")
    st.write("""
    - **Normal:** Es la base. $Y = \ln(X) \sim N(\mu_{\log}, \sigma_{\log})$.
    """)

    st.header("Fórmulas Matemáticas")
    st.subheader("Función de Densidad de Probabilidad (PDF)")
    st.latex(r"f(x) = \frac{1}{x \sigma_{\log} \sqrt{2\pi}} \exp \left( - \frac{(\ln(x) - \mu_{\log})^2}{2\sigma_{\log}^2} \right) \quad \text{para } x > 0")
    
    st.subheader("Media (Valor Esperado) de X")
    st.latex(r"\mu = E[X] = e^{\mu_{\log} + \sigma_{\log}^2 / 2}")
    
    st.subheader("Varianza de X")
    st.latex(r"\sigma^2 = \text{Var}(X) = \left( e^{\sigma_{\log}^2} - 1 \right) e^{2\mu_{\log} + \sigma_{\log}^2}")

with tab2:
    st.header("Visualización Interactiva")
    st.write("Ajusta $\mu_{\log}$ (afecta la escala) y $\sigma_{\log}$ (afecta la asimetría).")
    
    col1, col2 = st.columns(2)
    with col1:
        mu_log_slider = st.slider("Media Log (μ_log)", min_value=-2.0, max_value=3.0, value=0.0, step=0.1, key='lognorm_mu')
    with col2:
        sigma_log_slider = st.slider("Desv. Est. Log (σ_log)", min_value=0.1, max_value=2.0, value=1.0, step=0.1, key='lognorm_sigma')

    if sigma_log_slider <= 0:
        st.error("Sigma (σ_log) debe ser positiva.")
    else:
        try:
            # SciPy usa s=sigma_log, scale=exp(mu_log)
            dist = stats.lognorm(s=sigma_log_slider, scale=np.exp(mu_log_slider))
            
            # Graficar hasta el percentil 99.5
            x_min = 0
            x_max = dist.ppf(0.995)
            # Asegurar que x_max no sea demasiado grande o inf
            if x_max > 50 or np.isinf(x_max) or np.isnan(x_max):
                x_max = 50 
            
            fig = plot_continuous_distribution(dist, x_min, x_max, f"PDF Lognormal (μ_log={mu_log_slider:.1f}, σ_log={sigma_log_slider:.1f})")
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.error(f"Error al generar el gráfico: {e}")

with tab3:
    st.header("Calculadora Interactiva")
    st.write("Calcula probabilidades para $X$, dados los parámetros de $\ln(X)$.")
    
    st.subheader("Parámetros (de $\ln(X)$)")
    col1, col2 = st.columns(2)
    with col1:
        calc_mu_log = st.number_input("Media Log (μ_log)", value=0.0, step=0.1, key='lognorm_calc_mu')
    with col2:
        calc_sigma_log = st.number_input("Desv. Est. Log (σ_log)", min_value=0.01, value=1.0, step=0.01, key='lognorm_calc_sigma')

    if calc_sigma_log <= 0:
        st.error("'σ_log' debe ser positiva.")
    else:
        try:
            dist = stats.lognorm(s=calc_sigma_log, scale=np.exp(calc_mu_log))
            
            st.subheader("Cálculo de Probabilidad (para $X$)")
            
            st.write("**1. Probabilidad Acumulada $P(X \le x)$**")
            calc_x = st.number_input("Valor de X (debe ser > 0)", min_value=0.01, value=1.0, step=0.1, key='lognorm_calc_x')
            prob_cdf = dist.cdf(calc_x)
            prob_sf = dist.sf(calc_x)
            st.markdown(f"**$P(X \le {calc_x:.2f})$:** `{prob_cdf:.6f}`")
            st.markdown(f"**$P(X > {calc_x:.2f})$:** `{prob_sf:.6f}`")

            st.subheader("Estadísticos (de $X$, no de $\ln(X)$):")
            st.markdown(f"**Media (μ):** `{dist.mean():.4f}`")
            st.markdown(f"**Varianza (σ²):** `{dist.var():.4f}`")
                
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

with tab4:
    st.header("Ejemplos Aplicados")
    st.markdown("""
    1.  **Ingresos:** Los ingresos de un pueblo siguen una Lognormal, donde el $\ln(\text{Ingreso})$ sigue N($\mu=10.5, \sigma=0.5$). ¿Prob. de que alguien gane más de 50,000? (Calcular $P(X > 50000)$).
    2.  **Precios de Acciones:** El precio de una acción en 1 año ($P_1$) se modela como $P_1 = P_0 \cdot e^{R}$, donde $R \sim N(\mu, \sigma)$. Esto significa $P_1$ es Lognormal.
    3.  **Tiempos de Reparación:** El tiempo para reparar una máquina compleja a menudo es Lognormal (la mayoría de las reparaciones son rápidas, algunas toman mucho tiempo).
    """)

with tab5:
    st.header("Ejercicios Interactivos")
    
    st.subheader("Ejercicio 1")
    st.write("Si $Y = \ln(X)$ sigue una $N(\mu=0, \sigma=1)$ (Normal Estándar), ¿cuál es la probabilidad de que $X \le 1$?")
    ans1 = st.number_input("Tu respuesta (P(X≤1)):", min_value=0.0, max_value=1.0, step=0.01, format="%.2f", key='lognorm_ex1_ans')
    if st.button("Revisar 1", key='lognorm_ex1_btn'):
        correct_ans = 0.5
        if np.isclose(ans1, correct_ans):
            st.success(f"¡Correcto! La probabilidad es {correct_ans:.2f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.2f}.")
        with st.expander("Ver Solución"):
            st.write(f"$P(X \le 1)$ es lo mismo que $P(\ln(X) \le \ln(1)) = P(Y \le 0)$.")
            st.write("Dado que $Y \sim N(0, 1)$, estamos preguntando $P(Y \le 0)$, que es la prob. de estar por debajo de la media. Por simetría, es 0.5.")
    
    st.subheader("Ejercicio 2")
    st.write("Una variable $X$ es Lognormal con $\mu_{\log}=1$ y $\sigma_{\log}=0.5$. ¿Cuál es la media $E[X]$?")
    ans2 = st.number_input("Tu respuesta (Media E[X]):", min_value=0.0, step=0.01, format="%.3f", key='lognorm_ex2_ans')
    if st.button("Revisar 2", key='lognorm_ex2_btn'):
        correct_ans = np.exp(1 + (0.5**2 / 2))
        if np.isclose(ans2, correct_ans):
            st.success(f"¡Correcto! La media es {correct_ans:.3f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.3f}.")
        with st.expander("Ver Solución"):
            st.write(f"La media es $E[X] = e^{\mu_{\log} + \sigma_{\log}^2 / 2}$.")
            st.code(f"np.exp(1 + 0.5**2 / 2) = np.exp(1 + 0.125) = np.exp(1.125) = {correct_ans:.3f}")
            
    st.subheader("Ejercicio 3")
    st.write("Si $\ln(X) \sim N(3, 1)$, ¿cuál es la *mediana* de $X$?")
    ans3 = st.number_input("Tu respuesta (Mediana de X):", min_value=0.0, step=0.1, format="%.2f", key='lognorm_ex3_ans')
    if st.button("Revisar 3", key='lognorm_ex3_btn'):
        correct_ans = np.exp(3)
        if np.isclose(ans3, correct_ans):
            st.success(f"¡Correcto! La mediana es {correct_ans:.2f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.2f}.")
        with st.expander("Ver Solución"):
            st.write(f"La mediana de $X$ es $e^{{\mu_{\log}}}$. La mediana de $\ln(X)$ es $\mu_{\log}$.")
            st.write("Mediana($X$) = $e^{Mediana(\ln(X))}$ = $e^{\mu_{\log}}$")
            st.code(f"np.exp(3) = {correct_ans:.2f}")
