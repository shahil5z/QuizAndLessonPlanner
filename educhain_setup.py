import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file (used to securely load API keys)
load_dotenv()

class EduChainGenerator:
    def __init__(self, api_key=None):
        # Initialize the Groq client using either the provided API key or the one in the .env file
        self.client = Groq(api_key=api_key or os.getenv("GROQ_API_KEY"))
        
        # Specify the model to be used (note: second line overrides the first)
        self.model = "mixtral-8x7b-32768" 
        self.model = "llama3-70b-8192"  # This is the effective model used

    def generate_mcq(self, topic, num_questions=5):
        # Create a prompt to generate multiple-choice questions in a specified JSON format
        prompt = f"""Generate {num_questions} high-quality multiple-choice questions about {topic}.
        Return as JSON with this exact structure:
        {{
            "topic": "string",
            "questions": [
                {{
                    "question": "string",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "A",
                    "explanation": "string"
                }}
            ]
        }}
        Include questions that test different levels of understanding.
        """
        return self._generate_content(prompt)

    def generate_lesson_plan(self, topic):
        # Create a prompt to generate a comprehensive lesson plan in a specified JSON format
        prompt = f"""Generate a comprehensive lesson plan about {topic}.
        Return as JSON with this exact structure:
        {{
            "topic": "string",
            "duration": "string",
            "objectives": ["string"],
            "sections": [
                {{
                    "title": "string",
                    "content": "string",
                    "duration": "string",
                    "activities": ["string"]
                }}
            ],
            "assessment": "string",
            "resources": ["string"]
        }}
        Include hands-on activities where appropriate.
        """
        return self._generate_content(prompt)

    def _generate_content(self, prompt):
        # Internal method to send a chat prompt to the Groq model and handle JSON response
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.7,
                response_format={"type": "json_object"}  # Ensure JSON response
            )
            content = response.choices[0].message.content
            return json.loads(content)  # Parse and return JSON content
        except json.JSONDecodeError:
            # If the response is not valid JSON, return raw content with a warning
            print("Failed to parse JSON response, returning raw content")
            return {"content": content}
        except Exception as e:
            # Catch all other errors and return None
            print(f"Error generating content: {e}")
            return None

def save_to_file(filename, data):
    """Helper function to save data to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)  # Save formatted JSON
        return True
    except Exception as e:
        # Print error if file saving fails
        print(f"Error saving to {filename}: {e}")
        return False

def main():
    # Create an instance of the EduChainGenerator
    generator = EduChainGenerator()
    
    # Define the topic for which content will be generated
    topic = "Python Programming Basics"
    print(f"Generating content for: {topic}")
    
    # Generate MCQs and save to file
    print("\nGenerating multiple-choice questions...")
    mcqs = generator.generate_mcq(topic)
    if mcqs:
        save_to_file('mcqs.json', mcqs)
        print("✓ MCQs saved to mcqs.json")
    else:
        print("× Failed to generate MCQs")
    
    # Generate lesson plan and save to file
    print("\nGenerating lesson plan...")
    lesson_plan = generator.generate_lesson_plan(topic)
    if lesson_plan:
        save_to_file('lesson_plan.json', lesson_plan)
        print("✓ Lesson plan saved to lesson_plan.json")
    else:
        print("× Failed to generate lesson plan")
    
    print("\nProcess completed!")

if __name__ == "__main__":
    # Entry point of the script
    main()
    