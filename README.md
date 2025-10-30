# Reliable Agent Blueprint with Postman & Langfuse
A started AI agent to share  resources (videos, tutorials, units etc) for someone looking to learn how to code.  This app is designed to demonstrate the key requirements on how to make a reliable AI agent that solves common production requirements.


## Features

- 🤖 **Intelligent Course Recommendations**: Queries coding resources and filters results based on user intent
- 🔌 **MCP Integration**: Connects to Postman MCP servers to access external tools and resources
- 🎛️ **API Governance**: Uses Postman Role Based Access Controls (RBAC) to protect from data leakage into public LLMs
- ⚙️ **API Availability & Discovery**: API testing, documentation, monitoring, and collections via Postman to ensure API availability and easy of discovery within an organization. 
- 📊 **Full Observability**: Complete tracing, metrics, and token cost with Langfuse
- 📈 **Evaluations & Consistency**: Built-in response quality evaluation
- 🎯 **Relevance Scoring**: Automatic scoring of response relevance and completeness, including LLM-as-a-Judge. 


## Prerequisites

- Python 3.11 or higher
- Node.js (for MCP server)
- OpenAI API key 
- Langfuse account (free at https://cloud.langfuse.com)
- Postman account (free at https://identity.getpostman.com/signup?utm_source=cookbook)

## Postman Setup


### Add Coding Resources API Collection
Within your workspace, tap agent mode and enter the following prompt:

`"Create an API collection from https://api.sampleapis.com/codingresources/"`

Once this is complete you should now see a new collection in your workspace. If you tap in there will be Get Coding Resources GET request. This is the endpoint our AI agent will use to gather lessons and learning resources. In a full app, you may have multiple API Collections and endpoints to learning platforms, free website courses etc. 

### Create Unit Tests & Documentation
To ensure your agent works consistently, the APIs you rely on must be available and work as expected. Adding unit tests and documententation ensure they function as designed, and if anything changes, you know about it. 

Within your workspace, tap agent mode and enter the following prompt:

`"Add unit tests and documentation to the Coding Resources API Collection"`

Once completed, you can tap on the Get Coding Resources GET request, then the Scripts tab to see the generated API test. Make sure they all run and pass correctly. 

![Unit tests](images/unit-tests.gif)

### Add Monitoring & Alerts
The last thing you need to do in your Postman environment is add monitoring and alerts to your API collection to ensure quality and availability of the API services. 

Within your workspace, tap agent model and enter the following prompt:

`"add monitoring to the Coding Resources API and set an alert if the monitor detects my collection is unhealthy. I want it to run every 10 minutes, and send alerts to your@email.com"`

Once completed, tap monitors on the left navigation to see your dashboard. 

![Monitors](images/monitors.png)

### Postman skills
The list of activities above provide a solid baseline to ensure API health and reliability. Postman recently launched skills. Skills allow developers to leverage Postman best practices via a slash command in a prompt. Check out the [docs for detailed examples.](https://learning.postman.com/docs/agent-mode/overview/#skills). 

![Postman Skills](images/postman-skills.png)

### MCP Server
Once you have the Postman workspace created and API healthchecks in place, create an MCP server from the API Collection.

Within your workspace, tap agent model and enter the following prompt:

`"Create an MCP server from this collection"`

Once completed, it it create a local MCP server in ~/Postman/mcp-servers. We will use this shortly. 

![MCP Server](images/am-mcp.png)


### Role Based Security
Postman makes it easy to manage who has access to change your APIs and collections via role-based security. For example, let's say you wanted to restrict which team members can edit the Coding Resources API Collection, you can specifiy this as a [Collection role.](https://learning.postman.com/docs/administration/roles-and-permissions/#element-based-roles) 


### 1. Clone and Setup Environment
With the MCP server created and downloaded locally, create the agent. Clone the repo and follow the instructions below. 

```bash
# Navigate to project directory
cd learntocode-agent

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

### 3. Update with MCP server
Open main.py and scroll till you find the MCP call. Change the absolute path to match where you downloaded the MCP server. 
```python

mcp = MCPServerStdio(
        name="postman-mcp",
        params={
            "command": "node",
            "args": ["/Users/your-home-dir/Postman/mcp-servers/mcp-coding-resources-mcp-server-ML5GOBMY/mcpServer.js"]
        }
    )

```

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

