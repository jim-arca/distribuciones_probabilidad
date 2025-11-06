import streamlit as st
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Importamos la función de ayuda
try:
    from helpers import plot_discrete_distribution
except ImportError:
    st.error("No se pudo importar 'helpers.py'. Asegúrate de que esté en el directorio raíz.")
    st.stop()

# --- Contenido de la Página ---

st.title("Distribución Hipergeométrica")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teoría y Fórmulas", "Visualización", "Calculadora", "Ejemplos", "Ejercicios"
])

with tab1:
    st.header("Concepto Teórico")
    st.write("""
    La Distribución Hipergeométrica modela el número de éxitos $k$ en una muestra de tamaño $n$, extraída **SIN REEMPLAZO** de una población finita de tamaño $N$ que contiene $K$ éxitos.
    
    Es similar a la Binomial, pero la diferencia clave es la *dependencia* entre los ensayos (la probabilidad de éxito cambia con cada extracción).
    
    - **Parámetros:**
        - $N$: Tamaño total de la población (ej. 100 bolas en una urna).
        - $K$: Número total de "éxitos" en la población (ej. 30 bolas rojas).
        - $n$: Tamaño de la muestra extraída (ej. se sacan 10 bolas).
    - **Rango:** La variable $X$ (éxitos en la muestra) puede tomar valores $k$ desde $\max(0, n-(N-K))$ hasta $\min(n, K)$.
    """)

    st.header("Contexto Histórico y Casos de Uso")
    st.write("Es una de las distribuciones fundamentales en estadística inferencial y muestreo. Su nombre proviene de la serie hipergeométrica, que aparece en su función de probabilidad.")
    st.markdown("""
    **Casos de Uso:**
    - **Juegos de Azar:** Probabilidad de recibir 2 Ases ($K=4$) en una mano de 5 cartas ($n=5$) de una baraja ($N=52$).
    - **Control de Calidad:** Si un lote de 200 fusibles ($N=200$) tiene 10 defectuosos ($K=10$), ¿cuál es la prob. de encontrar 2 defectuosos ($k=2$) en una muestra de 20 ($n=20$)?
    - **Ecología:** Estimación de poblaciones (captura-recaptura). Si se capturan y marcan 50 peces ($K=50$) y se liberan, y luego se recapturan 30 ($n=30$), el número de peces marcados ($k$) en la recaptura sigue esta distribución.
    """)

    st.header("Relación con Otras Distribuciones")
    st.write("""
    - **Binomial:** Cuando el tamaño de la población $N$ es muy grande en comparación con el tamaño de la muestra $n$ (ej. $n/N < 0.05$), el muestreo *sin* reemplazo se parece mucho al muestreo *con* reemplazo. En este caso, la Hipergeométrica(N, K, n) se aproxima muy bien por una **Binomial(n, p)**, donde $p = K/N$.
    """)

    st.header("Fórmulas Matemáticas")
    st.subheader("Función de Masa de Probabilidad (PMF)")
    st.write(r"La prob. de obtener $k$ éxitos en una muestra de $n$:")
    st.latex(r"P(X=k) = \frac{\binom{K}{k} \binom{N-K}{n-k}}{\binom{N}{n}}")
    st.write(r"Donde $\binom{a}{b}$ es el coeficiente binomial 'a sobre b'.")
    
    st.subheader("Media (Valor Esperado)")
    st.latex(r"\mu = E[X] = n \left( \frac{K}{N} \right)")
    
    st.subheader("Varianza")
    st.latex(r"\sigma^2 = \text{Var}(X) = n \left( \frac{K}{N} \right) \left( 1 - \frac{K}{N} \right) \left( \frac{N-n}{N-1} \right)")
    st.write(r"El último término $\left( \frac{N-n}{N-1} \right)$ es el **factor de corrección por población finita**.")

with tab2:
    st.header("Visualización Interactiva")
    st.write("Ajusta los parámetros de la población ($N, K$) y la muestra ($n$).")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        N_slider = st.number_input("Población (N)", min_value=10, max_value=200, value=52, step=1, key='hyp_N')
    with col2:
        # K no puede ser mayor que N
        K_slider = st.slider("Éxitos en Pob. (K)", min_value=1, max_value=N_slider, value=4, step=1, key='hyp_K')
    with col3:
        # n no puede ser mayor que N
        n_slider = st.slider("Muestra (n)", min_value=1, max_value=N_slider, value=5, step=1, key='hyp_n')

    # Validación
    if K_slider > N_slider or n_slider > N_slider:
        st.error("K y n no pueden ser mayores que N.")
    else:
        try:
            # SciPy usa M=N (Pob), n=K (Éxitos), N=n (Muestra)
            dist = stats.hypergeom(M=N_slider, n=K_slider, N=n_slider)
            
            # Calcular rango válido de k
            k_min = max(0, n_slider - (N_slider - K_slider))
            k_max = min(n_slider, K_slider)
            k_values = np.arange(k_min, k_max + 1)
            
            fig = plot_discrete_distribution(dist, k_values, f"PMF Hipergeométrica (N={N_slider}, K={K_slider}, n={n_slider})")
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.error(f"Error al generar el gráfico: {e}")

