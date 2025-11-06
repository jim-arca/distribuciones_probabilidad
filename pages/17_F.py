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

st.title("Distribución F (de Fisher-Snedecor)")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teoría y Fórmulas", "Visualización", "Calculadora", "Ejemplos", "Ejercicios"
])

with tab1:
    st.header("Concepto Teórico")
    st.write("""
    La Distribución F es una distribución continua fundamental, usada principalmente para **comparar las varianzas** de dos o más grupos.
    
    Se define como la **proporción de dos distribuciones Chi-Cuadrado ($\chi^2$) independientes**, cada una dividida por sus respectivos grados de libertad.
    
    $F = \frac{ ( \chi^2_1 / df_1 ) }{ ( \chi^2_2 / df_2 ) } \sim F(df_1, df_2)$
    
    Es la base del **Análisis de Varianza (ANOVA)**. Es no simétrica (sesgada a la derecha) y solo toma valores positivos ($x \ge 0$).
    
    - **Parámetros:**
        - $df_1$ (o $d_1$): **Grados de libertad del numerador**.
        - $df_2$ (o $d_2$): **Grados de libertad del denominador**.
    - **Rango:** La variable $F$ puede tomar cualquier valor $x \ge 0$.
    """)

    st.header("Contexto Histórico y Casos de Uso")
    st.write("Nombrada en honor a **Sir Ronald Fisher** (desarrolló ANOVA) y **George Snedecor** (la tabuló).")
    st.markdown("""
    **Casos de Uso:**
    - **ANOVA (Análisis de Varianza):** Es el uso principal. Compara si las medias de 3 o más grupos son iguales, analizando la "Varianza entre grupos" ($df_1$) vs. la "Varianza dentro de los grupos" ($df_2$).
    - **Prueba F de Regresión:** En regresión lineal, prueba si el modelo completo (todos los predictores) es significativo (F-test de significancia global).
    - **Prueba F para Igualdad de Varianzas:** Comparar si dos poblaciones normales tienen la misma varianza.
    """)

    st.header("Relación con Otras Distribuciones")
    st.write("""
    - **Chi-Cuadrado:** Se deriva directamente de la Chi-Cuadrado.
    - **t de Student:** El cuadrado de una variable $t(df)$ sigue una $F(1, df)$. ($t^2 \sim F$).
    """)

    st.header("Fórmulas Matemáticas")
    st.subheader("Función de Densidad de Probabilidad (PDF)")
    st.write(r"La PDF es muy compleja, involucrando la función Beta ($B$):")
    st.latex(r"f(x) = \frac{\sqrt{\frac{(d_1 x)^{d_1} d_2^{d_2}}{(d_1 x + d_2)^{d_1+d_2}}}}{x B(d_1/2, d_2/2)}")
    
    st.subheader("Media (Valor Esperado)")
    st.latex(r"\mu = E[X] = \frac{d_2}{d_2 - 2} \quad (\text{para } d_2 > 2)")
    st.write("Interesante: la media solo depende de los grados de libertad del denominador.")
    
    st.subheader("Varianza")
    st.latex(r"\sigma^2 = \text{Var}(X) = \frac{2 d_2^2 (d_1 + d_2 - 2)}{d_1 (d_2 - 2)^2 (d_2 - 4)} \quad (\text{para } d_2 > 4)")

with tab2:
    st.header("Visualización Interactiva")
    st.write("Ajusta los grados de libertad del numerador ($df_1$) y denominador ($df_2$).")
    
    col1, col2 = st.columns(2)
    with col1:
        df1_slider = st.slider("Grados de Libertad Numerador (df1)", min_value=1, max_value=50, value=5, step=1, key='f_df1')
    with col2:
        df2_slider = st.slider("Grados de Libertad Denominador (df2)", min_value=1, max_value=50, value=20, step=1, key='f_df2')

    if df1_slider <= 0 or df2_slider <= 0:
        st.error("df1 y df2 deben ser positivos.")
    else:
        try:
            dist = stats.f(dfn=df1_slider, dfd=df2_slider)
            
            x_min = 0
            x_max = dist.ppf(0.995) # Graficar hasta el 99.5%
            # Evitar valores extremos si df2 es pequeño
            if x_max > 15: x_max = 15
            
            fig = plot_continuous_distribution(dist, x_min, x_max, f"PDF Distribución F (df1={df1_slider}, df2={df2_slider})")
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
        calc_df1 = st.number_input("Grados de Libertad Numerador (df1)", min_value=1, value=5, step=1, key='f_calc_df1')
    with col2:
        calc_df2 = st.number_input("Grados de Libertad Denominador (df2)", min_value=1, value=20, step=1, key='f_calc_df2')

    st.subheader("Estadísticos:")
    if calc_df2 <= 2:
        st.markdown(f"**Media (μ):** `Indefinida` (Requiere $df_2 > 2$)")
    else:
        st.markdown(f"**Media (μ):** `{stats.f.mean(dfn=calc_df1, dfd=calc_df2):.4f}`")

    if calc_df2 <= 4:
        st.markdown(f"**Varianza (σ²):** `Indefinida` (Requiere $df_2 > 4$)")
    else:
        st.markdown(f"**Varianza (σ²):** `{stats.f.var(dfn=calc_df1, dfd=calc_df2):.4f}`")
    
    st.subheader("Nota Pedagógica sobre Cálculo de Probabilidad")
    st.info("""
    **Esta distribución pertenece al GRUPO 2.**
    
    La distribución F es una de las más complejas de calcular. Los valores-p y valores críticos (el valor $F$ que necesitas para superar el umbral del 5%) siempre se han buscado en extensas **tablas F**, que dependían de $df_1$, $df_2$ y el nivel de significancia (ej. $\alpha=0.05$).
    
    Hoy, **software estadístico** realiza estos cálculos numéricamente.
    """)

