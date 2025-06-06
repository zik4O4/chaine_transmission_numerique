# 📡 Simulation de Transmission Numérique d'Image

Une application web interactive pour simuler une chaîne de transmission numérique d'image avec analyse des signaux NRZ et techniques de restauration.

## 🌟 Fonctionnalités

- **Chargement d'images** : Support des formats PNG, JPG, JPEG, BMP, TIFF
- **Simulation NRZ** : Conversion d'image en signal binaire Non-Return-to-Zero
- **Simulation de bruit** : Ajout d'erreurs aléatoires configurables (0-50%)
- **Filtrage adaptatif** : Multiples techniques de restauration
- **Analyse des performances** : Calcul des taux d'erreur pixels et bits
- **Visualisation interactive** : Graphiques des signaux avant/après transmission
- **Export des résultats** : Téléchargement des images restaurées

## 🚀 Démo en ligne

[Accéder à l'application](https://chaine.streamlit.app/)

## 🛠️ Installation locale

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation

1. **Clonez le repository**
   ```bash
   git clone https://github.com/zik4O4/chaine_transmission_numerique.git
   cd transmission-image-simulator
   ```

2. **Installez les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancez l'application**
   ```bash
   streamlit run app.py
   ```

4. **Accédez à l'application**
   - Ouvrez votre navigateur à l'adresse : `http://localhost:8501`

## 📋 Utilisation

### Étapes de simulation

1. **Chargement d'image**
   - Cliquez sur "Charger une image" dans la barre latérale
   - Sélectionnez une image (formats supportés : PNG, JPG, JPEG, BMP, TIFF)
   - L'image sera automatiquement redimensionnée en 128x128 pixels

2. **Configuration des paramètres**
   - **Taux de bruit** : Ajustez le curseur (0-50%)
   - **Type de filtre** : Choisissez parmi :
     - Aucun (pas de filtrage)
     - Médian (3x3) - Optimal pour le bruit impulsionnel
     - Gaussien (σ=1) - Lissage général
     - Moyen (3x3) - Réduction de bruit uniforme

3. **Simulation**
   - Cliquez sur "🚀 Simuler la transmission"
   - Observez les résultats en temps réel

4. **Analyse des résultats**
   - Visualisez les 3 versions de l'image
   - Consultez les métriques de performance
   - Analysez les graphiques des signaux NRZ

5. **Export**
   - Téléchargez l'image restaurée au format PNG

## 📊 Métriques de performance

### Taux d'erreur pixels
Pourcentage de pixels différents entre l'image originale et restaurée :
```
Taux erreur pixels = (Pixels différents / Total pixels) × 100
```

### Taux d'erreur bits
Pourcentage de bits erronés dans la représentation binaire :
```
Taux erreur bits = (Bits erronés / Total bits) × 100
```

## 🔬 Aspects techniques

### Signal NRZ (Non-Return-to-Zero)
- Conversion de l'image en représentation binaire
- Chaque pixel → 8 bits
- Signal binaire : 0V pour '0', +V pour '1'

### Simulation de canal bruité
- Modèle de bruit binaire symétrique
- Probabilité d'erreur configurable
- Inversion aléatoire des bits

### Techniques de filtrage

| Filtre | Usage optimal | Avantages |
|--------|---------------|-----------|
| Médian | Bruit impulsionnel | Préserve les contours |
| Gaussien | Bruit gaussien | Lissage uniforme |
| Moyen | Bruit uniforme | Simple et rapide |

## 📁 Structure du projet

```
transmission-image-simulator/
├── app.py              # Application Streamlit principale
├── requirements.txt    # Dépendances Python
├── README.md          # Documentation
└── .streamlit/        # Configuration Streamlit (optionnel)
    └── config.toml
```

## 🔧 Dépendances

- **streamlit** ≥1.28.0 : Framework web
- **numpy** ≥1.24.0 : Calculs numériques
- **Pillow** ≥9.5.0 : Traitement d'images
- **scipy** ≥1.10.0 : Filtres scientifiques
- **matplotlib** ≥3.7.0 : Génération de graphiques


## 🎯 Cas d'usage

### Éducation
- **Cours de télécommunications** : Démonstration pratique des concepts NRZ
- **Traitement du signal** : Visualisation des effets du bruit
- **Théorie de l'information** : Calcul des taux d'erreur

### Recherche
- **Évaluation d'algorithmes** : Test de nouvelles techniques de filtrage
- **Analyse comparative** : Comparaison de différentes méthodes
- **Prototypage rapide** : Validation de concepts

### Ingénierie
- **Formation technique** : Simulation de systèmes réels
- **Validation de systèmes** : Test de robustesse aux perturbations

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. **Forkez le projet**
2. **Créez une branche feature** (`git checkout -b feature/AmazingFeature`)
3. **Committez vos changements** (`git commit -m 'Add AmazingFeature'`)
4. **Poussez vers la branche** (`git push origin feature/AmazingFeature`)
5. **Ouvrez une Pull Request**

### Idées de contributions
- [ ] Support d'autres formats d'image (GIF, WebP)
- [ ] Nouveaux types de filtres (Wiener, adaptatif)
- [ ] Modes de bruit avancés (gaussien, Poisson)
- [ ] Export des graphiques en PDF
- [ ] Interface multilingue
- [ ] Traitement par lots d'images

## 📞 Support

### Problèmes courants

**L'application ne se lance pas**
- Vérifiez la version Python (≥3.8)
- Réinstallez les dépendances : `pip install -r requirements.txt`

**Erreur de mémoire avec de grandes images**
- Les images sont automatiquement redimensionnées en 128x128
- Réduisez la taille avant chargement si nécessaire

**Graphiques ne s'affichent pas**
- Problème possible avec matplotlib backend
- Relancez l'application : `streamlit run app.py`

## 🙏 Remerciements

- Communauté Streamlit pour le framework excellent
- Équipes NumPy, SciPy, Matplotlib pour les outils scientifiques
- Contributeurs et utilisateurs de l'application

---
