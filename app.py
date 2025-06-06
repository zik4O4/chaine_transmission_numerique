import streamlit as st
import numpy as np
from PIL import Image
from scipy.ndimage import median_filter, gaussian_filter, uniform_filter
import matplotlib.pyplot as plt
import io

# Configuration de la page
st.set_page_config(
    page_title="Chaîne de Transmission d'Image",
    page_icon="ZY",
    layout="wide"
)

# Initialisation des variables de session
if 'original_array' not in st.session_state:
    st.session_state.original_array = None
if 'restored_array' not in st.session_state:
    st.session_state.restored_array = None
if 'clean_nrz_signal' not in st.session_state:
    st.session_state.clean_nrz_signal = None
if 'noisy_nrz_signal' not in st.session_state:
    st.session_state.noisy_nrz_signal = None
if 'restored_nrz_signal' not in st.session_state:
    st.session_state.restored_nrz_signal = None

def apply_filter(image, method):
    """Applique le filtre sélectionné à l'image"""
    if image is None or image.size == 0:
        return np.zeros((128, 128), dtype=np.uint8)
    try:
        if method == "Médian (3x3)":
            return median_filter(image, size=3)
        elif method == "Gaussien (σ=1)":
            return gaussian_filter(image, sigma=1)
        elif method == "Moyen (3x3)":
            return uniform_filter(image, size=3)
        return image.copy()
    except Exception as e:
        st.error(f"Erreur lors de l'application du filtre: {e}")
        return image

def calculate_error_rate(original, restored):
    """Calcule le taux d'erreur entre l'image originale et restaurée"""
    try:
        if original is None or restored is None or original.size == 0 or restored.size == 0:
            return 0.0
        diff = np.abs(original.astype(int) - restored.astype(int))
        error_pixels = np.count_nonzero(diff)
        total = original.size
        return round(100 * error_pixels / total, 2)
    except Exception as e:
        st.error(f"Erreur dans le calcul du taux d'erreur: {e}")
        return 0.0

def calculate_bit_error_rate(original_bits, noisy_bits):
    """Calcule le taux d'erreur binaire"""
    try:
        if original_bits is None or noisy_bits is None or len(original_bits) == 0:
            return 0.0
        min_len = min(len(original_bits), len(noisy_bits))
        errors = np.sum(original_bits[:min_len] != noisy_bits[:min_len])
        total = min_len
        return round(100 * errors / total, 2)
    except Exception as e:
        st.error(f"Erreur dans le calcul du taux d'erreur binaire: {e}")
        return 0.0

def simulate_nrz_noise(image_array, noise_prob):
    """Simule le bruit sur le signal NRZ"""
    try:
        if image_array is None or image_array.size == 0:
            return np.zeros((128, 128), dtype=np.uint8), np.array([]), np.array([])
        
        bits = np.unpackbits(image_array)
        nrz_signal = bits.copy()
        noise = np.random.rand(len(bits)) < noise_prob
        noisy_nrz = nrz_signal.copy()
        noisy_nrz[noise] = 1 - noisy_nrz[noise]

        packed = np.packbits(noisy_nrz)
        target_shape = image_array.shape
        padded = np.resize(packed, np.prod(target_shape))
        noisy_image = padded.reshape(target_shape).astype(np.uint8)
        return noisy_image, nrz_signal, noisy_nrz
    except Exception as e:
        st.error(f"Erreur lors de la simulation NRZ: {e}")
        return np.zeros_like(image_array), np.array([]), np.array([])

def plot_nrz_signals():
    """Génère les graphiques des signaux NRZ"""
    try:
        if st.session_state.clean_nrz_signal is None or len(st.session_state.clean_nrz_signal) == 0:
            return None
        
        sample_size = min(100, len(st.session_state.clean_nrz_signal))
        clean_sample = st.session_state.clean_nrz_signal[:sample_size]
        noisy_sample = st.session_state.noisy_nrz_signal[:sample_size] if st.session_state.noisy_nrz_signal is not None else clean_sample
        restored_sample = st.session_state.restored_nrz_signal[:sample_size] if st.session_state.restored_nrz_signal is not None else clean_sample

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8))
        fig.suptitle('Signaux NRZ - Transmission Numérique', fontsize=14, fontweight='bold')
        t = np.arange(sample_size)

        # Signal original
        ax1.plot(t, clean_sample, 'b-', linewidth=2, label='Signal Original')
        ax1.fill_between(t, 0, clean_sample, alpha=0.3, color='blue')
        ax1.set_ylabel('Amplitude')
        ax1.set_title('1. Signal NRZ Original')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(-0.1, 1.1)
        ax1.legend()

        # Signal bruité
        ax2.plot(t, noisy_sample, 'r-', linewidth=2, label='Signal Bruité')
        ax2.fill_between(t, 0, noisy_sample, alpha=0.3, color='red')
        errors = clean_sample != noisy_sample
        error_indices = t[errors]
        if len(error_indices) > 0:
            ax2.scatter(error_indices, noisy_sample[errors], color='orange', s=50, zorder=5,
                        label=f'Erreurs ({len(error_indices)})')
        ax2.set_ylabel('Amplitude')
        ax2.set_title('2. Signal NRZ Bruité')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(-0.1, 1.1)
        ax2.legend()

        # Signal restauré
        ax3.plot(t, restored_sample, 'g-', linewidth=2, label='Signal Restauré')
        ax3.fill_between(t, 0, restored_sample, alpha=0.3, color='green')
        final_errors = clean_sample != restored_sample
        final_error_indices = t[final_errors]
        if len(final_error_indices) > 0:
            ax3.scatter(final_error_indices, restored_sample[final_errors], color='purple', s=50, zorder=5,
                        label=f'Erreurs résiduelles ({len(final_error_indices)})')
        ax3.set_xlabel('Index des bits')
        ax3.set_ylabel('Amplitude')
        ax3.set_title('3. Signal NRZ Restauré')
        ax3.grid(True, alpha=0.3)
        ax3.set_ylim(-0.1, 1.1)
        ax3.legend()

        plt.tight_layout()
        return fig
    except Exception as e:
        st.error(f"Erreur lors de la génération des graphiques: {e}")
        return None