with tab3:
    st.header("Calculadora Interactiva")
    st.write("Calcula $P(X=k)$ y $P(X \le k)$.")
    
    st.subheader("Parámetros")
    col1, col2, col3 = st.columns(3)
    with col1:
        calc_N = st.number_input("Población (N)", min_value=2, value=52, step=1, key='hyp_calc_N')
    with col2:
        calc_K = st.number_input("Éxitos en Pob. (K)", min_value=1, max_value=calc_N, value=4, step=1, key='hyp_calc_K')
    with col3:
        calc_n = st.number_input("Muestra (n)", min_value=1, max_value=calc_N, value=5, step=1, key='hyp_calc_n')
        
    st.subheader("Valor a Calcular")
    k_min_calc = max(0, calc_n - (calc_N - calc_K))
    k_max_calc = min(calc_n, calc_K)
    calc_k = st.number_input(f"Número de éxitos en muestra (k)", min_value=k_min_calc, max_value=k_max_calc, value=max(k_min_calc, min(2, k_max_calc)), step=1, key='hyp_calc_k')

    # Validación
    if calc_K > calc_N or calc_n > calc_N:
        st.error("K y n no pueden ser mayores que N.")
    else:
        try:
            # SciPy usa M=N (Pob), n=K (Éxitos), N=n (Muestra)
            dist = stats.hypergeom(M=calc_N, n=calc_K, N=calc_n)
            prob_k = dist.pmf(calc_k)
            prob_cdf = dist.cdf(calc_k)
            
            st.subheader("Resultados:")
            st.markdown(f"**$P(X = {calc_k})$:** `{prob_k:.6f}`")
            st.markdown(f"**$P(X \le {calc_k})$:** `{prob_cdf:.6f}`")
            
            st.subheader("Estadísticos:")
            st.markdown(f"**Media (μ):** `{dist.mean():.4f}`")
            st.markdown(f"**Varianza (σ²):** `{dist.var():.4f}`")
            
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

with tab4:
    st.header("Ejemplos Aplicados")
    st.markdown("""
    1.  **Lotería:** En un sorteo de 49 números ($N=49$) se eligen 6 ($n=6$). Si un jugador también elige 6 números ($K=6$), ¿cuál es la prob. de que acierte 4 ($k=4$)?
    2.  **Selección de Jurado:** De un grupo de 30 personas ($N=30$) (18 H y 12 M), se selecciona un jurado de 10 ($n=10$). ¿Cuál es la prob. de que el jurado tenga 5 Hombres y 5 Mujeres? (Se calcula $P(X=5)$ para $K=18$ (Hombres)).
    3.  **Auditoría:** Una empresa tiene 80 facturas ($N=80$) y 8 de ellas tienen errores ($K=8$). Un auditor toma una muestra de 10 facturas ($n=10$). ¿Cuál es la prob. de que no encuentre ningún error ($k=0$)?
    """)

with tab5:
    st.header("Ejercicios Interactivos")
    
    st.subheader("Ejercicio 1: Cartas")
    st.write("En una baraja de 52 cartas ($N=52$), hay 13 Corazones ($K=13$). Si se reparten 5 cartas ($n=5$), ¿cuál es la probabilidad de obtener *exactamente* 2 Corazones ($k=2$)?")
    ans1 = st.number_input("Tu respuesta (P(X=2)):", min_value=0.0, max_value=1.0, step=0.001, format="%.4f", key='hyp_ex1_ans')
    if st.button("Revisar 1", key='hyp_ex1_btn'):
        correct_ans = stats.hypergeom.pmf(k=2, M=52, n=13, N=5)
        if np.isclose(ans1, correct_ans):
            st.success(f"¡Correcto! La probabilidad es {correct_ans:.4f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.4f}.")
        with st.expander("Ver Solución"):
            st.write(r"$P(X=2) = \frac{\binom{13}{2} \binom{52-13}{5-2}}{\binom{52}{5}} = \frac{\binom{13}{2} \binom{39}{3}}{\binom{52}{5}}$")
            st.code(f"stats.hypergeom.pmf(k=2, M=52, n=13, N=5) = {correct_ans:.4f}")
    
    st.subheader("Ejercicio 2: Bolas")
    st.write("Una urna tiene 10 bolas rojas ($K=10$) y 5 bolas azules. En total $N=15$. Si sacas 4 bolas ($n=4$), ¿cuál es la probabilidad de que *todas* sean rojas ($k=4$)?")
    ans2 = st.number_input("Tu respuesta (P(X=4)):", min_value=0.0, max_value=1.0, step=0.001, format="%.4f", key='hyp_ex2_ans')
    if st.button("Revisar 2", key='hyp_ex2_btn'):
        correct_ans = stats.hypergeom.pmf(k=4, M=15, n=10, N=4)
        if np.isclose(ans2, correct_ans):
            st.success(f"¡Correcto! La probabilidad es {correct_ans:.4f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.4f}.")
        with st.expander("Ver Solución"):
            st.write(r"$P(X=4) = \frac{\binom{10}{4} \binom{15-10}{4-4}}{\binom{15}{4}} = \frac{\binom{10}{4} \binom{5}{0}}{\binom{15}{4}}$")
            st.code(f"stats.hypergeom.pmf(k=4, M=15, n=10, N=4) = {correct_ans:.4f}")

    st.subheader("Ejercicio 3: Media")
    st.write("En el escenario del Ejercicio 2 (N=15, K=10, n=4), ¿cuál es el número *esperado* (media) de bolas rojas en la muestra?")
    ans3 = st.number_input("Tu respuesta (Media μ):", min_value=0.0, step=0.1, format="%.2f", key='hyp_ex3_ans')
    if st.button("Revisar 3", key='hyp_ex3_btn'):
        correct_ans = stats.hypergeom.mean(M=15, n=10, N=4)
        if np.isclose(ans3, correct_ans):
            st.success(f"¡Correcto! La media es {correct_ans:.2f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.2f}.")
        with st.expander("Ver Solución"):
            st.write(r"La media es $\mu = n \left( \frac{K}{N} \right) = 4 \times (10 / 15)$")
            st.code(f"4 * (10 / 15) = 2.67")
