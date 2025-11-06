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

st.title("Distribución Normal (Gaussiana)")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teoría y Fórmulas", "Visualización", "Calculadora", "Ejemplos", "Ejercicios"
])

with tab1:
    st.header("Concepto Teórico")
    st.write("""
    La Distribución Normal, o "Campana de Gauss", es posiblemente la distribución más importante en estadística.
    
    Es una distribución continua que describe datos que se agrupan simétricamente alrededor de una media. Su importancia proviene del **Teorema del Límite Central**, que establece que la suma (o promedio) de muchas variables aleatorias independientes tiende a seguir una distribución normal, sin importar la distribución original de dichas variables.
    
    - **Parámetros:**
        - $\mu$ (mu): La **Media**, el centro de la campana.
        - $\sigma$ (sigma): La **Desviación Estándar**, que define cuán ancha o estrecha es la campana. $\sigma > 0$.
    - **Rango:** La variable $X$ puede tomar cualquier valor real $x \in (-\infty, \infty)$.
    """)
    
    st.subheader("La Regla Empírica (68-95-99.7)")
    st.markdown("""
    Para cualquier distribución normal:
    - **68%** de los datos cae dentro de $\pm 1$ desviación estándar de la media ($[\mu-\sigma, \mu+\sigma]$).
    - **95%** de los datos cae dentro de $\pm 2$ desviaciones estándar ($[\mu-2\sigma, \mu+2\sigma]$).
    - **99.7%** de los datos cae dentro de $\pm 3$ desviaciones estándar ($[\mu-3\sigma, \mu+3\sigma]$).
    """)

    st.header("Contexto Histórico y Casos de Uso")
    st.write("Desarrollada por **Carl Friedrich Gauss** (aunque Abraham de Moivre la usó antes), la usó para modelar errores de observación en astronomía.")
    st.markdown("""
    **Casos de Uso:**
    - **Fenómenos Naturales:** Altura, peso, presión arterial de una población.
    - **Mediciones:** Errores de medición en experimentos científicos.
    - **Finanzas:** Movimientos diarios de precios de acciones (aunque con limitaciones).
    - **Procesos Industriales:** Variaciones en el tamaño de piezas fabricadas.
    - **Estadística Inferencial:** Base para pruebas t, ANOVA, y regresión.
    """)

    st.header("Relación con Otras Distribuciones")
    st.write("""
    - **Estándar Normal (Z):** Un caso especial N(0, 1). Cualquier Normal N($\mu, \sigma$) se puede estandarizar.
    - **Lognormal:** Si $X \sim N(\mu, \sigma)$, entonces $e^X \sim \text{Lognormal}$.
    - **Aproximación:** La Normal aproxima a la Binomial y la Poisson cuando sus parámetros son grandes.
    - **t de Student / Chi-Cuadrado / F:** Estas distribuciones se derivan de la Normal y se usan para inferencia.
    """)

    st.header("Fórmulas Matemáticas")
    st.subheader("Función de Densidad de Probabilidad (PDF)")
    st.latex(r"f(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{ - \frac{1}{2} \left( \frac{x-\mu}{\sigma} \right)^2 }")
    
    st.subheader("Media (Valor Esperado)")
    st.latex(r"E[X] = \mu")
    
    st.subheader("Varianza")
    st.latex(r"\text{Var}(X) = \sigma^2")

with tab2:
    st.header("Visualización Interactiva")
    st.write("Ajusta la media ($\mu$) para mover la campana y la desviación ($\sigma$) para cambiar su ancho.")
    
    col1, col2 = st.columns(2)
    with col1:
        mu_slider = st.slider("Media (μ)", min_value=-10.0, max_value=10.0, value=0.0, step=0.5, key='norm_mu')
    with col2:
        sigma_slider = st.slider("Desviación Estándar (σ)", min_value=0.1, max_value=5.0, value=1.0, step=0.1, key='norm_sigma')

    if sigma_slider <= 0:
        st.error("Sigma (σ) debe ser positiva.")
    else:
        try:
            dist = stats.norm(loc=mu_slider, scale=sigma_slider)
            
            # Graficar +/- 4 desviaciones estándar
            x_min = mu_slider - 4 * sigma_slider
            x_max = mu_slider + 4 * sigma_slider
            
            fig = plot_continuous_distribution(dist, x_min, x_max, f"PDF Normal (μ={mu_slider:.1f}, σ={sigma_slider:.1f})")
            
            # Añadir líneas de la regla empírica
            ax = fig.gca()
            ax.axvline(mu_slider + sigma_slider, color='gray', linestyle='--', linewidth=1, label='μ ± 1σ (68%)')
            ax.axvline(mu_slider - sigma_slider, color='gray', linestyle='--', linewidth=1)
            ax.axvline(mu_slider + 2*sigma_slider, color='dimgray', linestyle=':', linewidth=1, label='μ ± 2σ (95%)')
            ax.axvline(mu_slider - 2*sigma_slider, color='dimgray', linestyle=':', linewidth=1)
            ax.legend()
            
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.error(f"Error al generar el gráfico: {e}")

