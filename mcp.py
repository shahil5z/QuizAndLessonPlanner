# mcp.py — Mock implementation for McpServer, Tool, and Resource

from functools import wraps  # Imported for decorators, but not used in this mock file

class McpServer:
    def __init__(self, name="", version="", description=""):
        # Initialize server metadata
        self.name = name
        self.version = version
        self.description = description

        # Dictionaries to hold registered tools and resources
        self.tools = {}
        self.resources = {}

    def tool(self, name="", description="", parameters=None):
        """
        Decorator to register a tool function.
        Saves function metadata under the given tool name.
        """
        def decorator(func):
            self.tools[name] = {
                "function": func,  # Actual function implementation
                "description": description,  # Description for documentation
                "parameters": parameters or {}  # Input parameters expected
            }
            print(f"[Tool Registered] {name}")  # Log tool registration
            return func  # Return the original function
        return decorator

    def resource(self, name="", description="", parameters=None):
        """
        Decorator to register a resource function.
        Works similarly to the `tool` decorator.
        """
        def decorator(func):
            self.resources[name] = {
                "function": func,  # Actual function implementation
                "description": description,  # Description for documentation
                "parameters": parameters or {}  # Input parameters expected
            }
            print(f"[Resource Registered] {name}")  # Log resource registration
            return func  # Return the original function
        return decorator

    def run(self, host="0.0.0.0", port=5000):
        """
        Mock server run method — prints the registered tools and resources.
        Emulates server startup (does not serve actual HTTP requests).
        """
        print(f"📡 MCP Server '{self.name}' running on {host}:{port}")
        print("🔧 Tools:")
        for name in self.tools:
            print(f" - {name}")  # List registered tools
        print("📚 Resources:")
        for name in self.resources:
            print(f" - {name}")  # List registered resources
        print("✅ Server Ready (Mock Mode)")  # Final status message

# These aliases are provided to prevent import errors from 'from mcp import Tool, Resource'
Tool = object
Resource = object
