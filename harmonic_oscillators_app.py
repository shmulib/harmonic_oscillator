import streamlit as st
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="Mass-Spring Damping Explorer", layout="wide")

st.title("🪀 Mass-Spring-Damper System Explorer")

st.markdown("""
Visualize the displacement of a damped harmonic oscillator with adjustable mass `m`, spring constant `k`, damping coefficient `b`, and initial position `x₀` and velocity `v₀`.

Click **'Add Trace'** to freeze the current curve and compare with others.
""")

# Sidebar – System Parameters
st.sidebar.header("System Parameters")
m = st.sidebar.slider("Mass (m)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
k = st.sidebar.slider("Spring constant (k)", min_value=0.1, max_value=20.0, value=4.0, step=0.1)
b = st.sidebar.slider("Damping coefficient (b)", min_value=0.0, max_value=20.0, value=4.0, step=0.1)
x0 = st.sidebar.slider("Initial position (x₀)", min_value=-10.0, max_value=10.0, value=1.0, step=0.1)
v0 = st.sidebar.slider("Initial velocity (v₀)", min_value=-10.0, max_value=10.0, value=0.0, step=0.1)
t_max = st.sidebar.slider("Duration (s)", min_value=2.0, max_value=30.0, value=10.0, step=1.0)
# --- Discriminant Display ---
discriminant = b**2 - 4 * m * k
damping_type = (
    "Overdamped" if discriminant > 0 else
    "Critically Damped" if discriminant == 0 else
    "Underdamped"
)

st.sidebar.markdown("### Damping Info")
st.sidebar.latex(r"\Delta = b^2 - 4mk")
st.sidebar.write(f"Discriminant: **{discriminant:.3f}**")
st.sidebar.write(f"Damping type: **{damping_type}**")

# # Sidebar – Animation Controls
# st.sidebar.header("Optional: Animate Parameter")

# animate_param = st.sidebar.selectbox("Animate which parameter?", ["None", "b", "m", "k", "x₀", "v₀"])
# if animate_param != "None":
#     anim_min = st.sidebar.number_input(f"Min value for {animate_param}", value=1.0)
#     anim_max = st.sidebar.number_input(f"Max value for {animate_param}", value=10.0)
#     animate = st.sidebar.button("🎞️ Animate")
# else:
#     animate = False

# Time array
t = np.linspace(0, t_max, 600)

# Damped oscillator solver
def solve_damped_oscillator(m, k, b, x0, v0, t):
    omega0 = np.sqrt(k / m)
    gamma = b / (2 * m)

    if gamma > omega0:  # overdamped
        delta = np.sqrt(gamma**2 - omega0**2)
        r1 = -gamma + delta
        r2 = -gamma - delta
        A = (v0 - r2 * x0) / (r1 - r2)
        B = (r1 * x0 - v0) / (r1 - r2)
        x = A * np.exp(r1 * t) + B * np.exp(r2 * t)
        damping_type = "Overdamped"
    elif gamma == omega0:  # critically damped
        x = np.exp(-gamma * t) * (x0 + (v0 + gamma * x0) * t)
        damping_type = "Critically Damped"
    else:  # underdamped
        omega_d = np.sqrt(omega0**2 - gamma**2)
        C = x0
        D = (v0 + gamma * x0) / omega_d
        x = np.exp(-gamma * t) * (C * np.cos(omega_d * t) + D * np.sin(omega_d * t))
        damping_type = "Underdamped"

    return x, damping_type

# Compute current solution
x, damping_type = solve_damped_oscillator(m, k, b, x0, v0, t)

# Session state for traces
if "traces" not in st.session_state:
    st.session_state.traces = []

# Buttons for adding and clearing traces
col1, col2 = st.columns([1, 5])
if col1.button("➕ Add Trace"):
    delta = b**2 - 4 * m * k
    damping_type = (
        "Overdamped" if delta > 0 else
        "Critically Damped" if np.isclose(delta, 0.0) else
        "Underdamped"
    )

    current_params = dict(b=b, m=m, k=k, x0=x0, v0=v0, delta=delta, damping_type=damping_type)

    # Get previous parameters for comparison
    if st.session_state.traces:
        _, _, prev_params, _ = st.session_state.traces[-1]
    else:
        prev_params = {}

    # Format and highlight changed parameters
    def fmt_param(key, val):
        changed = key in prev_params and not np.isclose(prev_params[key], val)
        return f"**{key}={val:.2f}**" if changed else f"{key}={val:.2f}"

    label = (
        f"{damping_type} (Δ = {delta:.2f}) | " +
        ", ".join([
            fmt_param("b", b),
            fmt_param("m", m),
            fmt_param("k", k),
            fmt_param("x0", x0),
            fmt_param("v0", v0)
        ])
    )

    # Store trace and full parameter set
    st.session_state.traces.append((t.copy(), x.copy(), current_params, label))

if col2.button("🧹 Clear Traces"):
    st.session_state.traces.clear()

# Plot current and past traces
fig = go.Figure()

fig.add_trace(go.Scatter(x=t, y=x, mode="lines", name=f"Current ({damping_type})", line=dict(width=2)))

for t_i, x_i, _, label in st.session_state.traces:
    fig.add_trace(go.Scatter(x=t_i, y=x_i, mode="lines", name=label, line=dict(width=2, dash="dash")))


fig.update_layout(
    height=600,
    xaxis_title="Time (s)",
    yaxis_title="Displacement x(t)",
    title="Damped Harmonic Oscillator",
    legend=dict(
    orientation="v",
        x=1.02,
        xanchor="left",
        y=1,
        yanchor="top",
        traceorder="normal"
    )
)

st.plotly_chart(fig, use_container_width=True)

# PNG Export
from plotly.graph_objs import Figure
import socket
from io import BytesIO

# Detect whether the app is running on Streamlit Community Cloud


is_cloud = "localhost" in socket.gethostname().lower() or "adminuser" in socket.gethostname().lower()

#st.write(socket.gethostname().lower())

custom_title = st.text_input("📛 Title for Exported Plot", "")

# Create export figure (traces only)
from plotly.graph_objs import Figure

export_fig = Figure()
export_fig.update_layout(
    title=custom_title,
    xaxis_title="Time (s)",
    yaxis_title="Displacement x(t)",
    template="plotly_white",
    width=1600,
    height=800,
    legend=dict(
        orientation="v",
        x=1.02,
        xanchor="left",
        y=1,
        yanchor="top",
        traceorder='normal',
        font=dict(size=12),
        itemsizing='constant'
    )
)

for t_i, x_i, _, label in st.session_state.traces:
    export_fig.add_trace(go.Scatter(x=t_i, y=x_i, mode="lines", name=label, line=dict(dash="dash")))

# HTML export (works everywhere)
export_html = export_fig.to_html(full_html=False, include_plotlyjs="cdn")
st.download_button(
    "📄 Download Traces as Interactive HTML",
    data=export_html,
    file_name="oscillator_plot.html",
    mime="text/html"
)

# PNG export only locally
if not is_cloud:
    buf = BytesIO()
    export_fig.write_image(buf, format="png", width=1600, height=800)
    st.download_button(
        "📥 Download Traces as PNG (High Res)",
        data=buf.getvalue(),
        file_name="oscillator_plot.png",
        mime="image/png"
    )
else:
    st.info("🖼️ PNG export is only available when running locally. \
To use this feature, click the GitHub icon (top-right) to access the repository and run the app on your machine.")



# if animate:
#     n_frames = 60
#     anim_values = np.linspace(anim_min, anim_max, n_frames)
#     slider_steps = []
#     param_key = animate_param if animate_param != "x₀" else "x0"

#     # Initial arguments
#     args = dict(b=b, m=m, k=k, x0=x0, v0=v0)

#     # Set initial value for animated parameter
#     args[param_key] = anim_values[0]
#     x_init, _ = solve_damped_oscillator(args["m"], args["k"], args["b"], args["x0"], args["v0"], t)

#     # Initial discriminant
#     D_init = args["b"]**2 - 4 * args["m"] * args["k"]

#     fig_title = (
#         f"Animation: Varying {animate_param} = {anim_values[0]:.2f} | "
#         f"m={args['m']}, k={args['k']}, b={args['b']}, x₀={args['x0']}, v₀={args['v0']} | "
#         f"Δ = {D_init:.3f}"
#     )

#     anim_fig = go.Figure(
#         data=[go.Scatter(x=t, y=x_init, mode="lines", name="")],
#         layout=go.Layout(
#             title=fig_title,
#             xaxis_title="Time (s)",
#             yaxis_title="Displacement x(t)",
#             updatemenus=[{
#                 "type": "buttons",
#                 "showactive": False,
#                 "buttons": [
#                     {"label": "▶️ Play", "method": "animate", "args": [None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True}]},
#                     {"label": "⏸️ Pause", "method": "animate", "args": [[None], {"frame": {"duration": 0}, "mode": "immediate"}]}
#                 ]
#             }]
#         )
#     )

#     frames_list = []

#     for val in anim_values:
#         args[param_key] = val
#         x_anim, _ = solve_damped_oscillator(args["m"], args["k"], args["b"], args["x0"], args["v0"], t)
#         D = args["b"]**2 - 4 * args["m"] * args["k"]

#         title = (
#             f"Animation: Varying {animate_param} = {val:.2f} | "
#             f"m={args['m']:.2f}, k={args['k']:.2f}, b={args['b']:.2f}, x₀={args['x0']:.2f}, v₀={args['v0']:.2f} | "
#             f"Δ = {D:.3f}"
#         )

#         frame = go.Frame(
#             data=[go.Scatter(x=t, y=x_anim, mode="lines", name="")],
#             name=f"{val:.4f}",
#             layout=go.Layout(title=title)
#         )
#         frames_list.append(frame)

#         slider_steps.append({
#             "method": "animate",
#             "args": [[f"{val:.4f}"], {"mode": "immediate", "frame": {"duration": 0}, "transition": {"duration": 0}}],
#             "label": f"{val:.2f}"
#         })

#     anim_fig.frames = frames_list

#     anim_fig.update_layout(
#         sliders=[{
#             "active": 0,
#             "currentvalue": {"prefix": f"{animate_param} = "},
#             "pad": {"t": 50},
#             "steps": slider_steps
#         }],
#         height=600,
#         legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
#     )

#     st.plotly_chart(anim_fig, use_container_width=True)
