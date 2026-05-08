<div align="center">

# Lorem Ipsum Ai MCP

**MCP server for lorem ipsum ai mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-lorem-ipsum-ai-mcp)](https://pypi.org/project/meok-lorem-ipsum-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Lorem Ipsum Ai MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `generate_paragraphs` | Generate placeholder paragraphs. Styles: lorem (classic), tech, business, nature |
| `generate_sentences` | Generate individual placeholder sentences with configurable length. |
| `generate_words` | Generate a specific number of placeholder words. |
| `generate_structured` | Generate structured placeholder content. Templates: article, email, list, table, |

## Installation

```bash
pip install meok-lorem-ipsum-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "lorem-ipsum-ai": {
      "command": "python",
      "args": ["-m", "meok_lorem_ipsum_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
