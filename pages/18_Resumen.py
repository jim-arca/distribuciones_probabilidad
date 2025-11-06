import streamlit as st
import numpy as np

# --- Contenido de la Página ---

st.title("Resumen y Próximos Pasos")
st.image("https://placehold.co/600x300/003366/FFFFFF?text=Mapa+de+Distribuciones", use_column_width=True)

st.header("¡Felicitaciones!")
st.write("""
Has completado el recorrido por las distribuciones de probabilidad más fundamentales de la estadística. 
Ahora posees un "catálogo" de herramientas que te permite modelar una increíble variedad de fenómenos del mundo real, desde eventos tan simples como lanzar una moneda hasta procesos complejos como el precio de las acciones o la vida útil de un componente.
""")

st.header("El Mapa de las Distribuciones")
st.write("Ninguna distribución vive aislada. Lo más poderoso es entender cómo se relacionan entre sí.")

st.subheader("1. La Base: Bernoulli")
st.markdown("""
- Un **Ensayo de Bernoulli** (un solo $p$) es el átomo.
- Si **sumas** $n$ ensayos de Bernoulli $\to$ **Distribución Binomial** (contar éxitos en $n$ intentos).
- Si cuentas los ensayos **hasta el primer éxito** $\to$ **Distribución Geométrica**.
- Si sacas una muestra **sin reemplazo** de una población de Bernoullis $\to$ **Distribución Hipergeométrica**.
""")

st.subheader("2. El Límite: Poisson y Normal")
st.markdown("""
- Si tomas una **Binomial** con $n$ muy grande y $p$ muy pequeña (eventos raros) $\to$ **Distribución de Poisson** (contar eventos en un intervalo).
- Si tomas una **Binomial** o una **Poisson** con parámetros grandes (gracias al Teorema del Límite Central) $\to$ **Distribución Normal**.
""")

st.subheader("3. El Tiempo y la Espera")
st.markdown("""
- Si los *conteos* siguen una **Poisson** (eventos/hora) $\to$ el *tiempo entre* eventos sigue una **Distribución Exponencial** (tasa de fallo constante).
- Si la **Exponencial** es el tiempo hasta el *primer* evento $\to$ la **Distribución Gamma** es el tiempo hasta el *$k$-ésimo* evento.
- La **Distribución de Weibull** generaliza a la Exponencial (tasa de fallo variable, $k \neq 1$).
""")

st.subheader("4. El Mundo de la Inferencia (Basadas en la Normal)")
st.markdown("""
- Si $X \sim \text{Normal}$, entonces $\ln(X) \sim$ **Lognormal**.
- Si tomas $Z \sim \text{Normal}(0,1)$ y la elevas al cuadrado ($Z^2$) $\to$ **Distribución Chi-Cuadrado ($\chi^2$)** con $k=1$.
- Si $X \sim \text{Normal}(0,1)$ y $Y \sim \chi^2(k)$ $\to$ $\frac{X}{\sqrt{Y/k}} \sim$ **Distribución t de Student**. (La base de las pruebas t).
- Si $X \sim \chi^2(k_1)$ y $Y \sim \chi^2(k_2)$ $\to$ $\frac{X/k_1}{Y/k_2} \sim$ **Distribución F**. (La base de ANOVA).
""")

st.subheader("5. Las "Otras" Fundamentales")
st.markdown("""
- Si todo es igualmente probable en $[a, b]$ $\to$ **Distribución Uniforme** (Discreta o Continua).
- Si modelas una **probabilidad** o **proporción** (un valor en $[0, 1]$) $\to$ **Distribución Beta**. (Beta(1, 1) es la Uniforme).
- Si solo conoces el mínimo, máximo y más probable $\to$ **Distribución Triangular**.
""")

st.header("Próximos Pasos en tu Aprendizaje")
st.write("Ahora que dominas los "qué", estás listo para los "cómo" y "por qué":")

st.markdown("""
1.  **Teorema del Límite Central (TLC):** Estudia a fondo por qué la Distribución Normal es tan importante y cómo emerge de la suma de otras distribuciones.
2.  **Estadística Inferencial:** Aplica estas distribuciones. Aprende a construir **Intervalos de Confianza** y a realizar **Pruebas de Hipótesis** (Pruebas Z, Pruebas t, Pruebas $\chi^2$, ANOVA).
3.  **Inferencia Bayesiana:** Explora cómo usar la Distribución Beta (para probabilidades) y Gamma (para tasas) como "distribuciones a priori" para actualizar tu conocimiento a medida que obtienes nuevos datos.
4.  **Modelos de Regresión:** Usa la Normal, Binomial y Poisson como base para construir modelos predictivos (Regresión Lineal, Regresión Logística, Regresión de Poisson).
5.  **Procesos Estocásticos:** Investiga cómo estas distribuciones se usan en secuencias de tiempo, como en las Cadenas de Markov.
""")
