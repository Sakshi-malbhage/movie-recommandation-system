import streamlit as st
import pandas as pd
import pickle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.stApp{
    background-color:white;
}

h1,h2,h3,h4,h5,h6,p,label{
    color:black !important;
}

div[data-baseweb="select"] > div{
    background-color:white !important;
    color:black !important;
}

.stButton>button{
    background-color:#1976D2;
    color:white;
    border-radius:10px;
    height:50px;
    width:100%;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover{
    background-color:#1565C0;
    color:white;
}

[data-testid="stMetricValue"]{
    color:black;
}

[data-testid="stMetricLabel"]{
    color:black;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.title("🎬 Movie Recommendation System")
st.write("Discover movies similar to your favorite movie.")

st.divider()

# ---------------- LOAD FILES ----------------

try:
    df = pd.read_csv("cleaned_data.csv")
except Exception:
    st.error("❌ cleaned_data.csv not found.")
    st.stop()

try:
    with open("similarity.pkl", "rb") as file:
        similarities = pickle.load(file)
except Exception:
    st.error("❌ similarity.pkl not found.")
    st.stop()

# ---------------- MOVIE LIST ----------------

movies = df["title"].tolist()

# ---------------- METRICS ----------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Movies", len(df))

with col2:
    st.metric("Algorithm", "TF-IDF")

with col3:
    st.metric("Similarity", "Cosine")

st.write("")

# ---------------- SELECT MOVIE ----------------

name = st.selectbox(
    "🍿 Select a Movie",
    movies,
    key="movie_select"
)

# ---------------- FUNCTIONS ----------------

def get_name_by_index(i):
    if 0 <= i < len(df):
        return df.iloc[i]["title"]
    return ""

def get_index_from_name(name):

    clean_name = (
        name.lower()
        .replace(" ", "")
        .replace("-", "")
    )

    titles = (
        df["title"]
        .str.lower()
        .str.replace(" ", "", regex=False)
        .str.replace("-", "", regex=False)
    )

    match = df[titles == clean_name]

    if not match.empty:
        return match.index[0]

    return -1

# ---------------- BUTTON ----------------

if st.button("🎬 Recommend Movies"):

    with st.spinner("Finding similar movies..."):

        index = get_index_from_name(name)

        if index == -1:
            st.error("Movie not found!")

        else:

            similarity_scores = list(enumerate(similarities[index]))

            similarity_scores = sorted(
                similarity_scores,
                key=lambda x: x[1],
                reverse=True
            )

            st.success(f"Top recommendations for: {name}")

            st.write("")

            for i in range(1, min(6, len(similarity_scores))):

                movie = get_name_by_index(
                    similarity_scores[i][0]
                )

                st.info(f"🎬 {i}. {movie}")

# ---------------- FOOTER ----------------

st.divider()

st.markdown(
    """
    <center>
    <h4 style="color:black;">
    ❤️ Developed by Sakshi
    </h4>

    <p style="color:black;">
    Python | Streamlit | NLP
    </p>
    </center>
    """,
    unsafe_allow_html=True
)