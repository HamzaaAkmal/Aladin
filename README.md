# Aladin Blog Generator - Streamlit App

This project is a Streamlit web application that uses Google's Gemini 1.5 Pro model to generate blog articles, complete with SEO and emotional metadata.  It's designed to be user-friendly and produce high-quality, human-like content.

## Features

*   **Generates complete blog articles:**  Creates blog posts based on a topic, keyword, and optional additional information.
*   **SEO Optimization:** Generates an SEO-optimized title and description.
*   **Emotional Engagement:**  Generates an emotional title and description to capture reader interest.
*   **URL Slug Generation:** Creates an SEO-friendly URL slug for the blog post.
*   **Content Formatting:**  Uses simple English, headings, subheadings, bullet points, and quotes.
*   **FAQ Section:** Includes a frequently asked questions section at the end of the blog.
*   **Word Count Control:** Allows the user to specify a target word count for the article.
*   **Copy to Clipboard:** Provides a button to easily copy the generated blog content to the clipboard.
*   **Error Handling:** Displays error messages if there are issues with content generation.
*   **Responsive UI:** Uses Streamlit's layout features for a user-friendly experience.
*   **About Sidebar:** Explains the purpose and features of the Aladin AI.

## How it Works

The application utilizes the following core components:

1.  **Streamlit:**  A Python library for building interactive web applications.  It handles the user interface, input fields, and display of the generated content.

2.  **Google Generative AI (Gemini 1.5 Pro):**  A powerful language model used to generate the blog content.  The application sends a carefully crafted prompt to the Gemini API, which includes the user's input (topic, keyword, etc.) and instructions on the desired style and format.  The API returns the generated text. *It is highly recommended that you use Gemini 1.5 Pro or another large language model for best results.*

3.  **`python-dotenv`:**  Loads the Google API key from a `.env` file, keeping sensitive information secure.

4.  **Prompt Engineering:** The `prompt_guidelines` variable contains a detailed prompt that instructs the Gemini model on how to generate the blog content.  This prompt specifies the persona ("Aladin"), the desired writing style (simple English, inspired by GQ and The Guardian), the structure of the blog post (headings, FAQ, etc.), and the required metadata.

5.  **Content Parsing:** The `generate_blog_content` function sends the prompt to the Gemini API, receives the response, and parses it to extract the different sections (SEO title, blog content, etc.).

6.  **UI Elements:** The Streamlit code creates input fields for the topic, keyword, additional information, and word count.  It displays the generated output in separate sections, including tabs for the SEO and emotional metadata. It also provides a button to copy all of the blog content to the clipboard.

## How to Run

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install dependencies:**

    ```bash
    pip install streamlit google-generativeai python-dotenv
    ```

3.  **Create a `.env` file:**

    Create a file named `.env` in the root directory of the project.  Add your Google API key to this file:

    ```
    GOOGLE_API_KEY=your_api_key_here
    ```

    Replace `your_api_key_here` with your actual API key.  **Do not commit this `.env` file to your Git repository.** Add `.env` to your `.gitignore` file.

4.  **Run the Streamlit app:**

    ```bash
    streamlit run your_script_name.py  # Replace with the actual filename
    ```

    This will open the application in your default web browser.

## Important Notes

*   **API Key:** You need a Google API key with access to the Gemini API to use this application.  Obtain an API key from the Google Cloud Console.
*   **Model Choice:** The code is configured to use `gemini-1.5-pro`. You should use this model, or the latest available powerful Gemini model, for the best results.  Less capable models may not follow the instructions as well.  If necessary, modify the `model` variable in the code to use a different model.
*   **Cost:** Using the Gemini API may incur costs depending on your usage and Google Cloud pricing.
*    **.gitignore:** Ensure that you have a `.gitignore` file, and it includes `.env`. This prevents accidental uploading of your API key to GitHub. If you don't already have one, create a `.gitignore` file in the root of your repository with the following content:
    ```
    .env
    ```


## Example Usage

1.  Open the web application in your browser.
2.  Enter the blog topic (e.g., "The Benefits of Reading").
3.  Enter the main keyword (e.g., "reading benefits").
4.  (Optional) Provide additional context (e.g., "Focus on benefits for children").
5.  Set the target word count (e.g., 800).
6.  Click the "✨ Generate Blog with Aladin" button.
7.  The application will generate the blog content, SEO metadata, emotional metadata, and URL slug.
8.  You can copy the blog content using the "📋 Copy Blog Content" button.
9. Review the generated output and check the word count.

This Markdown provides a comprehensive overview of the project, its features, how it works, how to run it, important considerations, and how to use it. It's suitable for a GitHub repository README file.
