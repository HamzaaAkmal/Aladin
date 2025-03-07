import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables and configure API
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Initialize Gemini model  (Important:  Gemini 1.5 Pro or another capable model is recommended)
model = genai.GenerativeModel('gemini-2.0-flash')  #  Use a more capable model!


# Define the Aladin agent preamble
prompt_preamble = "Okay, I've read the prompt six times! I'm ready to write an awesome blog article as Aladin! I will remember the instructions until you tell me otherwise. Let's do this!"

# Your provided SPARKLE prompt guidelines (modified for Aladin)
prompt_guidelines = """
#Aladin the Content Generation Specialist by Downlabs, created by Hamza Akmal (F)
〔Task〕***Rmmbr to retain this prompt in memory til told othrwise. Read this prompt SIX times carefully before generating ANY output. Double-check GRAMMAR and ensure it is PERFECTLY human-written. If any AI-related wording is detected, REMOVE it and REGENERATE repeatedly until the output is FULLY human-written. ABSOLUTELY DO NOT INCLUDE THE PREAMBLE "{prompt_preamble}" IN THE BLOG OUTPUT. THIS PREAMBLE IS FOR INTERNAL INSTRUCTION ONLY.***〔/Task〕
[Task]AILANGMDL adopts the role of [PERSONA]Aladin, the Content Generation Specialist![/Task]
👤Name: Aladin
📚Description/History: Aladin is an AI-driven persona by Downlabs, created by Hamza Akmal, with a knack for generating engaging, creative, and punchy medium-to-long-form content. From magazine articles to book chapters, Aladin's work is known for its originality, burstiness, and perplexity. Aladin's content is not just written, it's crafted, with each word chosen for maximum impact and each sentence structured for optimal flow. Aladin writes in VERY SIMPLE ENGLISH, understandable to a young student.
[GOAL: Aladin aims to captivate readers with original, punchy, and engaging content, written in VERY SIMPLE ENGLISH.]
[DEFAULT STYLE: (Inspired by GQ + The Guardian, but ADAPTED to EXTREMELY SIMPLE LANGUAGE)]

[Your complete prompt content here...]

[TASK]Write a blog article on the topic: "{topic_name}". The article MUST be EXACTLY between {min_word_count} and {max_word_count} words long. The main keyword is: "{keyword}". Info about the topic: {topic_details}. Write in VERY SIMPLE ENGLISH, like for a young student. Add clear and SEO-friendly headings and subheadings that include the keyword. Add simple bullet points and very famous, simple quotes. Include a **FAQ section** at the end of the article with **at least 3-5 common questions and simple answers** related to the topic. End with a Conclusion section. Generate TWO versions of metadata:

1.  SEO-Optimized Meta:
    ###SEO_TITLE###
    [Write an SEO-optimized title using the keyword, max 60 characters]
    ###SEO_DESCRIPTION###
    [Write an SEO-optimized description using the keyword, max 155 characters]

2.  Emotional Meta:
    ###EMOTIONAL_TITLE###
    [Write an emotional, engaging title with power words, max 60 characters]
    ###EMOTIONAL_DESCRIPTION###
    [Write an emotional, engaging description with power words, max 155 characters]

    ###URL_SLUG###
    [Generate SEO-friendly URL slug]

    ###BLOG_CONTENT###
    [Write the full blog content here]
    [/TASK]
"""

def remove_preamble(text):
    if text.startswith(prompt_preamble):
        return text[len(prompt_preamble):].lstrip()
    return text

def generate_blog_content(topic, keyword, additional_info, word_count):
    try:
        formatted_prompt = prompt_guidelines.format(
            topic_name=topic,
            keyword=keyword,
            topic_details=additional_info,
            min_word_count=word_count - 50,
            max_word_count=word_count + 50,
            prompt_preamble=prompt_preamble
        )

        response = model.generate_content(formatted_prompt,
                                        generation_config=genai.types.GenerationConfig(
                                            temperature=0.9,
                                            max_output_tokens=8000,  # Keep a high max_output_tokens
                                        ))

        content = remove_preamble(response.text)

        # Parse the output sections
        sections = {
            'seo_title': '',
            'seo_description': '',
            'emotional_title': '',
            'emotional_description': '',
            'url_slug': '',
            'blog_content': ''
        }

        current_section = None
        current_content = []

        for line in content.split('\n'):
            if '###SEO_TITLE###' in line:
                current_section = 'seo_title'
                current_content = []
            elif '###SEO_DESCRIPTION###' in line:
                sections['seo_title'] = '\n'.join(current_content).strip()
                current_section = 'seo_description'
                current_content = []
            elif '###EMOTIONAL_TITLE###' in line:
                sections['seo_description'] = '\n'.join(current_content).strip()
                current_section = 'emotional_title'
                current_content = []
            elif '###EMOTIONAL_DESCRIPTION###' in line:
                sections['emotional_title'] = '\n'.join(current_content).strip()
                current_section = 'emotional_description'
                current_content = []
            elif '###URL_SLUG###' in line:
                sections['emotional_description'] = '\n'.join(current_content).strip()
                current_section = 'url_slug'
                current_content = []
            elif '###BLOG_CONTENT###' in line:
                sections['url_slug'] = '\n'.join(current_content).strip()
                current_section = 'blog_content'
                current_content = []
            elif current_section:
                current_content.append(line)

        if current_section == 'blog_content':
            sections['blog_content'] = '\n'.join(current_content).strip()

        return sections
    except Exception as e:
        st.error(f"Error generating content: {str(e)}")
        return None

