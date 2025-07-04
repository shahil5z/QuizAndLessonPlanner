# EduChain - Educational Content Generator

## Overview
EduChain is a simple tool that creates educational content like quizzes and lesson plans using the Groq API. It has two main parts: a command-line script for generating content and a web interface built with Gradio for easy use. The tool is designed to help teachers and learners create multiple-choice questions (MCQs) and structured lesson plans on any topic.

## Features
- **Quiz Generator**: Creates multiple-choice questions with options, correct answers, and explanations for any topic.
- **Lesson Planner**: Generates detailed lesson plans with objectives, sections, activities, and assessments.
- **Web Interface**: A user-friendly Gradio interface with two tabs: "Quiz Generator" and "Lesson Planner" (see sample images in the project folder: `quiz_generator.png` and `lesson_planner.png`).
- **Command-Line Tool**: A script to generate and save quizzes and lesson plans as JSON files.
- **MCP Server**: A mock server setup to handle educational content generation requests.

## Project Structure
- `educhain_setup.py`: Command-line script to generate and save MCQs and lesson plans as JSON files.
- `mcp_server.py`: Mock server for handling content generation requests using the Groq API.
- `mcp.py`: Mock implementation of the MCP server, tool, and resource classes for testing.
- `gradio_server.py`: Web interface using Gradio for generating and displaying quizzes and lesson plans.
- Sample images:
  - `quiz_generator.png`: Screenshot of the Quiz Generator tab in the Gradio interface.
  - `lesson_planner.png`: Screenshot of the Lesson Planner tab in the Gradio interface.

## Requirements
- Python 3.8 or higher
- Required libraries: `groq`, `python-dotenv`, `gradio`
- A valid Groq API key (stored in a `.env` file)

## Setup
1. **Install Dependencies**:
   Run the following command to install required Python libraries:
   ```
   pip install groq python-dotenv gradio
   ```

2. **Set Up API Key**:
   - Create a `.env` file in the project folder.
   - Add your Groq API key like this:
     ```
     GROQ_API_KEY=your_api_key_here
     ```

3. **Prepare the Project**:
   - Ensure all Python files (`educhain_setup.py`, `mcp_server.py`, `mcp.py`, `gradio_server.py`) are in the same folder.
   - Place the sample images (`quiz_generator.png`, `lesson_planner.png`) in the project folder for reference.

## How to Use
### 1. Command-Line Tool (`educhain_setup.py`)
- Run the script to generate MCQs and a lesson plan for "Python Programming Basics" (or change the topic in the code):
  ```
  python educhain_setup.py
  ```
- Output:
  - MCQs are saved to `mcqs.json`.
  - Lesson plan is saved to `lesson_plan.json`.

### 2. Web Interface (`gradio_server.py`)
- Start the Gradio web server:
  ```
  python gradio_server.py
  ```
- Open your browser and go to `http://localhost:7860`.
- Use the interface:
  - **Quiz Generator Tab**: Enter a topic and select the number of questions, then click "Generate Quiz" to see the quiz.
  - **Lesson Planner Tab**: Enter a topic and choose a duration, then click "Create Plan" to view the lesson plan.
- Check the sample images (`quiz_generator.png`, `lesson_planner.png`) to see how the interface looks.

### 3. MCP Server (`mcp_server.py`)
- Run the mock server:
  ```
  python mcp_server.py
  ```
- The server will list registered tools and resources but runs in mock mode (no real HTTP requests).

## Notes
- The project uses the Groq API with the `llama3-70b-8192` model for content generation.
- The Gradio interface runs on port `7860` by default.
- The MCP server runs on port `6000` by default (mock mode only).
- Make sure your `.env` file has a valid Groq API key.
- The sample images (`quiz_generator.png`, `lesson_planner.png`) show the Gradio UI for reference.