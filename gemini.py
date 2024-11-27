import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def initialize_gemini(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    return model

def main():
    st.title("논문 분석 AI 어시스턴트")
    
    # API 키 입력
    api_key = st.text_input("Gemini API 키를 입력하세요", type="password")
    
    # PDF 파일 업로드
    uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")
    
    if uploaded_file and api_key:
        try:
            # PDF에서 텍스트 추출
            text_content = extract_text_from_pdf(uploaded_file)
            
            # Gemini 모델 초기화
            model = initialize_gemini(api_key)
            
            # 분석 옵션
            analysis_type = st.selectbox(
                "원하시는 분석 유형을 선택하세요",
                ["논문 요약", "주요 발견점", "연구 방법론 분석"]
            )
            
            if st.button("분석 시작"):
                with st.spinner("분석 중..."):
                    prompt = f"""
                    다음 논문을 한국어로 {analysis_type}해주세요. 
                    전문적인 용어는 원문 그대로 표기하고 괄호 안에 한국어 설명을 추가해주세요.
                    
                    논문 내용:
                    {text_content}
                    """
                    response = model.generate_content(prompt)
                    st.write(response.text)
                    
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()