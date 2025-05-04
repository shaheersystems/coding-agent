from google.adk.agents import LlmAgent, SequentialAgent
from .prompts import code_writer_instructions, code_reviwer_instructions, code_refactor_instructions
from dotenv import load_dotenv
import os
load_dotenv()


os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY")

GEMINI_MODEL="gemini-2.0-flash"


# --- 1. Define Sub-Agents for Each Pipeline Stage ---

# Code Writer Agent
# Takes the initial specification (from user query) and writes code.

code_writer_agent=LlmAgent(
    name="CodeWriterAgent",
    model=GEMINI_MODEL,
    instruction=code_writer_instructions(),
    description="Writes initial Python code based on a specification.",
    output_key="generated_code"
)


code_reviewer_agent=LlmAgent(
    name="CodeReviewerAgent",
    model=GEMINI_MODEL,
    instruction=code_reviwer_instructions(),
    description="Reviews code and provides feedback.",
    output_key="review_comments"
)


code_refactor_agent=LlmAgent(
    name="CodeRefactorerAgent",
    model=GEMINI_MODEL,
    instruction=code_refactor_instructions(),
    description="Refactors code based on review comments.",
    output_key="refactored_code", # Stores output in state['refactored_code']
)


# --- 2. Create the SequentialAgent ---
# This agent orchestrates the pipeline by running the sub_agents in order.


code_pipleline_agent=SequentialAgent(
    name="CodePipelineAgent",
    sub_agents=[code_writer_agent, code_reviewer_agent, code_refactor_agent],
    description="Executes a sequence of code writing, reviewing, and refactoring.",
)



root_agent=code_pipleline_agent