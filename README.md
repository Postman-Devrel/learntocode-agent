# Coding Teacher Agent with MCP and Langfuse

An AI-powered coding teacher agent that uses the OpenAI Agents SDK with MCP (Model Context Protocol) integration and comprehensive observability through Langfuse.

## Features

- 🤖 **Intelligent Course Recommendations**: Queries coding resources and filters results based on user intent
- 🔌 **MCP Integration**: Connects to Postman MCP servers to access external tools and resources
- 📊 **Full Observability**: Complete tracing and metrics with Langfuse
- 📈 **Automated Evaluations**: Built-in response quality evaluation
- 🎯 **Relevance Scoring**: Automatic scoring of response relevance and completeness

## Prerequisites

- Python 3.11 or higher
- Node.js (for MCP server)
- OpenAI API key
- Langfuse account (free at https://cloud.langfuse.com)

## Installation

### 1. Clone and Setup Environment

```bash
# Navigate to project directory
cd coding-bot

# Create virtual environment with uv
uv venv --python python3.11

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
```

### 2. Configure API Keys

Edit the `.env` file and add your credentials:

```bash
# OpenAI API Key
OPENAI_API_KEY=sk-proj-your-openai-key-here

# Langfuse Configuration
LANGFUSE_PUBLIC_KEY=pk-lf-your-public-key-here
LANGFUSE_SECRET_KEY=sk-lf-your-secret-key-here
LANGFUSE_HOST=https://cloud.langfuse.com
```

**Get your Langfuse keys:**
1. Go to https://cloud.langfuse.com
2. Sign up or log in
3. Create a new project
4. Go to Settings → API Keys
5. Copy your Public Key and Secret Key

## Usage

### Run the Agent

```bash
source .venv/bin/activate
python main.py
```

📊 Langfuse observability enabled

👤 User: What courses do you have on Python?

🔍 Agent is searching for relevant courses...

🤖 Agent Response:
------------------------------------------------------------
Here are the Python courses available:
1. Python Fundamentals - Learn the basics...
2. Advanced Python - Master advanced concepts...
...
------------------------------------------------------------

📈 Evaluating response quality...

✅ Evaluation Metrics:
   • Response Length: 245 characters
   • Contains Python Info: True
   • Has Course Info: True
   • Relevance Score: 100.00%

🔍 View detailed trace at: https://cloud.langfuse.com
```
### Example Output

```
🤖 Coding Teacher Agent initialized!
📊 Langfuse observability enabled

💡 What programming language are you interested in learning?
   (e.g., Python, JavaScript, Java, C++, Ruby, Go, etc.)

👉 Enter language: JavaScript

👤 User: What courses do you have on JavaScript?

🔍 Agent is searching for relevant courses...

🤖 Agent Response:
------------------------------------------------------------
Here are the JavaScript courses available:
1. JavaScript Fundamentals - Learn the basics...
2. Advanced JavaScript - Master advanced concepts...
...
------------------------------------------------------------

📈 Evaluating response quality...

✅ Evaluation Metrics:
   • Response Length: 245 characters
   • Contains JavaScript Info: True
   • Has Course Info: True
   • Relevance Score: 100.00%

🔍 View detailed trace at: https://cloud.langfuse.com
```
============================================================
📊 Langfuse observability enabled
============================================================

👤 User: What courses do you have on Python?

🔍 Agent is searching for relevant courses...

🤖 Agent Response:
------------------------------------------------------------
Here are the Python courses available:
1. Python Fundamentals - Learn the basics...
2. Advanced Python - Master advanced concepts...
...
------------------------------------------------------------

📈 Evaluating response quality...

✅ Evaluation Metrics:
   • Response Length: 245 characters
   • Contains Python Info: True
   • Has Course Info: True
   • Relevance Score: 100.00%

🔍 View detailed trace at: https://cloud.langfuse.com
```

## Langfuse Observability Features

### What Gets Tracked

1. **Execution Traces**
   - Complete agent execution flow
   - Input/output logging
   - Execution time and performance

2. **Metadata**
   - Agent name and configuration
   - Query type and classification
   - Timestamps and user IDs

3. **Evaluation Scores**
   - Response relevance (0-100%)
   - Completeness score
   - Custom quality metrics

4. **Tags**
   - `coding-education`
   - `mcp-integration`
   - Custom tags for filtering

### Viewing Traces in Langfuse

1. Log in to https://cloud.langfuse.com
2. Select your project
3. Navigate to "Traces" tab
4. View detailed execution traces with:
   - Input/output data
   - Latency metrics
   - Token usage (if available)
   - Custom scores and evaluations

### Custom Evaluations

The agent includes built-in evaluation functions:

```python
@observe()
async def evaluate_response(query: str, response: str):
    """Evaluate response quality with custom metrics"""
    # Calculates:
    # - Response length
    # - Keyword presence
    # - Relevance score
    # - Completeness score
```

You can extend this with your own evaluation criteria!

## Customizing the Agent

### Change the Query

Edit `main.py` line 118:

```python
user_query = "What courses do you have on Python?"
# Change to:
user_query = "Show me JavaScript courses"
user_query = "What web development courses are available?"
```

### Add More Evaluation Metrics

Add custom scores in the `evaluate_response` function:

```python
langfuse_context.score_current_trace(
    name="custom_metric",
    value=your_score,
    comment="Your evaluation description"
)
```

### Modify Agent Instructions

Update the agent's behavior in `main.py` line 33:

```python
agent = Agent(
    name="CodingTeacher",
    instructions="Your custom instructions here...",
    mcp_servers=[mcp_server]
)
```

## Project Structure

```
coding-bot/
├── .env                    # API keys and configuration (DO NOT commit!)
├── .gitignore             # Git ignore rules
├── main.py                # Main agent code with Langfuse integration
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .venv/                # Virtual environment
```

## Langfuse Dashboard Features

### Traces Tab
- View all agent executions
- Filter by tags, users, or metadata
- Analyze latency and performance

### Sessions Tab
- Group related conversations
- Track multi-turn interactions

### Scores Tab
- View evaluation metrics
- Analyze quality trends over time

### Analytics
- Token usage tracking
- Cost analysis
- Performance metrics

## Advanced Features

### Adding More MCP Servers

You can connect to multiple MCP servers:

```python
mcp1 = MCPServerStdio(name="server1", params={...})
mcp2 = MCPServerStdio(name="server2", params={...})

agent = Agent(
    name="MyAgent",
    mcp_servers=[mcp1, mcp2]
)
```

### Custom Metadata and Tags

Enhance observability with custom metadata:

```python
langfuse_context.update_current_trace(
    name="custom_trace",
    user_id="user_123",
    metadata={
        "custom_field": "value",
        "environment": "production"
    },
    tags=["custom-tag", "feature-x"]
)
```

### Batch Evaluations

Run evaluations on multiple queries:

```python
queries = [
    "Python courses",
    "JavaScript tutorials",
    "Web development resources"
]

for query in queries:
    result = await run_coding_teacher_agent(query, mcp)
    evaluation = await evaluate_response(query, result.final_output)
```

## Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY not set"**
   - Ensure `.env` file has your OpenAI API key
   - Verify the file is in the project root

2. **"Langfuse authentication failed"**
   - Check your Langfuse public and secret keys
   - Verify the host URL is correct

3. **"MCP server connection failed"**
   - Ensure Node.js is installed
   - Verify the MCP server path is correct
   - Check if the server is running

4. **"Module not found"**
   - Activate virtual environment: `source .venv/bin/activate`
   - Reinstall dependencies: `uv pip install -r requirements.txt`

## Contributing

Feel free to extend this agent with:
- More evaluation metrics
- Additional MCP servers
- Custom scoring functions
- Enhanced error handling

## Resources

- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- [Langfuse Documentation](https://langfuse.com/docs)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [OpenAI API](https://platform.openai.com/docs)

## License

MIT
