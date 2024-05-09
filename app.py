import streamlit as st

def load_css():
    css = """
    <style>
        body {
            background-color: #f4f4f9;
            font-family: 'Arial';
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .stTextInput>label, .stDateInput>label, .stNumberInput>label, .stSelectbox>label {
            color: #333;
        }
        .stTextInput>div>div>input, .stNumberInput>div>div>input {
            border-radius: 10px;
            border: 1px solid #ccc;
        }
        .stButton>button {
            width: 100%;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            background-color: #0068c9;
            border-radius: 5px;
            margin-top: 10px;
        }
        .stMarkdown {
            background-color: #fff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def main():
    load_css()  # Stildefinitionen laden
    st.title('Meine verbesserte Streamlit-Seite')

    st.markdown("""
        <div style='background-color: #e8eaf6; padding: 10px; border-radius: 5px;'>
            <h2>Willkommen auf meiner Seite!</h2>
            <p>Füllen Sie das Formular unten aus, um Informationen zu erhalten.</p>
        </div>
    """, unsafe_allow_html=True)

    name = st.text_input("Name:")
    alter = st.number_input("Alter:", min_value=0, max_value=100, step=1)
    geburtsdatum = st.date_input("Geburtsdatum:")

    optionen = ["Option 1", "Option 2", "Option 3"]
    auswahl = st.selectbox("Wähle eine Option:", optionen)

    if st.button('Submit'):
        st.success(f"Hallo {name}, du hast {auswahl} gewählt.")

if __name__ == "__main__":
    main()
