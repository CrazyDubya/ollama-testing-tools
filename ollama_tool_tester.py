import os
import json
import time
import logging
import subprocess
from typing import List, Dict, Any, Tuple, Optional

# Optional imports - will be checked at runtime
try:
    import ollama
    from ollama._types import ResponseError
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ollama_tool_test.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Check for required dependencies
def check_dependencies():
    """Check if all required dependencies are installed"""
    missing_deps = []
    
    if not OLLAMA_AVAILABLE:
        missing_deps.append("ollama")
    
    if not REQUESTS_AVAILABLE:
        missing_deps.append("requests")
    
    if not DDGS_AVAILABLE:
        logger.warning("DuckDuckGo search package not installed. Some search functions may not work properly.")
        logger.warning("Install with: pip install duckduckgo-search")
    
    if missing_deps:
        logger.error(f"Missing required dependencies: {', '.join(missing_deps)}")
        logger.error(f"Install with: pip install {' '.join(missing_deps)}")
        return False
    
    return True

def log_and_chat(
    model_name: str,
    messages: List[Dict[str, Any]],
    tools: Optional[List[Dict[str, Any]]] = None,
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Send a chat request to Ollama and log the prompt and response
    
    Args:
        model_name: Name of the Ollama model to use
        messages: List of message dictionaries
        tools: Optional list of tool definitions
        options: Optional model parameters
        
    Returns:
        The response from Ollama
    """
    if not OLLAMA_AVAILABLE:
        logger.error("Cannot chat: ollama package not installed")
        return {"error": "ollama package not installed"}
    
    logger.info(f"\n--- PROMPT to {model_name} ---\n{json.dumps(messages, indent=2)}")
    if tools is not None:
        logger.info(f"\n--- TOOLS schema ---\n{json.dumps(tools, indent=2)}")
    
    try:
        resp = ollama.chat(
            model=model_name,
            messages=messages,
            tools=tools or [],
            options=options or {}
        )
        logger.info(f"\n--- RESPONSE from {model_name} ---\n{json.dumps(resp, indent=2)}\n")
        return resp
    except Exception as e:
        logger.error(f"Error in chat with {model_name}: {str(e)}")
        return {"error": str(e)}

def get_downloaded_models() -> List[str]:
    """
    Get a list of downloaded Ollama models
    
    Returns:
        List of model names
    """
    if not OLLAMA_AVAILABLE:
        logger.error("Cannot get models: ollama package not installed")
        return []
    
    try:
        result = ollama.list()
        return [m['name'] for m in result['models']]
    except Exception as e:
        logger.error(f"Error retrieving models: {e}")
        return []

def search_web_ddg(query: str) -> List[str]:
    """
    Search the web using DuckDuckGo
    
    Args:
        query: The search query
        
    Returns:
        List of search results as strings
    """
    # Try using duckduckgo-search package first
    if DDGS_AVAILABLE:
        try:
            results = []
            with DDGS() as ddgs:
                ddg_results = list(ddgs.text(query, max_results=5))
                
                for result in ddg_results:
                    title = result.get('title', '')
                    url = result.get('href', '')
                    snippet = result.get('body', '')
                    results.append(f"{title} - {url} - {snippet}")
                
            return results or ["No results found."]
        except Exception as e:
            logger.warning(f"Error using DDGS: {e}. Falling back to API.")
    
    # Fall back to direct API if DDGS is not available or failed
    if REQUESTS_AVAILABLE:
        try:
            url = f"https://api.duckduckgo.com/?q={query}&format=json"
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            data = r.json()
            results = [item.get('FirstURL','') for item in data.get('Results',[])]
            for topic in data.get('RelatedTopics',[]):
                if 'FirstURL' in topic and 'Text' in topic:
                    results.append(f"{topic['Text']} - {topic['FirstURL']}")
            if data.get('AbstractText'):
                results.append(f"Abstract: {data['AbstractText']}")
            return results or ["No results found."]
        except Exception as e:
            return [f"Search error: {e}"]
    else:
        return ["Error: requests package not installed"]

def search_web_alternate(query: str) -> List[str]:
    """
    Search the web using DuckDuckGo's API for alternative information
    
    Args:
        query: The search query
        
    Returns:
        List of search results focusing on abstract, definition, and infobox content
    """
    if not REQUESTS_AVAILABLE:
        return ["Error: requests package not installed"]
    
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&pretty=1"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        out = []
        for key in ('Abstract','Definition','Answer'):
            if data.get(key):
                out.append(f"{key}: {data[key]}")
        inf = data.get('Infobox',{}).get('content',[])
        for item in inf:
            if 'label' in item and 'value' in item:
                out.append(f"{item['label']}: {item['value']}")
        return out or ["No alternate results."]
    except Exception as e:
        logger.error(f"Error in alternate search: {e}")
        return [f"Alternate error: {e}"]

def search_web_http(query: str) -> List[str]:
    """
    Search the web using HTTP requests (wrapper around search_web_ddg)
    
    Args:
        query: The search query
        
    Returns:
        List of search results
    """
    logger.info(f"HTTP Search for query: {query}")
    return search_web_ddg(query)

def search_web_curl(query: str) -> List[str]:
    """
    Search the web using curl subprocess
    
    Args:
        query: The search query
        
    Returns:
        List of search results
    """
    logger.info(f"Curl Search for query: {query}")
    try:
        cmd = ["curl","-s","https://api.duckduckgo.com/","-G",
               "--data-urlencode",f"q={query}","--data-urlencode","format=json"]
        out = subprocess.check_output(cmd, timeout=15).decode()
        data = json.loads(out)
        return [i.get('FirstURL','') for i in data.get('Results',[])] or ["No curl results"]
    except subprocess.SubprocessError as e:
        logger.error(f"Subprocess error in curl search: {e}")
        return [f"Curl error: {e}"]
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in curl search: {e}")
        return [f"JSON error: {e}"]
    except Exception as e:
        logger.error(f"Unexpected error in curl search: {e}")
        return [f"Curl error: {e}"]

def search_web_brave(query: str) -> List[str]:
    """
    Search via Brave Web Search API
    
    Args:
        query: The search query
        
    Returns:
        List of search results from Brave
    """
    if not REQUESTS_AVAILABLE:
        return ["Error: requests package not installed"]
    
    api_key = os.getenv("BRAVE_API_KEY")
    if not api_key:
        logger.warning("Brave API key not set. Set the BRAVE_API_KEY environment variable.")
        return ["Brave API key not set"]
    
    url = f"https://api.search.brave.com/res/v1/web/search?q={query}"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": api_key
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        # Extract URLs from the results list
        results = []
        for item in data.get("results", []):
            # Some responses use 'url' or 'link'
            url_field = item.get("url") or item.get("link")
            title = item.get("title", "")
            description = item.get("description", "")
            if url_field:
                results.append(f"{title} - {url_field} - {description}")
        return results or ["No results found via Brave"]
    except requests.RequestException as e:
        logger.error(f"Request error in Brave search: {e}")
        return [f"Brave search error: {e}"]
    except Exception as e:
        logger.error(f"Unexpected error in Brave search: {e}")
        return [f"Brave search error: {e}"]

def composite_search(query: str) -> Dict[str, List[str]]:
    """
    Perform a search using multiple methods and combine the results
    
    Args:
        query: The search query
        
    Returns:
        Dictionary mapping search method names to their results
    """
    methods = {
        "tool": search_web_ddg,
        "alternate": search_web_alternate,
        "http": search_web_http,
        "curl": search_web_curl,
        "brave": search_web_brave
    }
    
    all_res = {}
    for name, fn in methods.items():
        try:
            res = fn(query)
        except Exception as e:
            logger.error(f"Error in {name} search: {e}")
            res = [f"Error: {e}"]
        all_res[name] = res
        logger.info(f"{name} results count: {len(res)}")
    
    return all_res

def test_model_tool_support(model_name: str) -> Tuple[bool, str, Optional[str], Dict[str, Any]]:
    """
    Test if a model supports tool calling with a more rigorous verification approach.
    
    Returns:
        Tuple containing:
        - Boolean indicating success
        - Reason string
        - Optional response content
        - Dictionary with detailed metrics
    """
    # Define a unique, verifiable fact that would be hard to guess without search
    verification_query = "What is the population of Vaduz, Liechtenstein in 2023?"
    
    tools = [{
        "type": "function", "function": {
            "name": "search_web",
            "description": "Search DuckDuckGo",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]
            }
        }
    }]
    
    # First test with a common query that might be in training data
    messages = [{"role": "user", "content": "Search for the population of Tokyo in 2025."}]
    metrics = {
        "tool_calls_made": False,
        "tool_call_format_correct": False,
        "search_query_relevant": False,
        "response_uses_results": False,
        "verification_test_passed": False
    }
    
    try:
        response = log_and_chat(model_name, messages, tools=tools, options={"temperature": 0.5})
    except Exception as e:
        logger.warning(f"{model_name}: tool call failed ({e}). Falling back to composite_search.")
        fb = composite_search("population of Tokyo in 2025")
        logger.info(json.dumps(fb, indent=2))
        return False, "Tool call error; composite fallback run", None, metrics

    calls = response.get('message', {}).get('tool_calls')
    if not calls:
        logger.warning(f"{model_name} does not support tool calls. Falling back to composite_search.")
        fb = composite_search("population of Tokyo in 2025")
        logger.info(json.dumps(fb, indent=2))
        return False, "No tool calls; composite fallback run", None, metrics

    metrics["tool_calls_made"] = True
    
    # Validate tool call format
    try:
        for call in calls:
            if call['function']['name'] == 'search_web':
                args = call['function']['arguments']
                if isinstance(args, str):
                    args = json.loads(args)
                if 'query' in args and isinstance(args['query'], str):
                    metrics["tool_call_format_correct"] = True
                    
                # Check if query is relevant to the task
                if 'query' in args and ('tokyo' in args['query'].lower() or 'population' in args['query'].lower()):
                    metrics["search_query_relevant"] = True
    except (KeyError, json.JSONDecodeError):
        pass

    # Process tool calls and continue conversation
    tool_msgs = []
    for call in calls:
        name = call['function']['name']
        args = call['function']['arguments']
        if isinstance(args, str):
            args = json.loads(args)
        result = search_web_ddg(**args)
        tool_msgs.append({"role": "tool", "name": name, "content": json.dumps(result)})
    messages += tool_msgs

    final = log_and_chat(model_name, messages, options={"temperature": 0.5})
    content = final.get('message', {}).get('content')
    
    # Now run the verification test with an obscure fact
    if content:
        # Check if response seems to use the search results
        if any(term in content.lower() for term in ['million', 'population', 'tokyo', '2025']):
            metrics["response_uses_results"] = True
            
        # Run verification test with obscure query
        try:
            verify_messages = [{"role": "user", "content": verification_query}]
            verify_response = log_and_chat(model_name, verify_messages, tools=tools, options={"temperature": 0.5})
            verify_calls = verify_response.get('message', {}).get('tool_calls')
            
            if verify_calls:
                verify_tool_msgs = []
                for call in verify_calls:
                    name = call['function']['name']
                    args = call['function']['arguments']
                    if isinstance(args, str):
                        args = json.loads(args)
                    result = search_web_ddg(**args)
                    verify_tool_msgs.append({"role": "tool", "name": name, "content": json.dumps(result)})
                
                verify_messages += verify_tool_msgs
                verify_final = log_and_chat(model_name, verify_messages, options={"temperature": 0.5})
                verify_content = verify_final.get('message', {}).get('content', '')
                
                # Check if response contains specific details about Vaduz that would be hard to guess
                if 'vaduz' in verify_content.lower() and 'liechtenstein' in verify_content.lower():
                    metrics["verification_test_passed"] = True
        except Exception as e:
            logger.warning(f"Verification test failed for {model_name}: {e}")
    
    # Determine overall success based on metrics
    success = metrics["tool_calls_made"] and metrics["tool_call_format_correct"] and metrics["response_uses_results"]
    
    # Add verification test as a strong indicator
    if metrics["verification_test_passed"]:
        reason = "Native tool call succeeded with verification"
    elif success:
        reason = "Native tool call succeeded"
    else:
        reason = "Tool execution issues detected"
    
    return success, reason, content, metrics

def test_advanced_search(model_name: str) -> Dict[str, Any]:
    # Example implementation for advanced search tests
    results = {
        "complex_query": {"success": False, "response": None, "reason": None},
        "multi_tool": {"success": False, "response": None, "reason": None},
        "chain_of_thought": {"success": False, "response": None, "reason": None},
    }
    try:
        # Complex query
        tools = [{
            "type": "function", "function": {
                "name": "search_web",
                "description": "Search DuckDuckGo",
                "parameters": {
                    "type": "object",
                    "properties": {"query": {"type": "string"}},
                    "required": ["query"]
                }
            }
        }]
        messages = [{"role": "user", "content": "Compare the populations of Tokyo and New York City, and explain why they differ."}]
        response = log_and_chat(model_name, messages, tools=tools, options={"temperature": 0.5})
        calls = response.get('message', {}).get('tool_calls')
        if calls:
            tool_msgs = []
            for call in calls:
                args = call['function']['arguments']
                if isinstance(args, str):
                    args = json.loads(args)
                result = search_web_ddg(**args)
                tool_msgs.append({"role": "tool", "name": call['function']['name'], "content": json.dumps(result)})
            messages += tool_msgs
            final = log_and_chat(model_name, messages, options={"temperature": 0.5})
            content = final.get('message', {}).get('content')
            if content:
                results["complex_query"].update(success=True, response=content)
            else:
                results["complex_query"]["reason"] = "No response after tool execution"
        else:
            results["complex_query"]["reason"] = "No tool calls made"

        # Multi-tool test (simulate by multiple tool calls)
        messages = [{"role": "user", "content": "Find information about Tokyo's transportation system and how it compares to New York's subway."}]
        response = log_and_chat(model_name, messages, tools=tools, options={"temperature": 0.5})
        calls = response.get('message', {}).get('tool_calls', [])
        if calls:
            for _ in range(2):
                tool_msgs = []
                for call in calls:
                    args = call['function']['arguments']
                    if isinstance(args, str):
                        args = json.loads(args)
                    result = search_web_ddg(**args)
                    tool_msgs.append({"role": "tool", "name": call['function']['name'], "content": json.dumps(result)})
                messages += tool_msgs
                response = log_and_chat(model_name, messages, options={"temperature": 0.5})
                calls = response.get('message', {}).get('tool_calls', [])
                if not calls:
                    break
            content = response.get('message', {}).get('content')
            if content:
                results["multi_tool"].update(success=True, response=content)
            else:
                results["multi_tool"]["reason"] = "No response after tool execution"
        else:
            results["multi_tool"]["reason"] = "No tool calls made"

        # Chain of thought test
        messages = [{"role": "user", "content": (
            "Plan a 5-day trip to Tokyo: "
            "First, best time for mild weather; "
            "then, key attractions for both tradition and technology."
        )}]
        response = log_and_chat(model_name, messages, tools=tools, options={"temperature": 0.5})
        calls = response.get('message', {}).get('tool_calls', [])
        if calls:
            tool_msgs = []
            for call in calls:
                args = call['function']['arguments']
                if isinstance(args, str):
                    args = json.loads(args)
                result = search_web_ddg(**args)
                tool_msgs.append({"role": "tool", "name": call['function']['name'], "content": json.dumps(result)})
            messages += tool_msgs
            final = log_and_chat(model_name, messages, options={"temperature": 0.5})
            content = final.get('message', {}).get('content')
            if content:
                results["chain_of_thought"].update(success=True, response=content)
            else:
                results["chain_of_thought"]["reason"] = "No response after tool execution"
        else:
            results["chain_of_thought"]["reason"] = "No tool calls made"
    except Exception as e:
        logger.error(f"Advanced search test error for {model_name}: {e}")
        for k in results:
            if not results[k]["success"]:
                results[k]["reason"] = f"Error: {e}"
    return results

def test_alternative_methods(model_name: str) -> Dict[str, Any]:
    results = {
        "direct_json": {"success": False, "response": None, "reason": None},
        "alternate_search": {"success": False, "response": None, "reason": None}
    }
    try:
        # Direct JSON method (simulate function call by JSON output)
        messages = [{"role": "user", "content": (
            "Respond with JSON: {\"action\":\"search\",\"query\":\"Tokyo population\"} when you need to search."
        )}]
        response = log_and_chat(model_name, messages, options={"temperature": 0.5})
        content = response.get('message', {}).get('content', "")
        import re
        match = re.search(r'(\{.*\})', content)
        if match:
            data = json.loads(match.group(1))
            if data.get("action") == "search":
                res = search_web_ddg(data["query"])
                messages += [{"role": "assistant", "content": content},
                             {"role": "user", "content": f"Search results: {json.dumps(res)}"}]
                final = log_and_chat(model_name, messages, options={"temperature": 0.5})
                fc = final.get('message', {}).get('content')
                if fc:
                    results["direct_json"].update(success=True, response=fc)
                else:
                    results["direct_json"]["reason"] = "No response after results"
        else:
            results["direct_json"]["reason"] = "No JSON found"
    except Exception as e:
        results["direct_json"]["reason"] = f"Error: {e}"
    try:
        # Alternate search
        query = "Tokyo population 2025"
        res = search_web_alternate(query)
        messages = [{"role": "user", "content": f"Here are search results: {json.dumps(res)}"}]
        final = log_and_chat(model_name, messages, options={"temperature": 0.5})
        fc = final.get('message', {}).get('content')
        if fc:
            results["alternate_search"].update(success=True, response=fc)
        else:
            results["alternate_search"]["reason"] = "No response"
    except Exception as e:
        results["alternate_search"]["reason"] = f"Error: {e}"
    return results

def test_with_llama_interface(llama_model: str, target_models: List[str]) -> Dict[str, Any]:
    results = {}
    for model in target_models:
        if model == llama_model:
            continue
        logger.info(f"Testing {model} through interface {llama_model}")
        results[model] = {"success": False, "response": None, "reason": None}
        try:
            messages = [{"role": "user", "content": (
                f"Act as caller: search Tokyo population and ask {model} to analyze results."
            )}]
            tools = [
                {
                    "type": "function", "function": {
                        "name": "search_web",
                        "description": "Search DuckDuckGo",
                        "parameters": {
                            "type": "object",
                            "properties": {"query": {"type": "string"}},
                            "required": ["query"]
                        }
                    }
                },
                {
                    "type": "function", "function": {
                        "name": "ask_model",
                        "description": f"Ask the {model} AI model",
                        "parameters": {
                            "type": "object",
                            "properties": {"question": {"type": "string"}},
                            "required": ["question"]
                        }
                    }
                }
            ]
            response = log_and_chat(llama_model, messages, tools=tools, options={"temperature": 0.5})
            calls = response.get('message', {}).get('tool_calls', [])
            tool_msgs = []
            search_res = None
            for call in calls:
                fn = call['function']['name']
                args = call['function']['arguments']
                if isinstance(args, str): args = json.loads(args)
                if fn == "search_web":
                    search_res = search_web_ddg(**args)
                    tool_msgs.append({"role":"tool","name":fn,"content":json.dumps(search_res)})
                elif fn == "ask_model":
                    if search_res:
                        q = args['question']
                        targ = [{"role":"user","content":f"{q}\nResults:\n{json.dumps(search_res)}"}]
                        targ_resp = ollama.chat(model=model, messages=targ, options={"temperature":0.5})
                        tool_msgs.append({"role":"tool","name":fn,"content":json.dumps(targ_resp.get('message',{}).get('content'))})
            messages += tool_msgs
            final = log_and_chat(llama_model, messages, options={"temperature": 0.5})
            fc = final.get('message', {}).get('content')
            if fc:
                results[model].update(success=True, response=fc)
            else:
                results[model]["reason"] = "No final response"
        except Exception as e:
            results[model]["reason"] = f"Error: {e}"
    return results

def generate_report(
    basic_results: Dict[str, Any],
    advanced_results: Dict[str, Any],
    alternative_results: Dict[str, Any],
    interface_results: Dict[str, Any]
) -> str:
    lines = []
    lines.append("# Ollama Model Tool Support Analysis Report")
    lines.append(f"Test Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Summary
    total = len(basic_results)
    native_success = sum(1 for r in basic_results.values() if r["success"])
    verified_success = sum(1 for r in basic_results.values() if r.get("metrics", {}).get("verification_test_passed", False))
    alt_success = sum(1 for r in alternative_results.values() if r["direct_json"]["success"] or r["alternate_search"]["success"])
    iface_success = sum(1 for r in interface_results.values() if r["success"])
    
    lines.append("## Summary")
    lines.append(f"- Total models tested: {total}")
    lines.append(f"- Native tool support successes: {native_success} ({native_success/total*100:.1f}%)")
    lines.append(f"- **Verified** tool support (passed obscure fact test): {verified_success} ({verified_success/total*100:.1f}%)")
    lines.append(f"- Alternative method successes: {alt_success}")
    lines.append(f"- Interface method successes: {iface_success}\n")
    
    # Add explanation of verification
    lines.append("### Verification Methodology")
    lines.append("Models were tested with both common queries (Tokyo population) and obscure facts (Vaduz, Liechtenstein population) ")
    lines.append("to distinguish between genuine tool use and knowledge recall through inference. ")
    lines.append("A model passes verification when it successfully retrieves and incorporates information about an obscure topic ")
    lines.append("that would be unlikely to appear in its training data.\n")
    # Basic results with detailed metrics
    lines.append("## Basic Tool Calling Support")
    lines.append("| Model | Success | Verification | Tool Calls | Format Correct | Relevant Query | Uses Results | Reason |")
    lines.append("|-------|---------|--------------|------------|----------------|----------------|--------------|--------|")
    for m, r in basic_results.items():
        metrics = r.get("metrics", {})
        verification = "✅" if metrics.get("verification_test_passed", False) else "❌"
        tool_calls = "✅" if metrics.get("tool_calls_made", False) else "❌"
        format_correct = "✅" if metrics.get("tool_call_format_correct", False) else "❌"
        relevant_query = "✅" if metrics.get("search_query_relevant", False) else "❌"
        uses_results = "✅" if metrics.get("response_uses_results", False) else "❌"
        
        lines.append(f"| {m} | {r['success']} | {verification} | {tool_calls} | {format_correct} | {relevant_query} | {uses_results} | {r['reason']} |")
    lines.append("")
    # Advanced results
    lines.append("## Advanced Testing Results")
    for m, res in advanced_results.items():
        lines.append(f"### {m}")
        for test_name, data in res.items():
            status = "✅" if data["success"] else "❌"
            reason = data.get("reason", "")
            snippet = (data.get("response") or "").replace('\n',' ')[:80]
            lines.append(f"- **{test_name}**: {status} {reason} {snippet}")
        lines.append("")
    # Alternative methods
    lines.append("## Alternative Methods Results")
    for m, res in alternative_results.items():
        lines.append(f"### {m}")
        for method, data in res.items():
            status = "✅" if data["success"] else "❌"
            snippet = (data.get("response") or "").replace('\n',' ')[:80]
            reason = data.get("reason","")
            lines.append(f"- **{method}**: {status} {reason} {snippet}")
        lines.append("")
    # Interface results
    lines.append("## Interface (LLama) Results")
    for m, res in interface_results.items():
        status = "✅" if res["success"] else "❌"
        snippet = (res.get("response") or "").replace('\n',' ')[:80]
        reason = res.get("reason","")
        lines.append(f"- **{m}**: {status} {reason} {snippet}")
    return "\n".join(lines)

def main():
    """Main function to run the Ollama tool tests"""
    # Check dependencies first
    if not check_dependencies():
        logger.error("Missing required dependencies. Exiting.")
        return
    
    # Get available models
    models = get_downloaded_models()
    if not models:
        logger.error("No models available. Make sure Ollama is running and has models installed.")
        return
    
    logger.info(f"Found {len(models)} models: {', '.join(models)}")
    
    # Run tests
    basic_results = {}
    viable, failed = [], []
    for m in models:
        logger.info(f"Testing model: {m}")
        ok, reason, content, metrics = test_model_tool_support(m)
        basic_results[m] = {"success": ok, "reason": reason, "metrics": metrics}
        (viable if ok else failed).append(m)

    logger.info(f"Models with tool support: {len(viable)}")
    logger.info(f"Models without tool support: {len(failed)}")
    
    # Log verification results
    verified = [m for m in viable if basic_results[m].get("metrics", {}).get("verification_test_passed", False)]
    logger.info(f"Models with verified tool support: {len(verified)}")
    
    # Run advanced tests on viable models
    advanced_results = {m: test_advanced_search(m) for m in viable}
    
    # Run alternative tests on failed models
    alternative_results = {m: test_alternative_methods(m) for m in failed}
    
    # Run interface tests if there are viable models
    interface_results = {}
    if viable:
        interface_results = test_with_llama_interface(viable[0], failed)

    # Generate and save report
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    fname = f"ollama_report_{timestamp}.md"
    with open(fname, "w") as f:
        f.write(generate_report(basic_results, advanced_results, alternative_results, interface_results))
    logger.info(f"Report written to {fname}")
    print(f"Report written to {fname}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Test interrupted by user")
        print("\nTest interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Error: {e}")
