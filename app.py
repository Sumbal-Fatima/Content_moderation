import os
from groq import Groq
from dotenv import load_dotenv
import gradio as gr

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Function to moderate content
def moderate_content(user_input):
    try:
        # Generate moderation report using Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze this content for violations: {user_input}",
                }
            ],
            model="llama-3.3-70b-versatile",
            stream=False,
        )
        response = chat_completion.choices[0].message.content

        # Suggest actions based on the response
        if "violation" in response.lower():
            action = "Flag or delete this content."
        else:
            action = "Content is compliant."

        return response, action

    except Exception as e:
        return f"Error: {str(e)}", "No action suggested."

# Define Gradio interface
with gr.Blocks() as app:
    gr.Markdown("### Content Moderation with Groq API")
    with gr.Row():
        with gr.Column():
            user_input = gr.Textbox(
                label="Enter Content for Moderation",
                placeholder="Type the content you want to moderate here...",
            )
            moderate_btn = gr.Button("Moderate Content")
        with gr.Column():
            moderation_result = gr.Textbox(label="Moderation Result", interactive=False)
            suggested_action = gr.Textbox(label="Suggested Action", interactive=False)

    # Connect button to moderation function
    moderate_btn.click(
        moderate_content,
        inputs=[user_input],
        outputs=[moderation_result, suggested_action],
    )

# Run the Gradio app
if __name__ == "__main__":
    app.launch()
