import streamlit as st
from pyswip import Prolog
import json


try:
    prolog = Prolog()
    prolog.consult("music_kb.pl")
except Exception as e:
    st.error(f"Error initializing Prolog or loading 'music_kb.pl'. Details: {e}")
    st.error("Please ensure SWI-Prolog is installed, in your system's PATH, and the .pl file is in the same directory.")
    st.stop()


st.set_page_config(page_title="Music Genre Classifier", page_icon="🎵", layout="wide")
st.title("Music Genre Expert System")
st.write("Describe a song using the options below, or select one of our examples to see how it works.")



INSTRUMENT_LIST = sorted([
    'acoustic_guitar', 'bass', 'bongos', 'cajon', 'cello', 'double_bass', 'drums',
    'drum_machine', 'electric_guitar', 'flute', 'harmonica', 'organ', 'piano',
    'sampler', 'saxophone', 'serpina', 'sitar', 'strings', 'synthesizer',
    'tabla', 'trombone', 'trumpet', 'violin', 'viola'
])
VOCAL_LIST = sorted([
    'clean', 'classical_melodic', 'energetic', 'falsetto', 'instrumental',
    'melodic', 'narrative', 'raspy', 'robotic_vocal', 'soulful', 'upbeat'
])
BPM_OPTIONS = {
    "Very Slow (Under 75 BPM)": 70,
    "Slow (75-100 BPM)": 85,
    "Mid-Tempo (100-125 BPM)": 110,
    "Fast (125-150 BPM)": 135,
    "Very Fast (Over 150 BPM)": 160
}

BPM_REVERSE_MAP = {v: k for k, v in BPM_OPTIONS.items()}


PRESETS = [
    {
        "title": "Classic Calypso Pop",
        "description": "Triggers the 'Calypso Pop' rule with a high BPM, upbeat vocals, and bongos from the 60s.",
        "attributes": {
            "year": 1969,
            "bpm": 140,
            "vocals": "upbeat",
            "instruments": ["acoustic_guitar", "bongos", "bass"]
        }
    },
    {
        "title": "Sri Lankan Classical",
        "description": "Matches 'Sri Lankan Classical Folk' with a slow tempo and traditional instruments like the Sitar.",
        "attributes": {
            "year": 1970,
            "bpm": 65,
            "vocals": "classical_melodic",
            "instruments": ["sitar", "tabla", "serpina", "violin"]
        }
    },
    {
        "title": "'80s Synth Pop-Rock",
        "description": "An example for '80s Pop Rock', featuring the iconic synthesizer and electric guitar combination.",
        "attributes": {
            "year": 1989,
            "bpm": 115,
            "vocals": "clean",
            "instruments": ["synthesizer", "electric_guitar", "bass", "drums"]
        }
    },
    {
        "title": "Modern Folk Fusion",
        "description": "A recent song blending Eastern (Flute, Tabla) and Western (Guitar, Piano) instruments.",
        "attributes": {
            "year": 2018,
            "bpm": 100,
            "vocals": "melodic",
            "instruments": ["acoustic_guitar", "flute", "tabla", "piano"]
        }
    }
]


if 'year' not in st.session_state:
    st.session_state.year = 1985
if 'bpm_choice' not in st.session_state:
    st.session_state.bpm_choice = "Mid-Tempo (100-125 BPM)"
if 'vocal_choice' not in st.session_state:
    st.session_state.vocal_choice = "Skip / Not Sure"
if 'instruments' not in st.session_state:
    st.session_state.instruments = []

st.divider()
st.subheader("Try These Examples")

cols = st.columns(len(PRESETS))

def set_preset(preset_attributes):
    """A function to update the session state with preset values."""
    st.session_state.year = preset_attributes["year"]
    bpm_value = preset_attributes["bpm"]
    closest_bpm_key = min(BPM_OPTIONS.keys(), key=lambda k: abs(BPM_OPTIONS[k] - bpm_value))
    st.session_state.bpm_choice = closest_bpm_key
    st.session_state.vocal_choice = preset_attributes["vocals"]
    st.session_state.instruments = preset_attributes["instruments"]

