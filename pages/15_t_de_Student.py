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

st.title("Distribución t de Student")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teoría y Fórmulas", "Visualización", "Calculadora", "Ejemplos", "Ejercicios"
])

with tab1:
    st.header("Concepto Teórico")
    st.write("""
    La Distribución t de Student es una distribución continua clave en la **estadística inferencial**. Es similar a la Distribución Normal Estándar (N(0,1)), pero con **"colas más pesadas"** (más probabilidad en los extremos).
    
    Se utiliza fundamentalmente cuando:
    1.  El tamaño de la muestra ($n$) es pequeño.
    2.  La desviación estándar de la población ($\sigma$) es **desconocida** y debe estimarse a partir de la muestra.
    
    A medida que los grados de libertad aumentan (la muestra crece), la distribución t converge a la Normal.
    
    - **Parámetro:**
        - $\nu$ (nu) o $df$: **Grados de libertad**. Generalmente $df = n - 1$.
    - **Rango:** La variable $t$ puede tomar cualquier valor real $t \in (-\infty, \infty)$.
    """)

    st.header("Contexto Histórico y Casos de Uso")
    st.write("""
    Desarrollada por **William Sealy Gosset** en 1908, un químico que trabajaba para la cervecería Guinness en Dublín. 
    Publicó bajo el seudónimo "Student" porque Guinness prohibía a sus empleados publicar (para proteger secretos industriales).
    Gosset la necesitaba para analizar la calidad de la cerveza en muestras pequeñas.
    """)
    st.markdown("""
    **Casos de Uso:**
    - **Prueba t (t-test):** Comparar las medias de uno o dos grupos.
    - **Intervalos de Confianza:** Calcular intervalos de confianza para una media poblacional cuando $\sigma$ es desconocida.
    - **Coeficientes de Regresión:** Evaluar la significancia de los coeficientes en un modelo de regresión lineal.
    """)

    st.header("Relación con Otras Distribuciones")
    st.write("""
    - **Normal:** La $t(df)$ converge a la Normal(0, 1) a medida que $df \to \infty$. (En la práctica, con $df > 30$ ya son muy similares).
    - **Cauchy:** La $t(df=1)$ es idéntica a la Distribución de Cauchy.
    """)

    st.header("Fórmulas Matemáticas")
    st.subheader("Función de Densidad de Probabilidad (PDF)")
    st.latex(r"f(t) = \frac{\Gamma((\nu+1)/2)}{\sqrt{\nu\pi} \Gamma(\nu/2)} \left( 1 + \frac{t^2}{\nu} \right)^{-(\nu+1)/2}")
    
    st.subheader("Media (Valor Esperado)")
    st.latex(r"\mu = E[X] = 0 \quad (\text{para } \nu > 1)")
    
    st.subheader("Varianza")
    st.latex(r"\sigma^2 = \text{Var}(X) = \frac{\nu}{\nu - 2} \quad (\text{para } \nu > 2)")
    st.write("Nota: La varianza solo está definida para $df > 2$, y es *siempre mayor* que 1 (la varianza de la Normal Estándar).")

with tab2:
    st.header("Visualización Interactiva")
    st.write("Ajusta los grados de libertad ($df$) y compara con la Normal Estándar (línea punteada).")
    
    df_slider = st.slider("Grados de Libertad (df)", min_value=1, max_value=30, value=5, step=1, key='t_df')

    if df_slider <= 0:
        st.error("df debe ser positivo.")
    else:
        try:
            dist = stats.t(df=df_slider)
            
            # Rango de visualización
            x_min = -4
            x_max = 4
            
            fig = plot_continuous_distribution(dist, x_min, x_max, f"PDF t de Student (df={df_slider})")
            
            # Superponer la Normal Estándar para comparar
            ax = fig.gca()
            norm_dist = stats.norm(0, 1)
            x_values = np.linspace(x_min, x_max, 500)
            ax.plot(x_values, norm_dist.pdf(x_values), color='red', linestyle=':', linewidth=2, label='Normal(0,1)')
            ax.legend()
            
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.error(f"Error al generar el gráfico: {e}")

