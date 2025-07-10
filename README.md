
# 🪀 Mass-Spring-Damper System Explorer

An interactive [Streamlit](https://streamlit.io) app for visualizing the behavior of a damped harmonic oscillator under varying system parameters:

- Mass `m`
- Spring constant `k`
- Damping coefficient `b`
- Initial position `x₀`
- Initial velocity `v₀`

Explore underdamped, critically damped, and overdamped regimes. Add and compare multiple traces, and export interactive or high-resolution static plots.

---

## 🚀 Features

- 🎛️ Adjustable sliders for physical parameters  
- ➕ Save and compare multiple response traces  
- 📈 View discriminant \( \Delta = b^2 - 4mk \) and damping type in real time  
- 📤 Export plots as:
  - Interactive HTML (🟢 works everywhere)
  - High-resolution PNG (🟢 local only)

---

## 🖼️ Run Locally for PNG Export

This app works on [Streamlit Cloud](https://streamlit.io/cloud), but **PNG export requires running locally** due to Plotly’s image rendering engine (`kaleido`).

### 🧰 Local Setup Instructions

1. 📥 **Clone the repository**
   ```
   git clone https://github.com/shmulib/harmonic_oscillator.git
   cd harmonic_oscillator
   ```

2. 🐍 **(Optional)** Create and activate a virtual environment
   ```
   python -m venv .venv
   source .venv/bin/activate        # On Windows: .venv\Scripts\activate
   ```

3. 📦 **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. 🚀 **Run the app**
   ```
   streamlit run harmonic_oscillators_app.py
   ```

5. 🖼️ **Now you can export high-resolution PNGs** directly from the UI.
