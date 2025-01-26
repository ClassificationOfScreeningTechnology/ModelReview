import streamlit as st
import requests
import pandas as pd
import numpy as np
from PIL import Image

st.set_page_config(page_title="Klasyfikacja Animacji", layout="wide")

st.title("Klasyfikacja Animacji")
st.write("Prześlij jedno lub kilka zdjęć, a model zwróci prawdopodobieństwo przynależności do jednej z 4 kategorii:")

st.markdown(
    """
    - **Animacja 2D**
    - **Animacja 3D**
    - **Stop Motion**
    - **Live Action**
    """
)

st.subheader("1️⃣ Prześlij zdjęcia")
uploaded_files = st.file_uploader("Wybierz jedno lub więcej zdjęć...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Adresy endpointów API
single_image_url = "http://localhost:8000/process-image/"
multiple_images_url = "http://localhost:8000/process-images/"

def query_single_image(image_file):
    files = {"file": image_file}
    response = requests.post(single_image_url, files=files)
    return response.json()

def query_multiple_images(image_files):
    files = [("files", file) for file in image_files]
    response = requests.post(multiple_images_url, files=files)
    return response.json()


def convert_to_percentages(scores):
    exp_scores = np.exp(list(scores.values()))
    probabilities = exp_scores / np.sum(exp_scores)
    percentages = {key: f"{round(prob * 100, 2)}%" for key, prob in zip(scores.keys(), probabilities)}
    return percentages

def highlight_max_in_row(row):
    is_max = row == row.max()
    return ["background-color: darkgreen" if v else "" for v in is_max]

if uploaded_files:
    st.subheader("2️⃣ Wyniki klasyfikacji")
    results = []

    with st.spinner("Klasyfikuję przesłane zdjęcia..."):
        try:
            if len(uploaded_files) == 1:
                api_response = query_single_image(uploaded_files[0])
                percentages = convert_to_percentages(api_response)
                results.append({"Nazwa pliku": uploaded_files[0].name, **percentages})
            else:
                api_response = query_multiple_images(uploaded_files)
                for i, prediction in enumerate(api_response.get("predictions", [])):
                    percentages = convert_to_percentages(prediction)
                    results.append({"Nazwa pliku": uploaded_files[i].name, **percentages})
        except Exception as e:
            st.error(f"Błąd połączenia z API: {str(e)}")
            results = [{"Nazwa pliku": file.name, "Błąd": "Nie udało się pobrać danych z API"} for file in uploaded_files]

    if results:
        st.write("### Wyniki (w procentach):")
        df = pd.DataFrame(results)

        styled_df = df.style.apply(highlight_max_in_row, axis=1, subset=df.columns[1:])
        st.dataframe(styled_df, use_container_width=True)

    st.write("### Zdjęcia:")
    num_columns = 4
    images_per_row = []

    for i in range(0, len(uploaded_files), num_columns):
        images_per_row.append(uploaded_files[i:i + num_columns])

    for row in images_per_row:
        cols = st.columns(num_columns)
        for idx, uploaded_file in enumerate(row):
            with cols[idx]:
                image = Image.open(uploaded_file)
                st.image(image, caption=f"{uploaded_file.name}", use_container_width=False)