with tab3:
    st.header("Calculadora Interactiva (Conceptual)")
    st.write("Calcula la Media y Varianza. (Grupo 2)")
    
    st.subheader("Parámetros")
    calc_df = st.number_input("Grados de Libertad (df, $\nu$)", min_value=1, value=5, step=1, key='t_calc_df')

    st.subheader("Estadísticos:")
    if calc_df <= 1:
        st.markdown(f"**Media (μ):** `Indefinida` (Requiere $\nu > 1$)")
    else:
        st.markdown(f"**Media (μ):** `{stats.t.mean(df=calc_df):.4f}`")

    if calc_df <= 2:
        st.markdown(f"**Varianza (σ²):** `Indefinida` (Requiere $\nu > 2$)")
    else:
        st.markdown(f"**Varianza (σ²):** `{stats.t.var(df=calc_df):.4f}`")
    
    st.subheader("Nota Pedagógica sobre Cálculo de Probabilidad")
    st.info("""
    **Esta distribución pertenece al GRUPO 2.**
    
    En la práctica, los valores de probabilidad (CDF) y los valores críticos (PPF) para la distribución t no se calculan a mano. Históricamente, se buscaban en **tablas de t** impresas en los apéndices de los libros de texto de estadística.
    
    Hoy en día, se obtienen directamente de **software estadístico** (como R, Python con SciPy, o Excel), que usan funciones numéricas para calcular el área bajo esta compleja curva.
    """)

with tab4:
    st.header("Ejemplos Aplicados")
    st.markdown("""
    1.  **Muestra Pequeña:** Mides la altura de 10 estudiantes ($n=10$) para estimar la media. Usas una prueba t con $df = n-1 = 9$ para encontrar un intervalo de confianza.
    2.  **Comparación de Grupos:** Quieres saber si un nuevo fármaco (Grupo A, 15 pacientes) es mejor que un placebo (Grupo B, 15 pacientes). Usas una prueba t de dos muestras para comparar sus medias.
    3.  **Significancia de Regresión:** En un modelo `y = b_0 + b_1*x`, se usa una prueba t para determinar si el coeficiente $b_1$ es significativamente diferente de cero.
    """)

with tab5:
    st.header("Ejercicios Interactivos")
    
    st.subheader("Ejercicio 1: Grados de Libertad")
    st.write("Tomas una muestra de 25 personas ($n=25$) para calcular un intervalo de confianza para la media. ¿Cuántos grados de libertad ($df$) usarías?")
    ans1 = st.number_input("Tu respuesta (df):", min_value=1, step=1, key='t_ex1_ans')
    if st.button("Revisar 1", key='t_ex1_btn'):
        correct_ans = 24
        if ans1 == correct_ans:
            st.success(f"¡Correcto! Los df son $n-1 = 25 - 1 = 24$.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans}.")
        
    st.subheader("Ejercicio 2: Varianza")
    st.write("¿Cuál es la varianza de una distribución t con $df=5$?")
    ans2 = st.number_input("Tu respuesta (Varianza σ²):", min_value=0.0, step=0.01, format="%.2f", key='t_ex2_ans')
    if st.button("Revisar 2", key='t_ex2_btn'):
        correct_ans = 5 / (5 - 2)
        if np.isclose(ans2, correct_ans):
            st.success(f"¡Correcto! La varianza es {correct_ans:.2f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.2f}.")
        with st.expander("Ver Solución"):
            st.write(f"La varianza es $\sigma^2 = \nu / (\nu - 2)$.")
            st.code(f"5 / (5 - 2) = 5 / 3 = 1.67")
            
    st.subheader("Ejercicio 3: Convergencia")
    st.write("¿A qué distribución se parece más una $t(df=100)$?")
    ans3 = st.text_input("Tu respuesta (Nombre de la distribución):", key='t_ex3_ans').strip().lower()
    if st.button("Revisar 3", key='t_ex3_btn'):
        if "normal" in ans3:
            st.success("¡Correcto! A la Distribución Normal Estándar.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es 'Normal' o 'Normal Estándar'.")
        with st.expander("Ver Solución"):
            st.write(f"A medida que $df \to \infty$, la distribución t converge a la N(0, 1). Con $df=100$, las colas ya son muy ligeras y es casi idéntica a la Normal.")
