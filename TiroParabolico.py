import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from math import cos, sin, radians

# Page Configuration
st.set_page_config(page_title="Parabolic Motion Simulator", layout="wide")
st.title("Parabolic Motion Simulator")

# Sidebar for initial parameters
with st.sidebar:
    st.subheader("Initial Parameters")

    velocity = st.number_input("Velocity (m/s)", 0.0, 100.0, 20.0)
    angle = st.number_input("Angle (°)", 0.0, 90.0, 45.0)
    initial_height = st.number_input("Initial Height (m)", 0.0, 50.0, 0.0)
    gravity = st.number_input("Gravity (m/s²)", 1.0, 20.0, 9.81)
    
    show_vectors = st.checkbox("Show Velocity Vectors", value=True)
    compare = st.checkbox("Compare Trajectories")

    if compare:
        st.subheader("Second Trajectory")
        velocity2 = st.number_input("Velocity 2 (m/s)", 0.0, 100.0, 30.0)
        angle2 = st.number_input("Angle 2 (°)", 0.0, 90.0, 60.0)

    run_simulation = st.button("Run Simulation")



# Generate the plot only when the button is pressed
if run_simulation:
    angle_rad = radians(angle)
    v0x = velocity * cos(angle_rad)
    v0y = velocity * sin(angle_rad)

    if v0y**2 + 2*gravity*initial_height < 0:
        st.error("The current parameters do not produce a valid trajectory")
    else:
        flight_time = (v0y + np.sqrt(v0y**2 + 2*gravity*initial_height)) / gravity
        t = np.linspace(0, flight_time, 100)
        x = v0x * t
        y = initial_height + v0y * t - 0.5 * gravity * t**2

        
        # Create main plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, name='Trajectory 1', line=dict(color='#2563eb', width=2)))

        if compare:
            angle_rad2 = radians(angle2)
            v0x2 = velocity2 * cos(angle_rad2)
            v0y2 = velocity2 * sin(angle_rad2)
            flight_time2 = (v0y2 + np.sqrt(v0y2**2 + 2*gravity*initial_height)) / gravity
            t2 = np.linspace(0, flight_time2, 100)
            x2 = v0x2 * t2
            y2 = initial_height + v0y2 * t2 - 0.5 * gravity * t2**2
            fig.add_trace(go.Scatter(x=x2, y=y2, name='Trajectory 2', line=dict(color='#dc2626', width=2)))

        if show_vectors:
            N = 10
            fig.add_trace(go.Scatter(x=x[::N], y=y[::N], mode='markers+text', text=['→']*len(x[::N]), textposition="middle center"))

        fig.update_layout(title='Projectile Trajectory', xaxis_title='Distance (m)', yaxis_title='Height (m)')
        st.plotly_chart(fig)

        # Display equations
        st.subheader("Equations of Motion")
        st.latex(r"x(t) = v_0\cos(\theta)t")
        st.latex(r"y(t) = h_0 + v_0\sin(\theta)t - \frac{1}{2}gt^2")
