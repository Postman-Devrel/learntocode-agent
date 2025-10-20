import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

# Load environment variables from .env file
load_dotenv()

# Initialize Langfuse observability
from langfuse import observe, get_client

LANGFUSE_ENABLED = True

@observe(as_type="generation")
async def run_coding_teacher_agent(user_query: str, mcp_server):
    """
    Run the coding teacher agent with usage and cost tracking.
    
    Args:
        user_query: The user's question about courses
        mcp_server: The MCP server connection
    """
    langfuse = get_client()
    
    # Create agent with MCP tools
    agent = Agent(
        name="CodingTeacher",
        instructions="You are a helpful assistant designed to help people learn to code. When asked about courses, use the get_coding_resources tool to retrieve available courses and filter them to show only the most relevant ones based on the user's query.",
        mcp_servers=[mcp_server]
    )
    
    # Update generation with model info
    langfuse.update_current_generation(
        model="gpt-4o",  # Specify the model being used
        input=user_query,
        metadata={"agent": "CodingTeacher"}
    )
    
    # Run the agent
    print("🔍 Agent is searching for relevant courses...\n")
    result = await Runner.run(agent, user_query)
    
    # Update with output and usage if available
    langfuse.update_current_generation(
        output=result.final_output
    )
    
    # Note: The OpenAI Agents SDK may not directly expose token usage
    # Langfuse will automatically infer usage and cost based on the model (gpt-4o)
    # If usage data becomes available in future SDK versions, we can add:
    # usage_details={"input": tokens_in, "output": tokens_out}
    
    return result

@observe()
def evaluate_response(query: str, response: str, language: str):
    """
    Evaluate the quality of the agent's response.
    
    Args:
        query: The user's query
        response: The agent's response
        language: The programming language being queried
    """
    # Basic evaluation metrics
    metrics = {
        "response_length": len(response),
        "contains_language": language.lower() in response.lower() or language in response,
        "has_courses": "course" in response.lower(),
        "relevance_score": 0.0
    }
    
    # Calculate a simple relevance score using dynamic language
    query_keywords = [language.lower(), "course", "learn", "coding"]
    matches = sum(1 for keyword in query_keywords if keyword.lower() in response.lower())
    metrics["relevance_score"] = matches / len(query_keywords)
    
    return metrics

@observe()
async def main():
    """Main function with optional Langfuse observability."""
    
    # Start the Postman MCP server subprocess
    mcp = MCPServerStdio(
        name="postman-mcp",
        params={
            "command": "node",
            "args": ["/Users/quintonwall/Postman/mcp-servers/mcp-coding-resources-mcp-server-ML5GOBMY/mcpServer.js"]
        }
    )
    
    # Connect to the MCP server
    await mcp.connect()
    
    try:
        print("\n🤖 Coding Teacher Agent initialized!")
        print("=" * 60)
        if LANGFUSE_ENABLED:
            print("📊 Langfuse observability: ENABLED")
        else:
            print("📊 Langfuse observability: DISABLED")
        print("=" * 60)
        
        # Ask user for programming language
        print("\n💡 What programming language are you interested in learning?")
        print("   (e.g., Python, JavaScript, Java, C++, Ruby, Go, etc.)")
        language = input("\n👉 Enter language: ").strip()
        
        # Default to Python if no input provided
        if not language:
            language = "Python"
            print(f"   Using default: {language}")
        
        # Create user query with the specified language
        user_query = f"What courses do you have on {language}?"
        print(f"\n👤 User: {user_query}\n")
        
        # Run the agent (automatically traced by @observe decorator)
        result = await run_coding_teacher_agent(user_query, mcp)
        
        # Display the response
        print("🤖 Agent Response:")
        print("-" * 60)
        print(result.final_output)
        print("-" * 60)
        
        # Evaluate the response (automatically traced by @observe decorator)
        print("\n📈 Evaluating response quality...")
        evaluation = evaluate_response(user_query, result.final_output, language)
        
        print(f"\n✅ Evaluation Metrics:")
        print(f"   • Response Length: {evaluation['response_length']} characters")
        print(f"   • Contains {language} Info: {evaluation['contains_language']}")
        print(f"   • Has Course Info: {evaluation['has_courses']}")
        print(f"   • Relevance Score: {evaluation['relevance_score']:.2%}")
        
        # Flush Langfuse to ensure all traces are sent
        if LANGFUSE_ENABLED:
            langfuse_client = get_client()
            langfuse_client.flush()
            print("\n📊 Traces logged to Langfuse")
            print(f"🔍 View at: {os.getenv('LANGFUSE_HOST', 'https://us.cloud.langfuse.com')}")
        
    finally:
        # Cleanup
        await mcp.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
