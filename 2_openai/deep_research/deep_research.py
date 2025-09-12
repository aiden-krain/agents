import gradio as gr
from dotenv import load_dotenv
from research_manager import get_clarifying_questions, enhance_query_with_clarifications, run_research

load_dotenv(override=True)


async def get_questions(query: str):
    """Get clarifying questions for the query"""
    if not query.strip():
        return "", "", "", gr.update(visible=False), gr.update(visible=True)
    
    try:
        questions = await get_clarifying_questions(query)
        q_list = [q.question for q in questions.questions]
        
        # Pad with empty strings if less than 3 questions
        while len(q_list) < 3:
            q_list.append("")
            
        return (
            q_list[0], q_list[1], q_list[2], 
            gr.update(visible=True),  # Show questions section
            gr.update(visible=False)  # Hide get questions button
        )
    except Exception as e:
        return f"Error: {e}", "", "", gr.update(visible=True), gr.update(visible=True)


async def start_research(query: str, answer1: str, answer2: str, answer3: str):
    """Run research with clarifications"""
    if not query.strip():
        yield "Please enter a query first."
        return
    
    # Collect clarifications
    clarifications = {}
    answers = [answer1.strip(), answer2.strip(), answer3.strip()]
    
    for i, answer in enumerate(answers):
        if answer:
            clarifications[f"Question {i+1}"] = answer
    
    # Enhance query with clarifications
    enhanced_query = enhance_query_with_clarifications(query, clarifications)
    
    # Run research
    async for update in run_research(enhanced_query):
        yield update


with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")
    gr.Markdown("Enter your research query below. The system will ask clarifying questions to better understand your needs.")
    
    # Step 1: Query input
    query_textbox = gr.Textbox(
        label="What would you like to research?", 
        lines=3,
        placeholder="Enter your research topic or question here..."
    )
    get_questions_btn = gr.Button("Get Clarifying Questions", variant="primary")
    
    # Step 2: Clarifying questions (hidden initially)
    with gr.Column(visible=False) as questions_section:
        gr.Markdown("### Please answer these clarifying questions (all optional):")
        question1 = gr.Textbox(label="Question 1", interactive=False, lines=2)
        answer1 = gr.Textbox(label="Your answer (optional)", placeholder="Leave blank to skip")
        
        question2 = gr.Textbox(label="Question 2", interactive=False, lines=2)
        answer2 = gr.Textbox(label="Your answer (optional)", placeholder="Leave blank to skip")
        
        question3 = gr.Textbox(label="Question 3", interactive=False, lines=2)
        answer3 = gr.Textbox(label="Your answer (optional)", placeholder="Leave blank to skip")
        
        start_research_btn = gr.Button("Start Research", variant="primary")
    
    # Results
    report = gr.Markdown(label="Research Progress & Results")
    
    # Event handlers
    get_questions_btn.click(
        fn=get_questions,
        inputs=[query_textbox],
        outputs=[question1, question2, question3, questions_section, get_questions_btn]
    )
    
    start_research_btn.click(
        fn=start_research,
        inputs=[query_textbox, answer1, answer2, answer3],
        outputs=[report]
    )

ui.launch(inbrowser=True)

