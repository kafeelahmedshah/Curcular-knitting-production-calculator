# Circular Knitting Production Calculator

**Roll Number:** 25TE037  
**Assigned Topic:** Circular Knitting Production Calculator  
**Department:** Textile Engineering  
**Framework:** Streamlit

## Project overview
This Streamlit web application estimates daily knitted fabric output using circular knitting machine and fabric parameters.

## Features
- Machine RPM input
- Number of feeders input
- Machine efficiency slider
- Daily working hours
- Fabric GSM and finished width
- Stitch length, number of needles and yarn Tex inputs
- Estimated daily yarn/fabric output in kg
- Estimated fabric length and area
- Production chart
- Expandable calculation formulas

## Calculation model
This app uses a simplified educational estimate.

1. Total yarn length:

   `L (m) = RPM × 60 × Hours × Feeders × Needles × Stitch Length (mm) / 1000`

2. Theoretical yarn consumption:

   `Yarn (kg) = L (m) × Tex / 1,000,000`

3. Efficiency-adjusted output:

   `Production (kg/day) = Yarn (kg) × Efficiency / 100`

4. Estimated fabric length:

   `Length (m) = Production (kg) × 1000 / (GSM × Width (m))`

## Project files
- `app.py` — main Streamlit application
- `requirements.txt` — Python dependencies
- `README.md` — project documentation

## Run locally
1. Install Python 3.9 or newer.
2. Open a terminal in this project folder.
3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   streamlit run app.py
   ```

5. Open the local address shown in the terminal, usually `http://localhost:8501`.

## Deploy on Streamlit Community Cloud
1. Create a GitHub repository.
2. Upload `app.py`, `requirements.txt` and `README.md`.
3. Sign in to Streamlit Community Cloud using GitHub.
4. Select the repository and choose `app.py` as the main file.
5. Deploy.

## Important technical note
This is a simplified student-project estimator, not a guaranteed factory production formula. Real circular knitting production depends on machine diameter, gauge, stitch length, yarn linear density, number of feeders, RPM, machine efficiency, downtime, fabric construction and machine-specific production constants. Validate estimates against actual machine data.