with tab3:
    st.header("Calculadora Interactiva")
    st.write("Calcula probabilidades para cualquier N($\mu, \sigma$).")
    
    st.subheader("Parámetros")
    col1, col2 = st.columns(2)
    with col1:
        calc_mu = st.number_input("Media (μ)", value=0.0, step=0.1, key='norm_calc_mu')
    with col2:
        calc_sigma = st.number_input("Desviación Estándar (σ)", min_value=0.01, value=1.0, step=0.01, key='norm_calc_sigma')

    if calc_sigma <= 0:
        st.error("'σ' debe ser positiva.")
    else:
        try:
            dist = stats.norm(loc=calc_mu, scale=calc_sigma)
            
            st.subheader("Cálculo de Probabilidad")
            
            st.write("**1. Probabilidad de Rango $P(x_1 \le X \le x_2)$**")
            col_a, col_b = st.columns(2)
            with col_a:
                calc_x1 = st.number_input("Límite inferior (x₁)", value=calc_mu - calc_sigma, step=0.1, key='norm_calc_x1')
            with col_b:
                calc_x2 = st.number_input("Límite superior (x₂)", value=calc_mu + calc_sigma, step=0.1, key='norm_calc_x2')
            
            if calc_x1 >= calc_x2:
                st.warning("El límite inferior 'x₁' debe ser menor que 'x₂'.")
            else:
                prob_range = dist.cdf(calc_x2) - dist.cdf(calc_x1)
                st.markdown(f"**$P({calc_x1:.2f} \le X \le {calc_x2:.2f})$:** `{prob_range:.6f}`")

            st.write("**2. Probabilidad Acumulada $P(X \le x)$**")
            calc_x = st.number_input("Valor de x", value=calc_mu, step=0.1, key='norm_calc_x')
            prob_cdf = dist.cdf(calc_x)
            prob_sf = dist.sf(calc_x)
            st.markdown(f"**$P(X \le {calc_x:.2f})$:** `{prob_cdf:.6f}` (Área a la izquierda de x)")
            st.markdown(f"**$P(X > {calc_x:.2f})$:** `{prob_sf:.6f}` (Área a la derecha de x)")
                
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

with tab4:
    st.header("Ejemplos Aplicados")
    st.markdown("""
    1.  **Puntuaciones de IQ:** Las puntuaciones de IQ siguen N(100, 15). ¿Prob. de que una persona tenga un IQ > 130? (Esto es +2$\sigma$).
    2.  **Alturas:** La altura de hombres sigue N(175cm, 7cm). ¿Prob. de que alguien mida entre 170cm y 180cm?
    3.  **Fabricación:** El diámetro de un tornillo sigue N(10mm, 0.1mm). Las especificaciones son 9.8mm a 10.2mm. ¿Qué porcentaje de tornillos cumple? (Calcular $P(9.8 \le X \le 10.2)$).
    """)

with tab5:
    st.header("Ejercicios Interactivos")
    
    st.subheader("Ejercicio 1: Estandarización")
    st.write("Para N(μ=50, σ=10), ¿cuál es el 'Z-score' (valor estándar) para un puntaje $X=65$?")
    ans1 = st.number_input("Tu respuesta (Z-score):", min_value=-5.0, max_value=5.0, step=0.1, format="%.1f", key='norm_ex1_ans')
    if st.button("Revisar 1", key='norm_ex1_btn'):
        correct_ans = (65 - 50) / 10
        if np.isclose(ans1, correct_ans):
            st.success(f"¡Correcto! El Z-score es {correct_ans:.1f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.1f}.")
        with st.expander("Ver Solución"):
            st.write(f"El Z-score se calcula como $Z = (X - \mu) / \sigma$.")
            st.code(f"Z = (65 - 50) / 10 = 15 / 10 = 1.5")
    
    st.subheader("Ejercicio 2: Regla Empírica")
    st.write("Usando N(50, 10), ¿qué porcentaje aproximado de datos cae entre 40 y 60?")
    ans2 = st.number_input("Tu respuesta (%):", min_value=0, max_value=100, step=1, key='norm_ex2_ans')
    if st.button("Revisar 2", key='norm_ex2_btn'):
        if ans2 == 68:
            st.success("¡Correcto! Cae el 68%.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es 68%.")
        with st.expander("Ver Solución"):
            st.write(f"40 es $\mu - 1\sigma$ (50 - 10) y 60 es $\mu + 1\sigma$ (50 + 10).")
            st.write("Según la regla empírica, aproximadamente 68% de los datos cae dentro de $\pm 1$ desviación estándar.")
            
    st.subheader("Ejercicio 3: Cálculo")
    st.write("Usando N(50, 10), ¿cuál es la probabilidad exacta de $P(X \le 50)$?")
    ans3 = st.number_input("Tu respuesta (Probabilidad):", min_value=0.0, max_value=1.0, step=0.01, format="%.2f", key='norm_ex3_ans')
    if st.button("Revisar 3", key='norm_ex3_btn'):
        correct_ans = 0.5
        if np.isclose(ans3, correct_ans):
            st.success(f"¡Correcto! La probabilidad es {correct_ans:.2f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.2f}.")
        with st.expander("Ver Solución"):
            st.write(f"La distribución normal es simétrica. La media ($\mu=50$) divide la distribución exactamente a la mitad.")
            st.write("Por lo tanto, 50% del área está a la izquierda y 50% a la derecha.")
            st.code(f"stats.norm(loc=50, scale=10).cdf(50) = 0.5")
