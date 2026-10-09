# Image Transmission Simulator

An interactive Streamlit simulator for image transmission with bit-flip noise, NRZ-like visualization, image restoration and bit/pixel error analysis.

## Problem and solution

The app makes channel corruption visible: an uploaded image is converted to bits, randomly corrupted, reconstructed and filtered. Users compare original, noisy and restored images and download the restored result. It is an educational digital-transmission simulation.

**Stack:** Python, Streamlit, NumPy, SciPy, Pillow and Matplotlib.

## Architecture

`app.py` combines image handling, bit conversion, noise simulation, filtering, metrics and presentation. `requirements.txt` lists dependencies. The app is self-contained and requires no model files or database.

## Installation and usage

```bash
git clone https://github.com/zik4O4/chaine_transmission_numerique.git
cd chaine_transmission_numerique
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

On Windows activate `.venv\Scripts\Activate.ps1`. Open the local URL displayed by Streamlit.

1. Upload a PNG, JPG/JPEG, BMP or TIFF image; the app resizes it to 128 × 128.
2. Select a noise probability from 0% to 50%.
3. Choose no filter, median (3 × 3), Gaussian (sigma = 1), or mean (3 × 3).
4. Simulate and compare images, signals and metrics.
5. Download the restored image as PNG.

The existing [online demo reference](https://chaine.streamlit.app) is retained; live availability has not been verified.

## Metrics and limitations

Pixel error is the percentage of pixel values that differ from the original. Bit error compares the corresponding original and corrupted bit arrays. Random bit flips model a binary symmetric channel; the filters operate on reconstructed pixel values, not as error-correcting codes.

Noise is stochastic, so repeated runs can differ. NRZ-like plots visualize a short sample of bits, not a physically calibrated waveform. Package versions are unpinned; no real-channel or hardware performance benchmark is claimed.

## License

No repository-level license has been selected. Third-party dependency terms apply separately.