# Interface utilisateur
st.title("Simulation d'une Transmission Numérique d'Image")
st.markdown("---")

# Sidebar pour les paramètres
st.sidebar.header("Paramètres de simulation")

# Upload d'image
uploaded_file = st.sidebar.file_uploader(
    "Charger une image", 
    type=['png', 'jpg', 'jpeg', 'bmp', 'tiff']
)

if uploaded_file is not None:
    try:
        img = Image.open(uploaded_file).convert("L").resize((128, 128), Image.Resampling.LANCZOS)
        st.session_state.original_array = np.array(img, dtype=np.uint8)
        st.sidebar.success("Image chargée avec succès!")
    except Exception as e:
        st.sidebar.error(f"Erreur lors du chargement: {e}")

# Paramètres de simulation
noise_level = st.sidebar.slider("Taux de bruit (%)", 0, 50, 10)
filter_type = st.sidebar.selectbox(
    "Type de filtre",
    ["Aucun", "Médian (3x3)", "Gaussien (σ=1)", "Moyen (3x3)"]
)

# Bouton de simulation
simulate_button = st.sidebar.button(" Simuler la transmission", type="primary")

# Interface principale
if st.session_state.original_array is not None:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Image originale")
        st.image(st.session_state.original_array, caption="Image originale", use_column_width=True)
    
    if simulate_button:
        with st.spinner("Simulation en cours..."):
            try:
                noise_prob = noise_level / 100.0
                noisy_array, clean_nrz_signal, noisy_nrz_signal = simulate_nrz_noise(
                    st.session_state.original_array, noise_prob
                )
                
                restored_array = apply_filter(noisy_array, filter_type)
                
                # Mise à jour des variables de session
                st.session_state.restored_array = restored_array
                st.session_state.clean_nrz_signal = clean_nrz_signal
                st.session_state.noisy_nrz_signal = noisy_nrz_signal
                
                if restored_array is not None:
                    restored_bits = np.unpackbits(restored_array.astype(np.uint8))
                    if len(restored_bits) > len(clean_nrz_signal):
                        restored_bits = restored_bits[:len(clean_nrz_signal)]
                    else:
                        restored_bits = np.pad(restored_bits, (0, len(clean_nrz_signal) - len(restored_bits)), mode='constant')
                    st.session_state.restored_nrz_signal = restored_bits
                
                st.success("Simulation terminée!")
                
            except Exception as e:
                st.error(f"Erreur pendant la simulation: {e}")
    
    # Affichage des résultats
    if st.session_state.restored_array is not None:
        with col2:
            st.subheader("Image bruitée")
            noisy_display = simulate_nrz_noise(st.session_state.original_array, noise_level/100.0)[0]
            st.image(noisy_display, caption="Image bruitée", use_column_width=True)
        
        with col3:
            st.subheader("Image restaurée")
            st.image(st.session_state.restored_array, caption="Image restaurée", use_column_width=True)
        
        # Calcul et affichage des statistiques
        err_pixel = calculate_error_rate(st.session_state.original_array, st.session_state.restored_array)
        err_bit = calculate_bit_error_rate(st.session_state.clean_nrz_signal, st.session_state.restored_nrz_signal)
        
        st.markdown("---")
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("Taux d'erreur pixels", f"{err_pixel}%")
        with col_stat2:
            st.metric("Taux d'erreur bits", f"{err_bit}%")
        
        # Graphiques des signaux NRZ
        st.markdown("---")
        st.subheader("📊 Visualisation des Signaux NRZ")
        
        fig = plot_nrz_signals()
        if fig is not None:
            st.pyplot(fig)
        
        # Bouton de téléchargement
        st.markdown("---")
        if st.button("💾 Télécharger l'image restaurée"):
            try:
                img_pil = Image.fromarray(st.session_state.restored_array.astype(np.uint8))
                buf = io.BytesIO()
                img_pil.save(buf, format='PNG')
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="Cliquez pour télécharger",
                    data=byte_im,
                    file_name="image_restauree.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"Erreur lors de la préparation du téléchargement: {e}")

else:
    st.info(" Veuillez charger une image dans la barre latérale pour commencer.")
    
    # Affichage d'une image d'exemple
    st.markdown("---")
    st.subheader("À propos de cette application")
    st.markdown("""
    Cette application simule une chaîne de transmission numérique d'image avec :
    
    - **Conversion NRZ** : Transformation de l'image en signal binaire
    - **Simulation de bruit** : Ajout d'erreurs aléatoires
    - **Filtrage** : Application de différents filtres de restauration
    - **Analyse des performances** : Calcul des taux d'erreur
    
    **Comment utiliser :**
    1. Chargez une image via la barre latérale
    2. Ajustez les paramètres (taux de bruit, type de filtre)
    3. Cliquez sur "Simuler la transmission"
    4. Analysez les résultats et téléchargez l'image restaurée
    """)

# Footer
st.markdown("---")
st.markdown("*Application de simulation de transmission numérique d'image*")
