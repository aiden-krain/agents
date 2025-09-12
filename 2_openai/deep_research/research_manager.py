from agents import Agent, Runner, function_tool, trace, gen_trace_id
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from clarifying_agent import clarifying_agent, ClarifyingQuestions
from email_agent import email_agent
import asyncio


@function_tool
async def plan_searches(query: str) -> WebSearchPlan:
    """Plan the searches to perform for the query"""
    print("🔍 Planning searches for your query...")
    result = await Runner.run(
        planner_agent,
        f"Query: {query}",
    )
    search_count = len(result.final_output.searches)
    print(f"✅ Search planning complete - {search_count} searches planned")
    
    # Log the planned searches
    for i, search in enumerate(result.final_output.searches, 1):
        print(f"   {i}. {search.query} - {search.reason}")
    
    return result.final_output_as(WebSearchPlan)


@function_tool
async def perform_searches(search_plan: WebSearchPlan) -> list[str]:
    """Perform the planned searches"""
    total_searches = len(search_plan.searches)
    print(f"🌐 Starting {total_searches} web searches...")
    
    # Execute searches directly using the WebSearchPlan
    num_completed = 0
    tasks = [asyncio.create_task(_search_single(item, i+1)) for i, item in enumerate(search_plan.searches)]
    results = []
    
    for task in asyncio.as_completed(tasks):
        result = await task
        if result is not None:
            results.append(result)
        num_completed += 1
        print(f"📊 Search progress: {num_completed}/{total_searches} completed")
    
    successful_searches = len(results)
    print(f"✅ Web searches complete - {successful_searches}/{total_searches} searches successful")
    return results


async def _search_single(item: WebSearchItem, search_number: int) -> str | None:
    """Perform a single search"""
    print(f"🔎 Search #{search_number}: '{item.query}'")
    input_text = f"Search term: {item.query}\nReason for searching: {item.reason}"
    try:
        result = await Runner.run(search_agent, input_text)
        print(f"✅ Search #{search_number} completed successfully")
        return str(result.final_output)
    except Exception as e:
        print(f"❌ Search #{search_number} failed: {str(e)}")
        return None


@function_tool
async def write_report(query: str, search_results: list[str]) -> ReportData:
    """Write a comprehensive report based on search results"""
    print("📝 Analyzing search results and writing comprehensive report...")
    print(f"📊 Processing {len(search_results)} search results")
    
    input_text = f"Original query: {query}\nSummarized search results: {search_results}"
    result = await Runner.run(writer_agent, input_text)
    
    report_data = result.final_output_as(ReportData)
    word_count = len(report_data.markdown_report.split())
    
    print(f"✅ Report writing complete - {word_count} words generated")
    print(f"📋 Report includes: Summary, detailed analysis, and {len(report_data.follow_up_questions)} follow-up questions")
    
    return report_data


@function_tool
async def send_email(report_markdown: str) -> str:
    """Send the research report via email"""
    print("📧 Preparing to send research report via email...")
    
    try:
        result = await Runner.run(email_agent, report_markdown)
        print("✅ Email sent successfully to recipient")
        return "Email sent successfully"
    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")
        return f"Email sending failed: {str(e)}"


# Research agent (without clarifying questions)
research_agent = Agent(
    name="Research Agent",
    instructions="""You are a research agent that conducts comprehensive research.

Your process:
1. Plan searches using plan_searches tool
2. Execute searches using perform_searches tool  
3. Write a comprehensive report using write_report tool
4. Send the report via email using send_email tool

Follow this sequence and provide clear status updates about what you're doing at each step.
Always use the tools in the correct order and wait for each step to complete before proceeding.""",
    tools=[
        plan_searches,
        perform_searches,
        write_report,
        send_email
    ],
    model="gpt-4o-mini"
)


# Separate functions for UI
async def get_clarifying_questions(query: str) -> ClarifyingQuestions:
    """Get clarifying questions for a query"""
    print("❓ Generating clarifying questions to better understand your needs...")
    result = await Runner.run(clarifying_agent, f"User query: {query}")
    questions_count = len(result.final_output.questions)
    print(f"✅ Generated {questions_count} clarifying questions")
    return result.final_output_as(ClarifyingQuestions)


def enhance_query_with_clarifications(original_query: str, clarifications: dict = None) -> str:
    """Enhance the original query with user clarifications"""
    if not clarifications:
        print("📝 Using original query (no clarifications provided)")
        return original_query
    
    clarification_count = len([v for v in clarifications.values() if v and v.strip()])
    print(f"🔧 Enhancing query with {clarification_count} clarifications...")
    
    enhanced_query = f"Original query: {original_query}\n\n"
    enhanced_query += "Additional context and clarifications:\n"
    
    for question, answer in clarifications.items():
        if answer and answer.strip():
            enhanced_query += f"- {question}: {answer}\n"
    
    enhanced_query += f"\n\nPlease conduct research based on the original query with the above clarifications in mind."
    
    print("✅ Query enhancement complete")
    return enhanced_query


async def run_research(query: str):
    """Run research using the research agent with comprehensive logging"""
    trace_id = gen_trace_id()
    with trace("Research trace", trace_id=trace_id):
        yield f"🔗 View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
        yield "🚀 Starting comprehensive research process..."
        yield "🤖 Initializing research agent..."
        
        try:
            # Run the research agent
            result = await Runner.run(research_agent, f"Query: {query}")
            
            # Get any final output
            if hasattr(result, 'final_output'):
                final_result = str(result.final_output)
                yield "🎉 Research process completed successfully!"
                yield "📊 Final Results:"
                yield final_result
            else:
                yield "🎉 Research process completed!"
                yield str(result)
                
        except Exception as e:
            yield f"❌ Research process failed: {str(e)}"
            print(f"Research error: {e}")

