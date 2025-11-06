import streamlit as st
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# --- Funciones de Ayuda (Helpers) ---
# Movimos estas funciones aquí para que cualquier página pueda importarlas
# y no tengamos que repetir código.

@st.cache_data
def plot_discrete_distribution(_dist_obj, k_values, title):
    """
    Genera un gráfico de barras (PMF) para una distribución discreta.
    
    Args:
        dist_obj: Un objeto de distribución de scipy.stats (ej. stats.binom(n, p)).
        k_values: Una lista o array de numpy de los valores 'k' (eje x).
        title (str): El título del gráfico.
    
    Returns:
        matplotlib.figure.Figure: La figura generada.
    """
    pmf_values = dist_obj.pmf(k_values)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(k_values, pmf_values, label='PMF (Probabilidad)', color='skyblue', edgecolor='black')
    
    # Añadir línea de la media
    mean = dist_obj.mean()
    ax.axvline(mean, color='red', linestyle='--', linewidth=2, label=f'Media ({mean:.2f})')
    
    ax.set_title(title, fontsize=16)
    ax.set_xlabel('Valor (k)', fontsize=12)
    ax.set_ylabel('Probabilidad P(X=k)', fontsize=12)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Ajustar ticks del eje x para que sean enteros si es posible
    if all(isinstance(k, (int, np.integer)) for k in k_values) and len(k_values) < 30:
        ax.set_xticks(k_values)
        
    return fig

@st.cache_data
def plot_continuous_distribution(dist_obj, x_min, x_max, title):
    """
    Genera un gráfico de línea (PDF) para una distribución continua.
    
    Args:
        dist_obj: Un objeto de distribución de scipy.stats (ej. stats.norm(mu, sigma)).
        x_min (float): Límite inferior del eje x.
        x_max (float): Límite superior del eje x.
        title (str): El título del gráfico.
    
    Returns:
        matplotlib.figure.Figure: La figura generada.
    """
    x_values = np.linspace(x_min, x_max, 500)
    pdf_values = dist_obj.pdf(x_values)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_values, pdf_values, label='PDF (Densidad)', color='royalblue', linewidth=2)
    ax.fill_between(x_values, pdf_values, color='royalblue', alpha=0.2)
    
    # Añadir línea de la media
    mean = dist_obj.mean()
    ax.axvline(mean, color='red', linestyle='--', linewidth=2, label=f'Media ({mean:.2f})')
    
    ax.set_title(title, fontsize=16)
    ax.set_xlabel('Valor (x)', fontsize=12)
    ax.set_ylabel('Densidad de Probabilidad', fontsize=12)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_ylim(bottom=0)
    
    return fig
