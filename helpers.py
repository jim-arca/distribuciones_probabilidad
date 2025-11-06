import streamlit as st
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# --- Funciones de Ayuda (Helpers) ---
# Este archivo contiene las correcciones para AMBAS funciones.

@st.cache_data
def plot_discrete_distribution(_dist_obj, k_values, title):
    """
    Genera un gráfico de barras (PMF) para una distribución discreta.
    
    CORRECCIÓN: El argumento se renombra a '_dist_obj' para
    indicarle a Streamlit que no intente hashearlo.
    """
    # Usamos la variable con guion bajo: _dist_obj
    pmf_values = _dist_obj.pmf(k_values)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(k_values, pmf_values, label=r'PMF P(X=k)', color='skyblue', edgecolor='black', zorder=2)
    
    # Añadir línea de la media
    mean = _dist_obj.mean() # Usamos _dist_obj aquí también
    ax.axvline(mean, color='red', linestyle='--', linewidth=2, label=f'Media ({mean:.2f})', zorder=3)
    
    ax.set_title(title, fontsize=16)
    ax.set_xlabel('Valor (k)', fontsize=12)
    ax.set_ylabel(r'Probabilidad P(X=k)', fontsize=12) 
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)
    
    # Ajustar ticks del eje x para que sean enteros si es posible
    if len(k_values) > 1:
        int_k_values = np.unique(np.asarray(k_values).astype(int))
        if len(int_k_values) < 30:
            ax.set_xticks(int_k_values)
        else:
            ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    
    return fig

@st.cache_data
def plot_continuous_distribution(_dist_obj, x_min, x_max, title):
    """
    Genera un gráfico de línea (PDF) para una distribución continua.
    
    CORRECCIÓN: El argumento se renombra a '_dist_obj' 
    para evitar el error de hash de Streamlit.
    """
    x_values = np.linspace(x_min, x_max, 500)
    # --- CORRECIÓN APLICADA ---
    # Usamos la variable con guion bajo: _dist_obj
    pdf_values = _dist_obj.pdf(x_values)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_values, pdf_values, label=r'PDF f(x)', color='royalblue', linewidth=2, zorder=2)
    ax.fill_between(x_values, pdf_values, color='royalblue', alpha=0.2, zorder=1)
    
    # Añadir línea de la media
    mean = _dist_obj.mean() # Usamos _dist_obj aquí también
    ax.axvline(mean, color='red', linestyle='--', linewidth=2, label=f'Media ({mean:.2f})', zorder=3)
    
    ax.set_title(title, fontsize=16)
    ax.set_xlabel('Valor (x)', fontsize=12)
    ax.set_ylabel(r'Densidad de Probabilidad f(x)', fontsize=12)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)
    ax.set_ylim(bottom=0)
    
    return fig