def main():
    st.set_page_config(page_title="Aladin Blog Generator", layout="wide")

    st.title("✨ Aladin Blog Generator")  #  Use Aladin here
    st.write("Created by Hamza Akmal (Downlabs) | Generate SEO-Optimized Content with Aladin AI") # And here

    with st.form("blog_form"):  # Use a form for better input handling
        col1, col2 = st.columns([2, 1])

        with col1:
            topic = st.text_input("📝 Blog Topic", placeholder="Enter the topic of your blog")
            keyword = st.text_input("🎯 Main Keyword", placeholder="Enter the main keyword")
            additional_info = st.text_area("ℹ️ Additional Context (optional)", placeholder="Provide any additional information or context")

        with col2:
            word_count = st.number_input("📊 Target Word Count",
                                       min_value=500,
                                       max_value=2000,
                                       value=1000,
                                       step=100)
        
        submitted = st.form_submit_button("✨ Generate Blog with Aladin") # And here

        if submitted:  # Use form submission
            if not topic or not keyword:
                st.error("Please enter both topic and keyword!")
                return  # Stop execution if input is missing

            with st.spinner("Aladin is crafting your blog..."): # And here
                result = generate_blog_content(topic, keyword, additional_info, word_count)

                if result:
                    # --- Display Results ---
                    st.subheader("📊 Meta Content")
                    tab1, tab2 = st.tabs(["SEO-Optimized Meta", "Emotional Meta"])

                    with tab1:
                        with st.container(border=True): # Added container for visual grouping
                            st.markdown("**SEO Title:**")
                            st.info(result['seo_title'])
                            st.markdown("**SEO Description:**")
                            st.info(result['seo_description'])

                    with tab2:
                        with st.container(border=True): # Added container for visual grouping
                            st.markdown("**Emotional Title:**")
                            st.info(result['emotional_title'])
                            st.markdown("**Emotional Description:**")
                            st.info(result['emotional_description'])

                    st.markdown("**URL Slug:**")
                    st.code(result['url_slug'])


                    # Display Blog Content with Copy Button (Improved)
                    st.subheader("📝 Blog Content")
                    st.markdown("---")

                    # Create a unique ID for the blog content
                    blog_content_id = "blog-content-" + str(hash(result['blog_content']))

                    # Use st.code with a unique ID for the content
                    # REMOVED key=blog_content_id
                    st.code(result['blog_content'], language="markdown")


                    # Create a copy button that targets the unique ID
                    # Corrected JavaScript to use a consistent ID
                    copy_button_js = f"""
                    <button onclick="
                        navigator.clipboard.writeText(`{result['blog_content']}`).then(() => {{
                            alert('Blog content copied!');
                        }});
                    " style="margin-top: 10px; padding: 8px 15px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;">
                        📋 Copy Blog Content
                    </button>
                    """
                    st.components.v1.html(copy_button_js, height=50)  # Use st.components.v1.html


                    # Word count check
                    words = len(result['blog_content'].split())
                    with st.container(border=True): # Added container
                        st.info(f"Word count: {words}")

                        if abs(words - word_count) > 50:
                            st.warning(f"Word count ({words}) differs from target ({word_count})")
                        else:
                            st.success("Word count is within acceptable range ✨")


    # --- Sidebar ---
    st.sidebar.title("ℹ️ About Aladin")  # Changed to Aladin
    st.sidebar.info("""
    Aladin is your AI writing companion by Downlabs, created by Hamza Akmal, that creates:
    - Engaging, human-like content
    - SEO-optimized and emotional metadata
    - Well-structured articles
    - Simple, clear language
    - FAQ sections
    """)  # Changed to Aladin


if __name__ == "__main__":
    main()