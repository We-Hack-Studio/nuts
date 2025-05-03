# Cursor Custom Modes Format Documentation

This document describes the format for defining custom modes in the `.cursor/modes.json` file.

If you generate a file similar to docs/custom-agents.md either externally, internally with the AI or manually - you can then ask the cursor agent to generate a new or update an existing .cursor/mode.json. In the future when official support comes out for a json file - it will be easy to then ask the agent to convert your file - or if you had already created all of the agents described in the file through the gui - the file will be automatically created by cursor when you upgrade to the version that has the json file support - most likely in your user folder/.cursor (configs that apply across all projects in cursor)!

## File Structure

The `modes.json` file contains a JSON object with two main fields:

- `modes`: An array of mode configuration objects

## Mode Configuration Schema

```json
{
  "commentFromBMad": "string",
  "modes": [
    {
      "name": "string",
      "description": "string",
      "comment": "string",
      "model": "string",
      "customPrompt": "string",
      "allowedCursorTools": "string[]",
      "allowedMcpTools": "string[]",
      "autoApplyEdits": "boolean",
      "autoRun": "boolean",
      "autoFixErrors": "boolean"
    }
  ]
}
```

## Field Descriptions

### Root Level Fields

| Field   | Type  | Description                         |
| ------- | ----- | ----------------------------------- |
| `modes` | array | Array of mode configuration objects |

### Mode Configuration Fields

| Field                | Type              | Required | Default | Description                                                                                                                                    |
| -------------------- | ----------------- | -------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`               | string            | Yes      | -       | Display in tab Short CapCase but easy to remember. The full name will be in the description field - such as PicardPm or RikerArch, or FooFEDev |
| `description`        | string            | Yes      | -       | Not used in actual configuration, but easy for user to know what character it is briefly                                                       |
| `comment`            | string            | No       | -       | Reference note for documentation purposes                                                                                                      |
| `model`              | string            | Yes      | -       | The AI model to use for this mode                                                                                                              |
| `customPrompt`       | string            | No       | -       | Detailed prompt defining the agent's persona and behavior                                                                                      |
| `allowedCursorTools` | string[] or "all" | No       | -       | Array of Cursor tools this mode can access, or "all" to grant access to all available Cursor tools                                             |
| `allowedMcpTools`    | string[] or "all" | No       | -       | Array or comma-separated list of allowed MCP tool names, or "all" to grant access to all available MCP tools                                   |
| `autoApplyEdits`     | boolean           | No       | false   | Automatically apply edits without confirmation                                                                                                 |
| `autoRun`            | boolean           | No       | false   | Automatically run commands without confirmation                                                                                                |
| `autoFixErrors`      | boolean           | No       | false   | Automatically attempt to fix detected errors                                                                                                   |

## Supported Models

The following models are currently supported for the `model` field:

- `claude-3-opus`
- `claude-3.5-haiku`
- `claude-3.5-sonnet`
- `claude-3.7-sonnet`
- `claude-3.7-sonnet-max`
- `cursor-fast`
- `cursor-small`
- `deepseek-r1`
- `deepseek-v3`
- `gemini-2.0-flash`
- `gemini-2.0-flash-exp`
- `gemini-2.0-pro-exp`
- `gemini-2.5-pro-exp-03-25`
- `gemini-2.5-pro-max`
- `gemini-exp-1206`
- `gpt-3.5-turbo`
- `gpt-4`
- `gpt-4-turbo-2024-04-09`
- `gpt-4.5-preview`
- `gpt-4o`
- `gpt-4o-mini`
- `grok-2`
- `o1`
- `o1-mini`
- `o1-preview`
- `o3-mini`

Note: Additional models may be supported in the future as Cursor expands its model integrations.

## Supported Cursor Tools

The following tools can be specified in the `allowedCursorTools` array:

### Search Tools

- `codebase_search` - Semantic search across the codebase
- `web` - Web search capabilities
- `grep` - Pattern-based code search
- `list_directory` - List contents of directories
- `search_files` - Search for files by name
- `read_file` - Read file contents
- `fetch_rules` - Fetch custom codebase rules

### Edit Tools

- `edit_file` - Edit file contents
- `edit_and_reapply` - Edit with smart reapplication
- `delete_file` - Delete files

### Run Tools

- `terminal` - Execute terminal commands

## Example Configuration

```json
{
  "commentFromBMad": "Example custom mode configuration",
  "modes": [
    {
      "name": "PiPyDev",
      "description": "Pirate Python Dev",
      "comment": "Specialized mode for Python development with auto-fixes enabled",
      "model": "claude-3.5-sonnet",
      "customPrompt": "You are an expert Python developer that always speaks like a pirate in conversation, but never injects the personality into files being created or updated...",
      "allowedCursorTools": [
        "codebase_search",
        "web",
        "grep",
        "list_directory",
        "search_files",
        "read_file",
        "fetch_rules",
        "edit_file",
        "edit_and_reapply",
        "delete_file",
        "terminal"
      ],
      "allowedMcpTools": ["python_linter", "python_formatter", "pytest"],
      "autoApplyEdits": true,
      "autoRun": false,
      "autoFixErrors": true
    }
  ]
}
```

## MCP Tools

The `allowedMcpTools` field can contain any custom tool names that have been configured in your MCP configuration. These should match the exact names given to the tools in your MCP setup.

## Best Practices

1. Choose descriptive names for your custom modes
2. Provide detailed custom prompts that clearly define the agent's role
3. Limit tool access to only what's necessary for the mode's purpose
4. Document any special requirements or dependencies in the comment field
5. Use consistent naming conventions for MCP tools 🔧
