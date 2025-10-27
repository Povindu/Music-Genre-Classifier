import streamlit as st
from pyswip import Prolog
import json


try:
    prolog = Prolog()
    prolog.consult("music_kb.pl")
except Exception as e:
    st.error("Error initializing Prolog or loading 'music_classifier_kb.pl'.")
    st.error(f"Details: {e}")
    st.error("Please ensure SWI-Prolog is installed and the .pl file is in the same directory.")
    st.stop()



st.set_page_config(page_title="Music Genre Classifier", layout="wide")
st.title("Music Genre Prediction Expert System")
st.write("Describe a song using the options below to get a genre classification from our expert system.")

attributes = {}


INSTRUMENT_LIST = [
    'acoustic_guitar', 'bass', 'bongos', 'cajon', 'cello', 'double_bass', 'drums',
    'drum_machine', 'electric_guitar', 'flute', 'harmonica', 'organ', 'piano',
    'sampler', 'saxophone', 'serpina', 'sitar', 'strings', 'synthesizer',
    'tabla', 'trombone', 'trumpet', 'violin', 'viola'
]
VOCAL_LIST = [
    'clean', 'classical_melodic', 'energetic', 'falsetto', 'instrumental',
    'melodic', 'narrative', 'raspy', 'robotic_vocal', 'soulful', 'upbeat'
]


col1, col2 = st.columns(2)

with col1:
    st.subheader("Song Characteristics")
    
    # Q1: Year of Release
    attributes['year'] = st.slider(
        "Year of Release:",
        min_value=1700, max_value=2025, value=1985, step=5
    )
    
    # Q2: Tempo (BPM)
    bpm_map = {
        "Very Slow (Under 75 BPM)": 70,
        "Slow (75-100 BPM)": 85,
        "Mid-Tempo (100-125 BPM)": 110,
        "Fast (125-150 BPM)": 135,
        "Very Fast (Over 150 BPM)": 160
    }
    bpm_choice = st.select_slider("Select the song's tempo:", options=list(bpm_map.keys()))
    attributes['bpm'] = bpm_map[bpm_choice]

with col2:
    st.subheader("Instrumentation & Vocals")
    

    vocal_choice = st.selectbox("Select the vocal style:", ["Skip / Not Sure"] + sorted(VOCAL_LIST))
    if vocal_choice != "Skip / Not Sure":
        attributes['vocals'] = vocal_choice


    selected_instruments = st.multiselect(
        "Select the primary instruments in the song:",
        options=sorted(INSTRUMENT_LIST)
    )
    if selected_instruments:
        # Format for Prolog list: e.g., ['piano', 'violin']
        formatted_instruments = ",".join([f"'{inst}'" for inst in selected_instruments])
        attributes['instruments'] = f"[{formatted_instruments}]"

if st.button("Classify Music", type="primary", use_container_width=True):
    
    # Filter out any unselected attributes
    final_attributes = {k: v for k, v in attributes.items() if v is not None}
    
    with st.expander("See all collected attributes (facts sent to Prolog)"):
        st.json(final_attributes)
        

    try:

        prolog.retractall("song_attribute(_,_)")

        for key, value in final_attributes.items():
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
            
            st.header(f"🏆 Best Match: {recommendations[0]['genre']}")
            
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

            # Display all matched recommendations in tabs
            tab_titles = [f"Rank #{i+1} ({rec['genre']})" for i, rec in enumerate(recommendations)]
            tabs = st.tabs(tab_titles)
            
            for i, (tab, rec) in enumerate(zip(tabs, recommendations)):
                with tab:
                    st.subheader(f"Genre: {rec.get('genre')}")
                    st.metric("Confidence Score", f"{rec.get('confidence', 0) * 100:.1f}%")
                    st.info(f"💡 **Reason:** {rec.get('reason', 'N/A')}")

    except Exception as e:
        st.error(f"An error occurred during the Prolog query: {e}")
        prolog.retractall("song_attribute(_,_)")