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

st.title("Distribución Chi-Cuadrado (χ²)")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teoría y Fórmulas", "Visualización", "Calculadora", "Ejemplos", "Ejercicios"
])

with tab1:
    st.header("Concepto Teórico")
    st.write("""
    La Distribución Chi-Cuadrado (o Ji-Cuadrada) es una distribución continua fundamental en la estadística inferencial.
    
    Se define como la **suma de $k$ variables aleatorias Normal Estándar independientes, elevadas al cuadrado**.
    
    $X = Z_1^2 + Z_2^2 + \dots + Z_k^2 \sim \chi^2(k)$
    
    Es una distribución **no simétrica** (sesgada a la derecha) y **solo toma valores positivos** ($x \ge 0$).
    
    - **Parámetro:**
        - $k$ (o $df$): **Grados de libertad** (el número de variables $Z^2$ que se están sumando).
    - **Rango:** La variable $\chi^2$ puede tomar cualquier valor $x \ge 0$.
    """)

    st.header("Contexto Histórico y Casos de Uso")
    st.write("Desarrollada por **Karl Pearson** en 1900. Es la base de una de las pruebas de hipótesis más utilizadas.")
    st.markdown("""
    **Casos de Uso:**
    - **Prueba $\chi^2$ de Bondad de Ajuste:** Comprobar si los datos de una muestra (ej. lanzamientos de dado) se ajustan a una distribución teórica esperada.
    - **Prueba $\chi^2$ de Independencia:** Comprobar si dos variables categóricas (ej. 'Fumador' y 'Enfermedad') están relacionadas o son independientes (usando tablas de contingencia).
    - **Inferencia sobre la Varianza:** Calcular intervalos de confianza o probar hipótesis sobre la varianza de una población normal.
    """)

    st.header("Relación con Otras Distribuciones")
    st.write("""
    - **Normal:** Se deriva de la Normal Estándar ($Z^2$).
    - **Gamma:** Es un caso especial de la Gamma: $\chi^2(k) \equiv \text{Gamma}(\alpha=k/2, \beta=2)$.
    - **Distribución F:** La F-distribution es la *proporción* de dos Chi-Cuadrado independientes.
    """)

    st.header("Fórmulas Matemáticas")
    st.subheader("Función de Densidad de Probabilidad (PDF)")
    st.write(r"Es la PDF de la Gamma($k/2, 2$):")
    st.latex(r"f(x) = \frac{1}{2^{k/2} \Gamma(k/2)} x^{k/2 - 1} e^{-x/2} \quad \text{para } x \ge 0")
    
    st.subheader("Media (Valor Esperado)")
    st.latex(r"\mu = E[X] = k")
    
    st.subheader("Varianza")
    st.latex(r"\sigma^2 = \text{Var}(X) = 2k")

with tab2:
    st.header("Visualización Interactiva")
    st.write("Ajusta los grados de libertad ($k$). Observa cómo la forma se vuelve más simétrica (parecida a la Normal) a medida que $k$ aumenta.")
    
    k_slider = st.slider("Grados de Libertad (k, df)", min_value=1, max_value=50, value=5, step=1, key='chi2_k')

    if k_slider <= 0:
        st.error("k (df) debe ser positivo.")
    else:
        try:
            dist = stats.chi2(df=k_slider)
            
            x_min = 0
            x_max = dist.ppf(0.998) # Graficar hasta el 99.8%
            
            fig = plot_continuous_distribution(dist, x_min, x_max, f"PDF Chi-Cuadrado (k={k_slider})")
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.error(f"Error al generar el gráfico: {e}")

with tab3:
    st.header("Calculadora Interactiva (Conceptual)")
    st.write("Calcula la Media y Varianza. (Grupo 2)")
    
    st.subheader("Parámetros")
    calc_k = st.number_input("Grados de Libertad (k, df)", min_value=1, value=5, step=1, key='chi2_calc_k')

    st.subheader("Estadísticos:")
    if calc_k <= 0:
        st.error("k debe ser > 0")
    else:
        dist = stats.chi2(df=calc_k)
        st.markdown(f"**Media (μ = k):** `{dist.mean():.4f}`")
        st.markdown(f"**Varianza (σ² = 2k):** `{dist.var():.4f}`")
    
    st.subheader("Nota Pedagógica sobre Cálculo de Probabilidad")
    st.info("""
    **Esta distribución pertenece al GRUPO 2.**
    
    Al igual que la 't' y la 'Gamma', el cálculo de probabilidades (el área bajo la curva) para $\chi^2$ no es trivial y requiere integración numérica (es una función Gamma incompleta).
    
    Históricamente, los "valores críticos" (ej. el valor $x$ que deja 5% de área a la derecha) se buscaban en **tablas de Chi-Cuadrado**. Hoy, se obtienen de **software estadístico**.
    """)