with tab4:
    st.header("Ejemplos Aplicados")
    st.markdown("""
    1.  **ANOVA:** Un agrónomo prueba 3 fertilizantes (A, B, C) en 10 parcelas cada uno ($n=30$ total). Para ver si las medias de cosecha son diferentes, calcula $F = \frac{\text{Var(Entre Grupos)}}{\text{Var(Dentro Grupos)}}$. Esto sigue $F(df_1=2, df_2=27)$.
    2.  **Regresión:** Un modelo `y = b_0 + b_1*x_1 + b_2*x_2` (2 predictores, 50 muestras). La prueba F global para el modelo sigue $F(df_1=2, df_2=50-2-1=47)$.
    3.  **Igualdad de Varianzas:** Pruebas si la varianza de la máquina A (muestra $n_1=15$) es igual a la de la B ($n_2=20$). El estadístico $F = s_1^2 / s_2^2$ sigue $F(df_1=14, df_2=19)$.
    """)

with tab5:
    st.header("Ejercicios Interactivos")
    
    st.subheader("Ejercicio 1: Media")
    st.write("En un ANOVA, tu estadístico sigue una $F(df_1=5, df_2=10)$. ¿Cuál es la media (valor esperado) de esta distribución?")
    ans1 = st.number_input("Tu respuesta (Media μ):", min_value=0.0, step=0.01, format="%.2f", key='f_ex1_ans')
    if st.button("Revisar 1", key='f_ex1_btn'):
        correct_ans = 10 / (10 - 2)
        if np.isclose(ans1, correct_ans):
            st.success(f"¡Correcto! La media es {correct_ans:.2f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.2f}.")
        with st.expander("Ver Solución"):
            st.write(f"La media es $\mu = d_2 / (d_2 - 2)$ (requiere $d_2 > 2$).")
            st.code(f"10 / (10 - 2) = 10 / 8 = 1.25")
    
    st.subheader("Ejercicio 2: Grados de Libertad (ANOVA)")
    st.write("Realizas un ANOVA para comparar 4 grupos ($k=4$). Tienes 8 muestras por grupo ($N=32$ total). ¿Cuáles son $df_1$ y $df_2$?")
    col1, col2 = st.columns(2)
    with col1:
        ans_df1 = st.number_input("Tu respuesta (df1):", min_value=1, step=1, key='f_ex2_df1')
    with col2:
        ans_df2 = st.number_input("Tu respuesta (df2):", min_value=1, step=1, key='f_ex2_df2')
    
    if st.button("Revisar 2", key='f_ex2_btn'):
        if ans_df1 == 3 and ans_df2 == 28:
            st.success("¡Correcto! $df_1 = 3$ y $df_2 = 28$.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es df1=3 y df2=28.")
        with st.expander("Ver Solución"):
            st.write(f"Numerador (Entre grupos): $df_1 = k - 1 = 4 - 1 = 3$.")
            st.write(f"Denominador (Dentro grupos): $df_2 = N - k = 32 - 4 = 28$.")
            
    st.subheader("Ejercicio 3: Relaciones")
    st.write("Si $T$ sigue una $t(df=25)$, ¿qué distribución sigue $T^2$?")
    ans3 = st.text_input("Tu respuesta (Nombre y parámetros):", key='f_ex3_ans').strip().lower()
    if st.button("Revisar 3", key='f_ex3_btn'):
        if "f" in ans3 and "1" in ans3 and "25" in ans3:
            st.success("¡Correcto! Sigue una $F(df_1=1, df_2=25)$.")
        else:
            st.error(f"Incorrecto. Respuesta: F(1, 25).")
        with st.expander("Ver Solución"):
            st.write(f"Una propiedad fundamental es que $t(\nu)^2 = F(1, \nu)$.")
            st.write("Por lo tanto, $t(25)^2 = F(1, 25)$.")
