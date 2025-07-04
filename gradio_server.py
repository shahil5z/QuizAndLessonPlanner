# Import necessary libraries
import gradio as gr  # For building the web interface
from groq import Groq  # For connecting to the Groq API (LLM service)
from dotenv import load_dotenv  # For loading environment variables from a .env file
import os
import json

# Load environment variables (e.g., GROQ_API_KEY)
load_dotenv()

# Initialize the Groq client using the API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Define the LLM model to be used
MODEL = "llama3-70b-8192"

# Function to convert MCQ JSON data to formatted HTML for display in Gradio
def format_mcqs_for_display(json_data):
    """Convert MCQ JSON to interactive HTML format"""

    # Create the quiz container
    html_output = f"""
    <div style='font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; color: #ffffff; background-color: #0e1117; padding: 20px; border-radius: 8px;'>
        <h2 style='color: #6cb4ff; padding-bottom: 8px; border-bottom: 1px solid #444;'>📝 Quiz: {json_data['topic']}</h2>
    """

    # Loop through each question
    for i, question in enumerate(json_data["questions"], 1):
        html_output += f"""
        <div style='margin-bottom: 30px; padding: 15px; border-radius: 4px; border: 1px solid #333; background-color: #161b22;'>
            <h3 style='color: #6cb4ff; margin-top: 0;'>Q{i}. {question['question']}</h3>
            <div style='margin-left: 10px;'>
        """

        # Add each option as a radio button
        for j, opt in enumerate(question["options"]):
            html_output += f"""
            <div style='padding: 8px 0; display: flex; align-items: center; cursor: pointer; color: #ffffff;'
                 onclick='this.querySelector("input").checked = true'>
                <input type='radio' name='q{i}' id='q{i}o{j}' style='margin-right: 10px;'>
                <label for='q{i}o{j}' style='flex: 1; cursor: pointer;'>{opt}</label>
            </div>
            """

        # Add answer reveal section
        html_output += f"""
            </div>
            <div id='answer-{i}' style='display: none; margin-top: 15px; padding: 12px; background: #1f2937; border-radius: 4px; color: #d1d5db;'>
                <p style='margin: 0 0 8px 0;'><strong style='color: #22c55e;'>✅ Correct Answer:</strong> {question['correct_answer']}</p>
                <p style='margin: 0;'><strong>💡 Explanation:</strong> {question['explanation']}</p>
            </div>
            <button onclick='document.getElementById(\"answer-{i}\").style.display = \"block\"; this.style.display = \"none\"' 
                    style='margin-top: 10px; background: #374151; color: #ffffff; border: 1px solid #4b5563; padding: 6px 12px; border-radius: 4px; cursor: pointer;'>
                Show Answer
            </button>
        </div>
        """

    html_output += "</div>"
    return html_output

# Function to convert lesson plan JSON data to markdown
def format_lesson_plan(json_data):
    """Convert lesson plan JSON to structured markdown"""
    
    output = f"# 📚 Lesson Plan: {json_data['topic']}\n"
    output += f"**Duration:** {json_data['duration']}\n\n"

    # Add learning objectives
    output += "## 🎯 Learning Objectives:\n"
    for obj in json_data["objectives"]:
        output += f"- {obj}\n"

    # Add structured sections
    output += "\n## 📖 Lesson Structure:\n"
    for section in json_data["sections"]:
        output += f"\n### {section['title']} ({section['duration']})\n"
        output += f"{section['content']}\n"
        if "activities" in section:
            output += "\n#### 🔹 Activities:\n"
            for activity in section["activities"]:
                output += f"- {activity}\n"

    # Add assessment method
    output += f"\n## 📝 Assessment:\n{json_data['assessment']}\n"
    return output

# Function to generate MCQs using the Groq LLM
def generate_mcqs(topic: str, num_questions: int = 5):
    # Define prompt for the LLM
    prompt = f"""Generate {num_questions} multiple-choice questions about {topic}.
    For each question:
    - Provide 4 clear options (A-D)
    - Mark the correct answer
    - Add a 1-sentence explanation
    Return JSON with this structure:
    {{"topic": "string", "questions": [{{"question": "string", "options": ["A", ...], "correct_answer": "string", "explanation": "string"}}]}}"""

    # Send request to Groq API
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=MODEL,
        temperature=0.7,
        response_format={"type": "json_object"}
    )

    # Convert model response to JSON and format it for display
    json_data = json.loads(response.choices[0].message.content)
    return format_mcqs_for_display(json_data)

# Function to generate a lesson plan using the Groq LLM
def generate_lesson_plan(topic: str, duration: str = "60 minutes"):
    # Define prompt for the LLM
    prompt = f"""Create a {duration} lesson plan about {topic}.
    Include:
    - 3-5 learning objectives
    - 3-5 sections with titles/durations
    - Key content points for each section
    - Suggested activities
    - Assessment method
    Return JSON with this structure:
    {{"topic": "string", "duration": "string", "objectives": ["string"], 
    "sections": [{{"title": "string", "content": "string", "duration": "string", 
    "activities": ["string"]}}], "assessment": "string"}}"""

    # Send request to Groq API
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=MODEL,
        temperature=0.5,
        response_format={"type": "json_object"}
    )

    # Convert model response to JSON and format it for display
    json_data = json.loads(response.choices[0].message.content)
    return format_lesson_plan(json_data)

# Build Gradio interface
with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🎓 EduChain")  # App title

    # Tab 1: Quiz Generator
    with gr.Tab("✏️ Quiz Generator"):
        with gr.Row():
            topic_mcq = gr.Textbox(label="Topic", placeholder="e.g., Quantum Mechanics")  # Input: topic
            num_questions = gr.Dropdown(
                choices=[str(i) for i in range(1, 16)],
                value="5",
                label="Number of Questions"
            )  # Dropdown to choose number of questions
        mcq_btn = gr.Button("Generate Quiz", variant="primary")  # Button to generate quiz
        mcq_output = gr.HTML(label="Generated Quiz")  # HTML output for MCQ display

    # Tab 2: Lesson Planner
    with gr.Tab("📖 Lesson Planner"):
        with gr.Row():
            topic_lesson = gr.Textbox(label="Topic", placeholder="e.g., Thermodynamics")  # Input: topic
            duration = gr.Dropdown(["30 mins", "60 mins", "90 mins", "2 hours"], value="60 mins", label="Duration")  # Duration dropdown
        lesson_btn = gr.Button("Create Plan", variant="primary")  # Button to generate lesson plan
        lesson_output = gr.Markdown(label="Lesson Plan")  # Output lesson plan in markdown

    # Button click event handlers
    mcq_btn.click(
        generate_mcqs,
        inputs=[topic_mcq, num_questions],
        outputs=mcq_output
    )
    lesson_btn.click(
        generate_lesson_plan,
        inputs=[topic_lesson, duration],
        outputs=lesson_output
    )

# Run the app on port 7860
if __name__ == "__main__":
    app.launch(server_port=7860)
