import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Constantes
MAC = 1152
CG_MIN = 19
CG_MAX = 30
CG_IDEAL_MIN = 20
CG_IDEAL_MAX = 23

st.set_page_config(page_title="MD3 CG Calculator", layout="wide")

st.title("✈️ MD3 CG Calculator")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Dados de Entrada")

    empty_weight = st.number_input("Peso Vazio (kg)", value=321.1)
    empty_cg = st.number_input("CG Vazio (mm)", value=216.5)

    pilot_weight = st.number_input("Peso Piloto (kg)", value=70.0)
    copilot_weight = st.number_input("Peso Copiloto (kg)", value=0.0)

    seat_arm = st.number_input("Braço Assentos (mm)", value=300.0)

    fuel_liters = st.slider("Combustível (L)", 0, 92, 0)
    fuel_arm = st.number_input("Braço Combustível (mm)", value=250.0)

# Cálculos
fuel_weight = fuel_liters * 0.72

fixed_moment = empty_weight * empty_cg
pilot_moment = pilot_weight * seat_arm
copilot_moment = copilot_weight * seat_arm
fuel_moment = fuel_weight * fuel_arm

total_weight = empty_weight + pilot_weight + copilot_weight + fuel_weight
total_moment = fixed_moment + pilot_moment + copilot_moment + fuel_moment

cg = total_moment / total_weight
mac_percent = (cg / MAC) * 100

with col2:
    st.subheader("Resultados")

    st.metric("Peso Total (kg)", f"{total_weight:.1f}")
    st.metric("CG (mm)", f"{cg:.1f}")
    st.metric("% MAC", f"{mac_percent:.2f}")

    if mac_percent < CG_MIN or mac_percent > CG_MAX:
        st.error("FORA DO ENVELOPE")
    elif CG_IDEAL_MIN <= mac_percent <= CG_IDEAL_MAX:
        st.success("ZONA IDEAL")
    else:
        st.warning("DENTRO DO LIMITE")

# Gráfico Envelope
st.subheader("Envelope CG (% MAC)")

fig, ax = plt.subplots()

ax.set_xlim(0, 600)
ax.set_ylim(15, 35)

ax.set_xlabel("Peso (kg)")
ax.set_ylabel("% MAC")

# Envelope
ax.axhspan(CG_MIN, CG_MAX, alpha=0.1)
ax.axhspan(CG_IDEAL_MIN, CG_IDEAL_MAX, alpha=0.2)

# Posição atual
ax.axvline(total_weight)
ax.axhline(mac_percent)

st.pyplot(fig)
