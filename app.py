import streamlit as st
from pathlib import Path
from src.matcher import load_universities, recommend

st.set_page_config(page_title="GermanPath AI", page_icon="🎓", layout="wide")

st.title("🎓 GermanPath AI")
st.caption("Find German Master's programmes that fit your academic profile.")

st.info(
    "Enter your details and click **Save profile & find programmes**. "
    "No recommendations or requirement comparisons are shown before you submit. "
    "Results are profile matches, not admission guarantees."
)

DATA_PATH = Path(__file__).parent / "data" / "universities.csv"
try:
    df = load_universities(DATA_PATH)
except Exception as exc:
    st.error(f"Could not load the university dataset: {exc}")
    st.stop()

# Keep the submitted profile and results separate from the editable form.
if "submitted_profile" not in st.session_state:
    st.session_state.submitted_profile = None
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

COURSES = [
    "Computer Science", "Data Science", "Artificial Intelligence",
    "Machine Learning", "Software Engineering", "Cyber Security",
    "Information Systems", "Robotics", "Human-Computer Interaction",
    "Computer Engineering"
]

with st.sidebar:
    st.header("👨‍🎓 Student profile")
    with st.form("profile_form", clear_on_submit=False):
        st.subheader("Academic details")
        cgpa_text = st.text_input(
            "Bachelor's CGPA (German scale, optional)",
            placeholder="e.g. 2.3"
        )
        degree = st.text_input(
            "Bachelor's degree / background",
            placeholder="e.g. B.Tech Computer Science"
        )
        interests = st.multiselect(
            "Areas of interest",
            COURSES,
            default=[]
        )

        st.divider()
        st.subheader("Language tests")
        ielts = st.selectbox(
            "IELTS Academic",
            ["Not entered", "5.5", "6.0", "6.5", "7.0", "7.5", "8.0"],
            index=0
        )
        toefl = st.selectbox(
            "TOEFL iBT",
            ["Not entered", "72", "80", "85", "88", "90", "95", "100", "105", "110"],
            index=0
        )
        german = st.selectbox(
            "German language level",
            ["Not entered", "None", "A1", "A2", "B1", "B2", "C1", "C2"],
            index=0
        )

        st.divider()
        st.subheader("Additional details")
        gre = st.selectbox("GRE", ["Not entered", "Taken", "Not taken"], index=0)
        experience = st.selectbox(
            "Work experience",
            ["Not entered", "Fresher", "Less than 1 year", "1–2 years", "3+ years"],
            index=0
        )
        intake = st.selectbox(
            "Target intake",
            ["Not entered", "Winter semester", "Summer semester"],
            index=0
        )

        save = st.form_submit_button(
            "💾 Save profile & find programmes",
            type="primary",
            use_container_width=True
        )

    reset = st.button("↻ Clear profile and results", use_container_width=True)

    if save:
        profile = {
            "cgpa": cgpa_text.strip(),
            "degree": degree.strip(),
            "interests": interests,
            "ielts": ielts,
            "toefl": toefl,
            "german": german,
            "gre": gre,
            "experience": experience,
            "intake": intake,
        }

        # Validate CGPA only if the student entered it.
        if profile["cgpa"]:
            try:
                value = float(profile["cgpa"])
                if not 1.0 <= value <= 4.0:
                    raise ValueError
            except ValueError:
                st.error("Enter German CGPA between 1.0 and 4.0, or leave it blank.")
                st.stop()

        has_input = any([
            profile["cgpa"],
            profile["degree"],
            profile["interests"],
            profile["ielts"] != "Not entered",
            profile["toefl"] != "Not entered",
            profile["german"] != "Not entered",
            profile["gre"] != "Not entered",
            profile["experience"] != "Not entered",
            profile["intake"] != "Not entered",
        ])

        if not has_input:
            st.warning("Please enter at least one profile detail before requesting recommendations.")
        else:
            with st.spinner("Matching your profile against the university dataset..."):
                try:
                    cgpa_value = float(profile["cgpa"]) if profile["cgpa"] else None
                    results = recommend(
                        df=df,
                        cgpa=cgpa_value,
                        interests=profile["interests"],
                        ielts=profile["ielts"],
                        toefl=profile["toefl"],
                        german=profile["german"],
                        gre=profile["gre"],
                        degree=profile["degree"],
                    )
                    st.session_state.submitted_profile = profile
                    st.session_state.recommendations = results
                    st.success("Profile saved. Your recommendations have been updated.")
                except Exception as exc:
                    st.error(f"Could not generate recommendations: {exc}")

    if reset:
        st.session_state.submitted_profile = None
        st.session_state.recommendations = None
        st.rerun()

# Main page: deliberately blank until the student submits a profile.
if st.session_state.submitted_profile is None:
    st.header("Your personalised shortlist")
    st.write("Your university suggestions will appear here after you save your profile.")
    st.empty()
    st.stop()

profile = st.session_state.submitted_profile
results = st.session_state.recommendations

st.success("Showing recommendations based on your last saved profile.")
with st.expander("View saved student profile"):
    st.write(profile)

st.header("🎯 Recommended Master's programmes")
if results is None or results.empty:
    st.warning("No suitable programme records were found. Try adding or changing your course interests.")
    st.stop()

st.caption(f"{len(results)} programme records ranked against the submitted profile.")

for _, row in results.iterrows():
    with st.container(border=True):
        left, right = st.columns([4, 1])
        left.markdown(f"### {row.get('Course name', 'Course not specified')}")
        left.markdown(f"**{row.get('University name', 'University not specified')}**")
        right.metric("Profile fit", f"{int(row.get('match_score', 0))}/100")

        st.write(row.get("match_summary", ""))

        st.markdown("**Requirement comparison**")
        requirement_rows = [
            ("CGPA", row.get("CGPA_status", "Not assessed"), row.get("CGPA", "")),
            ("IELTS", row.get("IELTS_status", "Not assessed"), row.get("IELTS", "")),
            ("TOEFL", row.get("TOEFL_status", "Not assessed"), row.get("TOFEL", "")),
            ("German", row.get("GERMAN_status", "Not assessed"), row.get("GERMAN", "")),
            ("GRE", row.get("GRE_status", "Not assessed"), row.get("GRE", "")),
        ]
        st.table([
            {"Requirement": name, "Dataset requirement": str(raw) or "Not specified", "Your status": status}
            for name, status, raw in requirement_rows
        ])

        special = str(row.get("Special Requirements", "")).strip()
        if special and special.lower() not in {"nan", "none", "n", "-"}:
            st.write("**Additional / special requirements:**", special)

        route = str(row.get("Application Link", "")).strip()
        st.write("**Application route recorded:**", route or "Not listed")
        if route.startswith(("https://", "http://")):
            st.link_button("Open application portal", route)
        elif "uniassist" in route.lower():
            st.link_button("Open Uni-Assist", "https://www.uni-assist.de/")

        st.write("**Deadline recorded in spreadsheet:**", str(row.get("End Date", "Not listed")))
        st.caption("Verify current deadlines, requirements and application routes on the official programme website.")

st.divider()
st.subheader("Explore the dataset")
query = st.text_input("Search all university and course records")
filtered = df
if query:
    mask = df.astype(str).apply(
        lambda col: col.str.contains(query, case=False, na=False)
    ).any(axis=1)
    filtered = df[mask]
st.dataframe(filtered, use_container_width=True, hide_index=True)