with tab4:
    st.header("Ejemplos Aplicados")
    st.markdown("""
    1.  **Bondad de Ajuste (Dado):** Lanzas un dado 600 veces. Esperas 100 de cada cara. Calculas $\sum \frac{{(O_i - E_i)^2}}{{E_i}}$ (Observado - Esperado). Este estadístico sigue una $\chi^2(df=5)$.
    2.  **Independencia (Tabla):** Encuestas a 500 personas sobre "Preferencia Política" (3 categorías) y "Nivel Educativo" (4 categorías). Para ver si son independientes, creas una tabla $3 \times 4$. El estadístico sigue una $\chi^2(df=(3-1)(4-1)=6)$.
    3.  **Varianza:** Quieres probar si la varianza $\sigma^2$ de una máquina es mayor a 0.5. El estadístico $(n-1)s^2 / \sigma^2$ sigue una $\chi^2(df=n-1)$.
    """)

with tab5:
    st.header("Ejercicios Interactivos")
    
    st.subheader("Ejercicio 1: Media y Varianza")
    st.write("Para una prueba de Chi-Cuadrado con $k=10$ grados de libertad, ¿cuál es la media y la varianza esperadas?")
    col1, col2 = st.columns(2)
    with col1:
        ans_m = st.number_input("Tu respuesta (Media μ):", min_value=0, step=1, key='chi2_ex1_m')
    with col2:
        ans_v = st.number_input("Tu respuesta (Varianza σ²):", min_value=0, step=1, key='chi2_ex1_v')
    
    if st.button("Revisar 1", key='chi2_ex1_btn'):
        if ans_m == 10 and ans_v == 20:
            st.success("¡Correcto!")
        else:
            st.error(f"Incorrecto. La media es 10 y la varianza es 20.")
        with st.expander("Ver Solución"):
            st.write(f"La media es $\mu = k = 10$.")
            st.write(f"La varianza es $\sigma^2 = 2k = 2 \times 10 = 20$.")
    
    st.subheader("Ejercicio 2: Grados de Libertad")
    st.write("Estás probando la independencia entre 'Género' (2 categorías) y 'Preferencia Musical' (4 categorías). ¿Cuántos grados de libertad tiene la distribución $\chi^2$?")
    ans2 = st.number_input("Tu respuesta (df):", min_value=1, step=1, key='chi2_ex2_ans')
    if st.button("Revisar 2", key='chi2_ex2_btn'):
        correct_ans = (2 - 1) * (4 - 1)
        if ans2 == correct_ans:
            st.success(f"¡Correcto! Los df son 3.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans}.")
        with st.expander("Ver Solución"):
            st.write(f"Para una tabla de contingencia, $df = (\text{filas} - 1) \times (\text{columnas} - 1)$.")
            st.code(f"(2 - 1) * (4 - 1) = 1 * 3 = 3")
            
    st.subheader("Ejercicio 3: Relaciones")
    st.write("Si sumas los cuadrados de 8 variables Normal Estándar independientes, ¿qué distribución sigues?")
    ans3 = st.text_input("Tu respuesta (Nombre y parámetro):", key='chi2_ex3_ans').strip().lower()
    if st.button("Revisar 3", key='chi2_ex3_btn'):
        if "chi-cuadrado" in ans3 and "8" in ans3:
            st.success("¡Correcto! Chi-Cuadrado con 8 grados de libertad (χ²(8)).")
        else:
            st.error(f"Incorrecto. Respuesta: Chi-Cuadrado(8).")
        with st.expander("Ver Solución"):
            st.write(f"Por definición, la suma de $k$ variables $Z^2$ sigue una $\chi^2(k)$. En este caso, $k=8$.")
