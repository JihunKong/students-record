import streamlit as st
import uuid
import openai
from streamlit_extras.stateful_button import button
import pandas as pd

# Set page config
st.set_page_config(page_title="학생 교과 세부능력 및 특기사항 컨설팅", layout="wide")

# Initialize session state
if 'uuid' not in st.session_state:
    st.session_state.uuid = str(uuid.uuid4())

if 'history' not in st.session_state:
    st.session_state.history = []

# Define competencies
competencies = [
    "자기관리 역량", "지식정보처리 역량", "창의적 사고 역량", "심미적 감성 역량", "의사소통 역량", "공동체 역량",
    "비판적 사고력", "문제 해결 및 혁신 능력", "자기 주도성", "협력", "디지털 리터러시", "글로벌 시민의식"
]

# Main app
st.title("학생 교과 세부능력 및 특기사항 컨설팅")

# 1. GPT API Key input
api_key = st.text_input("GPT API 키를 입력하세요:", type="password")

# 2. Achievement standards input
achievement_standards = st.text_area("수업 내용의 성취기준을 입력하세요:")

# 3. Student achievement level and observations
student_achievement = st.text_area("학생의 성취 수준 및 관찰 내용을 입력하세요:")

# 4. Observed competencies
observed_competencies = st.multiselect("학생에게서 특별히 관찰한 역량을 선택하세요:", competencies)

# 5. Execute button
if button("실행", key="execute"):
    if not api_key:
        st.error("GPT API 키를 입력해주세요.")
    elif not achievement_standards or not student_achievement:
        st.error("모든 필드를 채워주세요.")
    else:
        with st.spinner("GPT로부터 피드백을 받아오는 중..."):
            try:
                openai.api_key = api_key
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert in educational assessment and curriculum."},
                        {"role": "user", "content": f"성취기준: {achievement_standards}\n\n학생 관찰 내용: {student_achievement}\n\n관찰된 역량: {', '.join(observed_competencies)}\n\n이 내용을 바탕으로 학생 교과 세부능력 및 특기사항에 대한 피드백을 제공해주세요. 또한 개선된 버전의 기록도 제안해주세요."}
                    ]
                )
                feedback = response.choices[0].message['content']
                
                # 6. Visual indicator (spinner) is shown above
                
                # 7. Feedback display
                st.subheader("피드백:")
                st.write(feedback)
                
                # 8. Revised student record
                st.subheader("개선된 학생 기록:")
                improved_record = st.text_area("피드백을 반영하여 수정한 학생 기록:", value=feedback.split("개선된 버전:")[-1].strip() if "개선된 버전:" in feedback else "")
                
                # 9. Data exchange record
                st.session_state.history.append({
                    "uuid": st.session_state.uuid,
                    "achievement_standards": achievement_standards,
                    "student_achievement": student_achievement,
                    "observed_competencies": observed_competencies,
                    "feedback": feedback,
                    "improved_record": improved_record
                })
                
                # Display history
                st.subheader("기록:")
                df = pd.DataFrame(st.session_state.history)
                st.dataframe(df)
                
                # Copy button for final content
                st.markdown("### 최종 내용")
                st.code(improved_record)
                st.button("복사", on_click=lambda: st.write(st.clipboard.write(improved_record)))
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")

# UUID display (for demonstration, you might want to hide this in production)
st.sidebar.write(f"Your session UUID: {st.session_state.uuid}")
