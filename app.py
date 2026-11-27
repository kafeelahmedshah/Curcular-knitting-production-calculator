import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Circular Knitting Production Calculator",
    page_icon="🧶",
    layout="wide"
)

st.markdown("""
<style>
.stApp {background: #f5f8fc;}
.block-container {padding-top: 1.7rem; max-width: 1050px;}
.hero {
    background: linear-gradient(120deg, #17365d, #2878a5);
    color: white; padding: 1.5rem 1.7rem; border-radius: 16px;
    margin-bottom: 1.2rem;
}
.hero h1 {color: white; margin: 0 0 .35rem 0;}
.hero p {color: #eaf4fb; margin: 0;}
div[data-testid="stMetric"] {
    background: white; border: 1px solid #e2eaf2;
    padding: 13px; border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🧶 Circular Knitting Production Calculator</h1>
    <p>Estimate daily knitted fabric production from machine RPM, feeders and fabric GSM.</p>
</div>
""", unsafe_allow_html=True)

st.write(
    "Enter the machine and fabric details to estimate the theoretical daily fabric output. "
    "You can also include machine efficiency and operating hours for a more practical estimate."
)

with st.sidebar:
    st.header("About this App")
    st.write("A textile engineering student tool for estimating circular knitting machine production.")
    st.caption("Roll Number: 25TE037")
    st.caption("Department: Textile Engineering")
    st.divider()
    st.caption("The calculation is an estimate. Actual output depends on machine gauge, stitch length, yarn properties, downtime and other production conditions.")

st.subheader("1. Machine Parameters")
c1, c2 = st.columns(2)
with c1:
    rpm = st.number_input("Machine speed (RPM)", min_value=1.0, max_value=100.0, value=25.0, step=1.0,
                          help="Rotations per minute of the circular knitting machine.")
    feeders = st.number_input("Number of feeders", min_value=1, max_value=200, value=90, step=1)
with c2:
    efficiency = st.slider("Machine efficiency (%)", min_value=1, max_value=100, value=85)
    hours = st.number_input("Working hours per day", min_value=1.0, max_value=24.0, value=20.0, step=0.5)

st.subheader("2. Fabric Parameters")
f1, f2 = st.columns(2)
with f1:
    gsm = st.number_input("Fabric GSM (g/m²)", min_value=1.0, max_value=1500.0, value=180.0, step=5.0)
with f2:
    width = st.number_input("Finished fabric width (metres)", min_value=0.1, max_value=5.0, value=1.8, step=0.1,
                            help="Used to estimate fabric length from fabric weight.")

st.subheader("3. Production Calculation")
st.caption(
    "Simplified theoretical estimate: one course is assumed per machine revolution, "
    "and each feeder is assumed to form one course. The assumed stitch length is entered below."
)
st.warning(
    "Circular knitting output depends on stitch length and machine construction. "
    "This app includes stitch length as an input so the production estimate is more meaningful."
)
stitch_length = st.number_input(
    "Stitch length (mm)", min_value=1.0, max_value=10.0, value=2.8, step=0.1,
    help="Average yarn length consumed per stitch, in millimetres."
)
needles = st.number_input(
    "Number of needles", min_value=100, max_value=5000, value=1800, step=100,
    help="Total needles in the cylinder. Used in the simplified yarn-consumption estimate."
)

# Approximate yarn consumption:
# RPM * 60 * hours * feeders * needles * stitch length (mm) / 1,000,000 = kg yarn
# (mm to km: /1e6; km * tex /1000 would be needed for yarn mass)
# Since yarn linear density is not part of the assignment inputs, ask for yarn count in Tex.
yarn_tex = st.number_input(
    "Yarn linear density (Tex)", min_value=1.0, max_value=200.0, value=20.0, step=1.0,
    help="Enter yarn fineness in Tex. 1 Tex = 1 gram per 1000 metres."
)

# Total yarn length in metres:
# RPM * 60 * hours * feeders * needles * stitch length(mm) / 1000
total_yarn_m = rpm * 60 * hours * feeders * needles * stitch_length / 1000
theoretical_yarn_kg = total_yarn_m * yarn_tex / 1_000_000
actual_yarn_kg = theoretical_yarn_kg * efficiency / 100

# Fabric weight is approximated from yarn consumption. Fabric GSM and width help estimate length.
# kg = GSM(g/m2) * width(m) * length(m) / 1000
# Solve length = kg*1000/(GSM*width)
fabric_length_m = actual_yarn_kg * 1000 / (gsm * width)
fabric_area_m2 = fabric_length_m * width

st.divider()
st.subheader("4. Estimated Daily Production")
m1, m2, m3 = st.columns(3)
m1.metric("Daily Fabric Output", f"{actual_yarn_kg:.2f} kg")
m2.metric("Estimated Fabric Length", f"{fabric_length_m:.1f} m")
m3.metric("Fabric Area", f"{fabric_area_m2:.1f} m²")

r1, r2 = st.columns(2)
r1.metric("Theoretical Yarn Consumption", f"{theoretical_yarn_kg:.2f} kg")
r2.metric("Efficiency-adjusted Yarn", f"{actual_yarn_kg:.2f} kg")

st.info(
    "This is an educational estimate based on the entered stitch length, needle count and yarn Tex. "
    "For production planning, compare the result with actual machine records and measured fabric output."
)

fig, ax = plt.subplots(figsize=(7, 3))
ax.bar(["Theoretical output", "Efficiency-adjusted output"],
       [theoretical_yarn_kg, actual_yarn_kg])
ax.set_ylabel("Estimated output (kg/day)")
ax.set_title("Daily Production Estimate")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
st.pyplot(fig, use_container_width=True)

with st.expander("View calculation formulas"):
    st.markdown("**1. Total yarn length (metres)**")
    st.latex(r"L = RPM \\times 60 \\times Hours \\times Feeders \\times Needles \\times \\frac{Stitch\\ Length\\ (mm)}{1000}")
    st.markdown("**2. Theoretical yarn consumption (kg)**")
    st.latex(r"Yarn\\ (kg) = \\frac{L\\ (m) \\times Tex}{1,000,000}")
    st.markdown("**3. Efficiency-adjusted production (kg/day)**")
    st.latex(r"Production = Yarn\\ (kg) \\times \\frac{Efficiency}{100}")
    st.markdown("**4. Estimated fabric length (metres)**")
    st.latex(r"Length = \\frac{Production\\ (kg) \\times 1000}{GSM \\times Width\\ (m)}")
    st.caption(
        "This simplified educational model treats the entered stitch length and needle count as representative "
        "for the machine. Actual circular knitting calculations may require machine diameter, gauge, "
        "stitch length, yarn count, take-down conditions and measured machine constants."
    )

st.caption("Student Project · Roll No. 25TE037 · Textile Engineering")
