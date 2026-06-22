import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Student Performance Prediction",
    page_icon="🎓",
    layout="wide"
)

# =====================================
# LOAD MODEL
# =====================================

model = joblib.load("student_model.pkl")

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("📚 Student Achievement Dashboard")

page = st.sidebar.radio(
    "Choose One Page",
    [
        "Prediction",
        "Dataset Information",
        "Analytics Dashboard"
    ]
)

# =====================================
# HEADER
# =====================================

st.markdown("""
<h1 style='text-align:center;color:#1E88E5'>
🎓 Student Performance Prediction System
</h1>
""", unsafe_allow_html=True)

# =====================================
# PREDICTION PAGE
# =====================================

if page == "Prediction":

    st.subheader("Enter Student Information")

    col1, col2 = st.columns(2)

    with col1:

        study_hours = st.number_input(
            "Study Hours Per Week",
            min_value=0.0,
            max_value=100.0,
            value=10.0
        )

        attendance = st.number_input(
            "Attendance Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=75.0
        )

        previous_grades = st.number_input(
            "Previous Grades",
            min_value=0.0,
            max_value=100.0,
            value=70.0
        )

    with col2:

        extracurricular = st.selectbox(
            "Extracurricular Activities",
            ["Yes", "No"]
        )

        parent_education = st.selectbox(
            "Parent Education Level",
            [
                "High School",
                "Associate",
                "Bachelor",
                "Master",
                "Doctorate"
            ]
        )

    if st.button("🚀 Predict Result"):

        input_df = pd.DataFrame({

            "Study Hours per Week": [study_hours],

            "Attendance Rate": [attendance],

            "Previous Grades": [previous_grades],

            "Participation in Extracurricular Activities":
            [extracurricular],

            "Parent Education Level":
            [parent_education]

        })

        prediction = model.predict(input_df)

        result = prediction[0]

        if str(result).lower() in ["yes", "pass", "passed", "1"]:

            st.success("🎉 Student Will PASS")

        elif str(result).lower() in ["no", "fail", "failed", "0"]:

            st.error(" Student Will FAIL")

        else:

            st.info(f"Prediction: {result}")

# =====================================
# DATASET PAGE
# =====================================

elif page == "Dataset Information":

    st.subheader("Dataset Overview")

    df = pd.read_csv("student_performance_prediction.csv")

    st.write("Dataset Shape")

    st.write(df.shape)

    st.write("First 10 Rows")

    st.dataframe(df.head(10))

    st.write("Column Names")

    st.write(df.columns.tolist())

    st.write("Summary Statistics")

    st.dataframe(df.describe())

# =====================================
# ANALYTICS DASHBOARD
# =====================================

elif page == "Analytics Dashboard":

    st.markdown("""
    <style>

    [data-testid="stPlotlyChart"]{
        border:3px solid #3F51B5;
        border-radius:15px;
        padding:10px;
        background:white;
        box-shadow:0px 4px 15px rgba(0,0,0,0.20);
        margin-bottom:20px;
    }

    </style>
    """, unsafe_allow_html=True)

    def style_chart(fig):

        fig.update_layout(

            paper_bgcolor="white",
            plot_bgcolor="white",

            font=dict(
                size=14,
                color="black"
            ),

            title_font_size=22,

            xaxis=dict(
                showgrid=True,
                gridcolor="lightgray",
                showline=True,
                linewidth=2,
                linecolor="black",
                mirror=True
            ),

            yaxis=dict(
                showgrid=True,
                gridcolor="lightgray",
                showline=True,
                linewidth=2,
                linecolor="black",
                mirror=True
            )
        )

        return fig

    st.header("📊 Student Performance Analytics Dashboard")

    df = pd.read_csv("student_performance_prediction.csv")

    # =====================================
    # KPI CARDS
    # =====================================

    total_students = len(df)

    passed = len(df[df["Passed"] == "Yes"])

    failed = len(df[df["Passed"] == "No"])

    pass_rate = (passed / total_students) * 100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👨‍🎓 Total Students", total_students)

    col2.metric("✅ Passed", passed)

    col3.metric("❌ Failed", failed)

    col4.metric("📈 Pass Rate", f"{pass_rate:.2f}%")

    st.divider()

    # =====================================
    # PIE CHART
    # =====================================

    fig1 = px.pie(
        df,
        names="Passed",
        title="Pass vs Fail Ratio",
        color="Passed",
        color_discrete_map={
            "Yes": "#00C853",
            "No": "#D50000"
        }
    )

    st.plotly_chart(
        style_chart(fig1),
        use_container_width=True
    )

    # =====================================
    # ATTENDANCE
    # =====================================

    fig2 = px.histogram(
        df,
        x="Attendance Rate",
        nbins=20,
        title="Attendance Distribution",
        color_discrete_sequence=["#2962FF"]
    )

    fig2.update_traces(
        marker_line_color="black",
        marker_line_width=1.5
    )

    st.plotly_chart(
        style_chart(fig2),
        use_container_width=True
    )

    # =====================================
    # STUDY HOURS
    # =====================================

    fig3 = px.histogram(
        df,
        x="Study Hours per Week",
        nbins=20,
        title="Study Hours Distribution",
        color_discrete_sequence=["#AA00FF"]
    )

    fig3.update_traces(
        marker_line_color="black",
        marker_line_width=1.5
    )

    st.plotly_chart(
        style_chart(fig3),
        use_container_width=True
    )

    # =====================================
    # PREVIOUS GRADES
    # =====================================

    fig4 = px.histogram(
        df,
        x="Previous Grades",
        nbins=20,
        title="Previous Grades Distribution",
        color_discrete_sequence=["#FF6D00"]
    )

    fig4.update_traces(
        marker_line_color="black",
        marker_line_width=1.5
    )

    st.plotly_chart(
        style_chart(fig4),
        use_container_width=True
    )

    # =====================================
    # PARENT EDUCATION
    # =====================================

    parent_counts = (
        df["Parent Education Level"]
        .value_counts()
        .reset_index()
    )

    parent_counts.columns = [
        "Parent Education Level",
        "Count"
    ]

    fig5 = px.bar(
        parent_counts,
        x="Parent Education Level",
        y="Count",
        title="Parent Education Levels",
        color="Parent Education Level"
    )

    st.plotly_chart(
        style_chart(fig5),
        use_container_width=True
    )

    # =====================================
    # EXTRACURRICULAR
    # =====================================

    activity_counts = (
        df["Participation in Extracurricular Activities"]
        .value_counts()
        .reset_index()
    )

    activity_counts.columns = [
        "Activity",
        "Count"
    ]

    fig6 = px.bar(
        activity_counts,
        x="Activity",
        y="Count",
        title="Activity Participation",
        color="Activity"
    )

    st.plotly_chart(
        style_chart(fig6),
        use_container_width=True
    )

    # =====================================
    # SCATTER PLOT
    # =====================================

    fig7 = px.scatter(
        df,
        x="Study Hours per Week",
        y="Previous Grades",
        color="Passed",
        title="Study Hours vs Grades",
        color_discrete_map={
            "Yes": "#00C853",
            "No": "#D50000"
        }
    )

    st.plotly_chart(
        style_chart(fig7),
        use_container_width=True
    )

    # =====================================
    # BOX PLOT
    # =====================================

    fig8 = px.box(
        df,
        x="Passed",
        y="Attendance Rate",
        color="Passed",
        title="Attendance Comparison",
        color_discrete_map={
            "Yes": "#00C853",
            "No": "#D50000"
        }
    )

    st.plotly_chart(
        style_chart(fig8),
        use_container_width=True
    )