
# import streamlit as st
# from PIL import Image
# from prediction import predict_disease, class_names

# # Page configuration
# st.set_page_config(
#     page_title="Potato Leaf Disease Detection",
#     page_icon="🌿",
#     layout="centered"
# )

# # Application title
# st.title("🌿 Potato Leaf Disease Detection")

# st.write(
#     "Upload a potato leaf image "
#     "to detect its disease using CNN."
# )

# st.divider()

# # Image uploader
# uploaded_file = st.file_uploader(
#     "Upload Potato Leaf Image",
#     type=["jpg", "jpeg", "png"]
# )

# # Check if image is uploaded
# if uploaded_file is not None:

#     # Read uploaded image
#     image = Image.open(uploaded_file)

#     # Display uploaded image
#     st.image(
#         image,
#         caption="Uploaded Potato Leaf",
#         width=400
#     )

#     # Predict button
#     if st.button("Predict Disease"):

#         with st.spinner("Analyzing image..."):

#             # Call prediction function
#             predicted_class, confidence, predictions = (
#                 predict_disease(image)
#             )

#         # Display result
#         st.success("Prediction Completed!")

#         st.subheader("Prediction Result")

#         # Display disease name
#         st.write(
#             "Predicted Disease:",
#             predicted_class.replace("Potato___", "")
#         )

#         # Display confidence
#         st.metric(
#             "Model Confidence",
#             f"{confidence * 100:.2f}%"
#         )

#         st.divider()

#         # Display all class scores
#         st.subheader("All Disease Scores")

#         for name, score in zip(class_names, predictions):

#             disease_name = name.replace("Potato___", "")

#             st.write(
#                 f"{disease_name}: {score * 100:.2f}%"
#             )

#             st.progress(float(score))

# else:

#     st.info("Please upload a potato leaf image.")





import streamlit as st
from PIL import Image
from prediction import predict_disease, class_names

# ------------------------------------------------------------------
# Page configuration
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Potato Leaf Disease Detection",
    page_icon="🥔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# Disease information (shown in the result card)
# ------------------------------------------------------------------
DISEASE_INFO = {
    "healthy": {
        "label": "Healthy leaf",
        "color": "#2f7d4f",
        "bg": "#e6f4ea",
        "icon": "✅",
        "summary": "No signs of disease were found on this leaf.",
        "tips": [
            "Keep watering at the base of the plant, not over the leaves.",
            "Check plants every few days, especially after rain.",
            "Rotate crops each season to keep the soil healthy.",
        ],
    },
    "early_blight": {
        "label": "Early blight",
        "color": "#b7791f",
        "bg": "#fdf3dc",
        "icon": "⚠️",
        "summary": (
            "Caused by the fungus Alternaria solani. Look for brown spots "
            "with ring-like patterns, usually on older leaves first."
        ),
        "tips": [
            "Remove and destroy badly affected leaves.",
            "Spray a recommended fungicide such as mancozeb or chlorothalonil.",
            "Avoid overhead watering and keep plants well spaced.",
        ],
    },
    "late_blight": {
        "label": "Late blight",
        "color": "#b83a3a",
        "bg": "#fbe7e7",
        "icon": "🚨",
        "summary": (
            "Caused by Phytophthora infestans. It spreads fast in cool, "
            "wet weather and can destroy a crop within days."
        ),
        "tips": [
            "Act quickly: remove infected plants and keep them away from the field.",
            "Apply a suitable fungicide and contact your local agriculture officer.",
            "Do not store tubers from infected plants.",
        ],
    },
}

FALLBACK_INFO = {
    "label": "Unknown",
    "color": "#4a5568",
    "bg": "#edf2f7",
    "icon": "❔",
    "summary": "This result is not in the disease guide.",
    "tips": ["Try another photo with better light and a plain background."],
}


def clean_name(raw: str) -> str:
    """'Potato___Early_blight' -> 'early_blight'"""
    return raw.replace("Potato___", "").strip().lower()


def get_info(raw: str) -> dict:
    return DISEASE_INFO.get(clean_name(raw), FALLBACK_INFO)