for i, preset in enumerate(PRESETS):
    with cols[i]:
        if st.button(preset["title"], help=preset["description"], use_container_width=True):
            set_preset(preset["attributes"])

st.divider()


attributes = {}

col1, col2 = st.columns(2)

with col1:
    st.subheader("Song Characteristics")

    attributes['year'] = st.slider(
        "Year of Release:",
        min_value=1950, max_value=2025, step=1,
        key='year'
    )
    

    bpm_choice = st.select_slider(
        "Select the song's tempo:",
        options=list(BPM_OPTIONS.keys()),
        key='bpm_choice'
    )
    attributes['bpm'] = BPM_OPTIONS[bpm_choice]

with col2:
    st.subheader("Instrumentation & Vocals")
    
    vocal_choice = st.selectbox(
        "Select the vocal style:",
        ["Skip / Not Sure"] + VOCAL_LIST,
        key='vocal_choice'
    )
    if vocal_choice != "Skip / Not Sure":
        attributes['vocals'] = vocal_choice


    selected_instruments = st.multiselect(
        "Select the primary instruments in the song:",
        options=INSTRUMENT_LIST,
        key='instruments'
    )
    if selected_instruments:
        formatted_instruments = ",".join([f"'{inst}'" for inst in selected_instruments])
        attributes['instruments'] = f"[{formatted_instruments}]"



if st.button("Classify Music", type="primary", use_container_width=True):
    
    final_attributes = {k: v for k, v in attributes.items() if v is not None}
    
    with st.expander("See all collected attributes (facts sent to Prolog)"):
        st.json(final_attributes)
        
    try:

        prolog.retractall("song_attribute(_,_)")
        

        for key, value in final_attributes.items():
            fact_string = ""
            if key == 'instruments':
                fact_string = f"song_attribute({key}, {value})"
            elif isinstance(value, (int, float)):
                fact_string = f"song_attribute({key}, {value})"
            else:
                fact_string = f"song_attribute({key}, '{value}')"
            prolog.assertz(fact_string)


        query_string = "all_recommendations(Matches)"
        raw_results = list(prolog.query(query_string))


        prolog.retractall("song_attribute(_,_)")
        

        recommendations = []
        if raw_results and 'Matches' in raw_results[0]:
            for r in raw_results[0]['Matches']:
                recommendations.append({
                    'genre': r[0],
                    'confidence': r[1],
                    'reason': r[2]
                })
        
        st.divider()

        if not recommendations:
            st.warning("No specific genre matched your unique criteria. Try adjusting the attributes.")
        else:
            recommendations.sort(key=lambda x: x.get('confidence', 0), reverse=True)
            
            st.header(f"Best Match: {recommendations[0]['genre']}")
            
            output_data = {
                'attributes': final_attributes,
                'best_match': recommendations[0],
                'all_recommendations': recommendations
            }
            st.download_button(
                label="Download Full Report (JSON)",
                data=json.dumps(output_data, indent=2),
                file_name="genre_classification_report.json",
                mime="application/json"
            )

            tab_titles = [f"Rank #{i+1} ({rec['genre']})" for i, rec in enumerate(recommendations)]
            tabs = st.tabs(tab_titles)
            
            for i, (tab, rec) in enumerate(zip(tabs, recommendations)):
                with tab:
                    st.subheader(f"Genre: {rec.get('genre')}")
                    st.metric("Confidence Score", f"{rec.get('confidence', 0) * 100:.1f}%")
                    st.info(f"**Reason:** {rec.get('reason', 'N/A')}")

    except Exception as e:
        st.error(f"An error occurred during the Prolog query: {e}")
        prolog.retractall("song_attribute(_,_)")