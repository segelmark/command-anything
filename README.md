# Command Anything

Command Anything lets you create command-line commands using plain English. Instead of remembering complex syntax or flags, just describe what you want to do, and let AI figure out the details.

## Why Use Command Anything?

- **Focus on intent**: Tell it what you want to accomplish, not how to do it
- **Natural language**: No need to memorize command syntax or man pages
- **Learn as you go**: See the actual commands that match your intentions
- **Safe execution**: Preview commands before running them

## Quick Start

1. Save the script as `command-anything` in your preferred location
2. Make it executable:
```bash
chmod +x command-anything
```

3. Set up an alias for easy access. Add this line to your shell config file:

For Bash (`~/.bashrc` or `~/.bash_profile`):
```bash
alias llm="path/to/command-anything"
```

For Zsh (`~/.zshrc`):
```bash
alias llm="path/to/command-anything"
```

After adding the alias:
```bash
source ~/.bashrc  # or ~/.zshrc if using Zsh
```

Now you can use `llm` from anywhere!

## How to Use

Basic usage:
```bash
ca "your request in plain english"
```

Options:
- `-m MODEL`: Choose a different AI model (default: gpt-4o)
- `-l LANGUAGE`: Specify output language (default: python)
- `-p PARAMETERS`: Add extra context or parameters

For each command:
1. Describe what you want to do
2. Review the explanation and generated command
3. Confirm if you want to run it

## Tips for Best Results

- Be specific about what you want to accomplish
- Include relevant details like file types, locations, or conditions
- Review commands before executing, especially for system-changing operations
- Use parameters to provide additional context when needed

## Safety Notes

- Always review generated commands before execution
- The tool will show you what it plans to do and ask for confirmation
- For system-changing operations, consider running with `--dry-run` first (just add this to your request)

## Examples

Find large files in your system:
```bash
llm "find files larger than 1GB in my home directory"
```

Manage processes:
```bash
llm "kill all processes using more than 2GB of RAM"
```

File operations:
```bash
llm "rename all jpg files in current folder to include today's date"
```

System maintenance:
```bash
llm "clean up old docker images and containers"
```

Complex tasks:
```bash
llm "find all Python files modified in the last week and count their lines of code"
```

## Requirements

- Python 3.x
- OpenAI API key (set in your environment)
- Required Python packages: `openai`, `pydantic`

## Installation Troubleshooting

If you get a "command not found" error:
1. Make sure the script is executable (`chmod +x command-anything`)
2. Verify your alias is set up correctly:
```bash
which llm
```
3. Check if the OpenAI API key is set:
```bash
echo $OPENAI_API_KEY
```