# ------------------------------------------------------------------
# Custom styling
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap');

    :root {
        --leaf-900: #123524;
        --leaf-700: #1f5a3a;
        --leaf-500: #2f7d4f;
        --sage-100: #eef3ec;
        --soil: #6b4f3a;
        --ink: #1b2a22;
        --muted: #5c6b62;
        --line: #d9e2d6;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif;
        color: var(--ink);
    }
    .stApp { background: var(--sage-100); }

    /* force readable text colours (works even if browser/Streamlit is in dark mode) */
    .stApp, .stApp p, .stApp li, .stApp label, .stApp span,
    .stMarkdown, [data-testid="stMarkdownContainer"] * {
        color: var(--ink);
    }
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] span {
        color: var(--ink) !important;
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: var(--leaf-900) !important;
    }

    /* uploader text and button */
    [data-testid="stFileUploader"] section,
    [data-testid="stFileUploader"] section * {
        color: var(--muted) !important;
    }
    [data-testid="stFileUploader"] button {
        background: var(--leaf-700) !important;
        border: none !important;
        border-radius: 8px !important;
    }
    [data-testid="stFileUploader"] button,
    [data-testid="stFileUploader"] button * {
        color: #ffffff !important;
    }
    [data-testid="stFileUploaderFile"] * { color: var(--ink) !important; }

    /* tabs */
    .stTabs [data-baseweb="tab"] { color: var(--muted) !important; }
    .stTabs [aria-selected="true"] { color: var(--leaf-700) !important; font-weight: 600; }

    /* hero text must stay light on the dark green banner */
    .hero h1 { color: #ffffff !important; }
    .hero p { color: #cfe3d3 !important; }

    /* main button label stays white on green */
    .stButton > button, .stButton > button * { color: #ffffff !important; }

    /* disabled button */
    .stButton > button:disabled {
        background: #c9d6c8 !important;
        cursor: not-allowed;
    }
    .stButton > button:disabled, .stButton > button:disabled * {
        color: #6f7f74 !important;
    }

    /* hide default streamlit chrome */
    #MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
    .block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1150px; }

    /* hero */
    .hero {
        background: linear-gradient(135deg, var(--leaf-900) 0%, var(--leaf-700) 100%);
        border-radius: 20px;
        padding: 2.4rem 2.6rem;
        margin-bottom: 1.6rem;
        color: #f2f7f1;
    }
    .hero h1 {
        font-family: 'Fraunces', serif;
        font-weight: 700;
        font-size: 2.4rem;
        line-height: 1.15;
        margin: 0 0 .6rem 0;
        color: #ffffff;
    }
    .hero p { font-size: 1.05rem; margin: 0; max-width: 560px; color: #cfe3d3; }

    /* panels */
    .panel-title {
        font-family: 'Fraunces', serif;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: .6rem;
        color: var(--leaf-900);
    }
    .panel {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 1.4rem 1.5rem;
    }

    /* empty state */
    .empty {
        text-align: center;
        padding: 2.6rem 1rem;
        color: var(--muted);
    }
    .empty .big { font-size: 2.6rem; margin-bottom: .4rem; }

    /* result card */
    .result-card {
        border-radius: 14px;
        padding: 1.3rem 1.4rem;
        margin-bottom: 1rem;
        border-left: 6px solid;
    }
    .result-card .name {
        font-family: 'Fraunces', serif;
        font-size: 1.7rem;
        font-weight: 700;
        margin: 0;
    }
    .result-card .conf { font-size: .95rem; margin-top: .2rem; color: var(--muted); }
    .result-card .desc { margin-top: .7rem; font-size: .98rem; line-height: 1.55; }

    /* score bars */
    .score-row { margin-bottom: .9rem; }
    .score-head {
        display: flex; justify-content: space-between;
        font-size: .93rem; margin-bottom: .3rem;
    }
    .score-head .val { font-weight: 600; }
    .bar-bg { background: #e8eee6; border-radius: 99px; height: 10px; overflow: hidden; }
    .bar-fill { height: 100%; border-radius: 99px; }

    /* tips */
    .tips li { margin-bottom: .45rem; line-height: 1.5; }

    /* buttons */
    .stButton > button {
        background: var(--leaf-700);
        color: #fff;
        border: none;
        border-radius: 10px;
        padding: .7rem 1.2rem;
        font-weight: 600;
        width: 100%;
        transition: background .15s ease;
    }
    .stButton > button:hover { background: var(--leaf-900); color: #fff; }
    .stButton > button:focus-visible { outline: 3px solid #9cd0ae; outline-offset: 2px; }

    /* uploader */
    [data-testid="stFileUploader"] section {
        border: 2px dashed #b7c9b5;
        border-radius: 14px;
        background: #f8fbf7;
    }

    /* sidebar */
    [data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid var(--line); }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        font-family: 'Fraunces', serif; color: var(--leaf-900);
    }

    .footer {
        text-align: center; color: var(--muted);
        font-size: .88rem; margin-top: 2.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🥔 About this app")
    st.write(
        "This tool uses a CNN (deep learning model) to look at a potato "
        "leaf photo and tell whether it is healthy or has a disease."
    )

    st.markdown("### Diseases it can detect")
    for key, info in DISEASE_INFO.items():
        st.markdown(f"{info['icon']} **{info['label']}**")

    st.markdown("### For a better result")
    st.markdown(
        "- Photograph one leaf at a time\n"
        "- Use daylight, avoid shadows\n"
        "- Keep the leaf in the centre\n"
        "- Use a plain background if possible"
    )

# ------------------------------------------------------------------
# Hero
# ------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>Check your potato leaf in seconds</h1>
        <p>Upload a clear photo of a potato leaf. The model will tell you
        whether it is healthy or has early or late blight.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Main layout: left = upload, right = result
# ------------------------------------------------------------------
left, right = st.columns([1, 1.15], gap="large")

with left:
    st.markdown('<div class="panel-title">1. Upload a photo</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose a leaf image (JPG, JPEG or PNG)",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    image = None
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="Your leaf photo", use_container_width=True)
        except Exception:
            st.error("We couldn't open this file. Please upload a valid JPG or PNG image.")
            image = None

    predict_clicked = st.button(
        "Detect disease",
        disabled=image is None,
    )

with right:
    st.markdown('<div class="panel-title">2. See the result</div>', unsafe_allow_html=True)

    if image is None:
        st.markdown(
            """
            <div class="panel empty">
                <div class="big">🌿</div>
                <div><b>No photo yet</b></div>
                <div>Upload a leaf image on the left to begin.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif not predict_clicked and "result" not in st.session_state:
        st.markdown(
            """
            <div class="panel empty">
                <div class="big">🔍</div>
                <div><b>Photo ready</b></div>
                <div>Select <b>Detect disease</b> to analyse the leaf.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Run prediction and store it so the result stays on screen
    if predict_clicked and image is not None:
        with st.spinner("Analysing the leaf..."):
            predicted_class, confidence, predictions = predict_disease(image)
        st.session_state["result"] = {
            "file": uploaded_file.name,
            "predicted_class": predicted_class,
            "confidence": float(confidence),
            "predictions": [float(p) for p in predictions],
        }

    result = st.session_state.get("result")

    # Only show a result that belongs to the currently uploaded file
    if image is not None and result and result["file"] == uploaded_file.name:
        info = get_info(result["predicted_class"])

        # Main result card
        st.markdown(
            f"""
            <div class="result-card" style="background:{info['bg']}; border-color:{info['color']};">
                <p class="name" style="color:{info['color']};">{info['icon']} {info['label']}</p>
                <div class="conf">Model confidence: <b>{result['confidence'] * 100:.2f}%</b></div>
                <div class="desc">{info['summary']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if result["confidence"] < 0.6:
            st.warning(
                "The model is not very sure about this photo. "
                "Try another image with better light and a clearer leaf."
            )

        # Tabs for scores and advice
        tab_scores, tab_advice = st.tabs(["All scores", "What to do next"])

        with tab_scores:
            rows = ""
            for name, score in zip(class_names, result["predictions"]):
                item = get_info(name)
                pct = score * 100
                rows += (
                    '<div class="score-row">'
                    '<div class="score-head">'
                    f'<span>{item["label"]}</span>'
                    f'<span class="val">{pct:.2f}%</span>'
                    '</div>'
                    '<div class="bar-bg">'
                    f'<div class="bar-fill" style="width:{pct:.2f}%; background:{item["color"]};"></div>'
                    '</div>'
                    '</div>'
                )
            st.markdown(f'<div class="panel">{rows}</div>', unsafe_allow_html=True)

        with tab_advice:
            tips = "".join(f"<li>{t}</li>" for t in info["tips"])
            st.markdown(
                f'<div class="panel"><ul class="tips">{tips}</ul>'
                '<div style="color:#5c6b62; font-size:.88rem; margin-top:.6rem;">'
                "This is an AI estimate. For serious cases, check with a local "
                "agriculture expert.</div></div>",
                unsafe_allow_html=True,
            )

# ------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------
st.markdown(
    '<div class="footer">Potato Leaf Disease Detection · Built with Streamlit and TensorFlow</div>',
    unsafe_allow_html=True,
)