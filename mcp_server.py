# Import necessary libraries
import os
import json
from mcp import McpServer, Tool, Resource  # Custom module with server and decorators
from groq import Groq  # Groq API client
from dotenv import load_dotenv  # For loading environment variables
from typing import Dict, Any  # For type hinting

# Load environment variables from .env file
load_dotenv()

class EduChainMcpServer:
    def __init__(self):
        # Initialize Groq client with API key from environment
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        # Set the model to be used with Groq API
        self.model = "llama3-70b-8192"
        
        # Initialize the MCP server with metadata
        self.server = McpServer(
            name="EduChain Server",
            version="1.0",
            description="Educational content generator using Groq API"
        )
        
        # Register all tools (functions) and resources (structured data generators)
        self._register_tools()
        self._register_resources()

    def _call_groq_api(self, prompt: str) -> Dict[str, Any]:
        """
        Calls the Groq API with the provided prompt and returns parsed JSON.
        Handles JSON decoding errors and other exceptions gracefully.
        """
        try:
            # Make a chat completion request to Groq API
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.7,
                response_format={"type": "json_object"}  # Expecting JSON-formatted response
            )
            # Parse and return JSON content from the response
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            # Handle invalid JSON responses
            return {"error": "Invalid JSON response from API", "status": 500}
        except Exception as e:
            # Handle any other exception
            return {"error": str(e), "status": 500}

    def _register_tools(self):
        """Defines and registers tools that users can invoke on the server"""

        @self.server.tool(
            name="generate_mcqs",
            description="Generate multiple-choice questions for a given topic",
            parameters={
                "topic": {"type": "string", "description": "Topic for questions"},
                "num_questions": {
                    "type": "integer", 
                    "description": "Number of questions (1-10)",
                    "default": 5,
                    "min": 1,
                    "max": 10
                }
            }
        )
        def generate_mcqs(topic: str, num_questions: int = 5) -> Dict[str, Any]:
            # Compose prompt to generate MCQs based on the topic and number of questions
            prompt = f"""Generate {num_questions} high-quality multiple-choice questions about {topic}.
            Requirements:
            - Questions should test different cognitive levels
            - Include 4 options per question
            - Mark the correct answer
            - Provide explanations
            
            Return JSON with this structure:
            {{
                "topic": "string",
                "questions": [
                    {{
                        "question": "string",
                        "options": ["A", "B", "C", "D"],
                        "correct_answer": "string",
                        "explanation": "string",
                        "difficulty": "easy|medium|hard"
                    }}
                ]
            }}"""
            # Send prompt to Groq API and return response
            return self._call_groq_api(prompt)

    def _register_resources(self):
        """Defines and registers reusable content generation resources"""

        @self.server.resource(
            name="lesson_plans",
            description="Generate structured lesson plans",
            parameters={
                "topic": {"type": "string", "description": "Lesson topic"},
                "duration": {
                    "type": "string", 
                    "description": "Total duration (e.g., '90 minutes')",
                    "default": "60 minutes"
                },
                "level": {
                    "type": "string",
                    "description": "Target audience level",
                    "enum": ["beginner", "intermediate", "advanced"],
                    "default": "beginner"
                }
            }
        )
        def generate_lesson_plan(topic: str, duration: str = "60 minutes", level: str = "beginner") -> Dict[str, Any]:
            # Compose prompt for lesson plan generation
            prompt = f"""Create a {duration} lesson plan about {topic} for {level} learners.
            Required structure:
            {{
                "topic": "string",
                "duration": "string",
                "level": "string",
                "learning_objectives": ["string"],
                "sections": [
                    {{
                        "title": "string",
                        "duration": "string",
                        "content": "string",
                        "activities": ["string"],
                        "materials": ["string"]
                    }}
                ],
                "assessment": {{
                    "type": "string",
                    "description": "string"
                }}
            }}"""
            # Call the API and return the structured response
            return self._call_groq_api(prompt)

    def run(self, host: str = "0.0.0.0", port: int = 6000):
        """Starts the MCP server and listens for incoming requests"""
        print(f"Starting EduChain MCP server on {host}:{port}")
        try:
            self.server.run(host=host, port=port)
        except Exception as e:
            print(f"Server failed: {str(e)}")
            raise

# Entry point: Create the server instance and run it
if __name__ == "__main__":
    try:
        server = EduChainMcpServer()
        server.run()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Critical error: {str(e)}")
