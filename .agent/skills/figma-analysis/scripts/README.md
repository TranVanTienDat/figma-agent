# Figma Analysis Scripts - Setup Guide

This directory contains Python scripts for advanced Figma metadata extraction and querying.

## 📋 Prerequisites

- **Python**: Version 3.9 or higher
- **Figma Personal Access Token**: Required for API access

## 🚀 Quick Setup

### Step 1: Install Python Dependencies

```bash
pip install python-dotenv requests
```

Or if you're using `pip3`:

```bash
pip3 install python-dotenv requests
```

### Step 2: Configure Figma Access Token

You have **3 options** to provide your Figma token:

#### Option 1: Project `.env` File (Recommended)

1. Create a `.env` file in your **project root**:

   ```bash
   touch .env
   ```

2. Add your token to `.env`:

   ```env
   FIGMA_ACCESS_TOKEN=your_personal_access_token_here
   ```

3. **Security**: Add `.env` to `.gitignore`:
   ```bash
   echo ".env" >> .gitignore
   ```

#### Option 2: System Environment Variable

**macOS/Linux** (permanent):

```bash
# Add to ~/.zshrc or ~/.bashrc
echo 'export FIGMA_ACCESS_TOKEN="your_token_here"' >> ~/.zshrc
source ~/.zshrc
```

**macOS/Linux** (temporary, current session only):

```bash
export FIGMA_ACCESS_TOKEN="your_token_here"
```

#### Option 3: Command-line Argument

Pass the token directly when running scripts:

```bash
python3 fetch_figma_metadata.py "FIGMA_URL" --token "your_token_here"
```

### Step 3: Get Your Figma Personal Access Token

1. Open Figma and go to **Settings** (click your profile picture)
2. Scroll to **Personal access tokens**
3. Click **Generate new token**
4. Give it a name (e.g., "Figma Agent Tool")
5. **Copy the token** (it only shows once!)
6. Paste it into your `.env` file or environment variable

**Required Scopes:**

- `file_content:read` - For reading file data
- `file_metadata:read` - For file metadata
- `library_content:read` - For components and styles

## 📝 Available Scripts

### 1. `fetch_figma_metadata.py`

Fetches comprehensive metadata from a Figma file.

**Usage:**

```bash
# Using .env token
python3 fetch_figma_metadata.py "https://www.figma.com/design/YOUR_FILE_KEY/..."

# Using command-line token
python3 fetch_figma_metadata.py "YOUR_FILE_KEY" --token "your_token"

# Custom output location
python3 fetch_figma_metadata.py "YOUR_FILE_KEY" --output custom/path/metadata.json
```

**Output:** `figma-agent/common/file-metadata.json` (by default)

### 2. `query_metadata.py`

Efficiently query metadata without loading the entire file.

**Usage:**

```bash
# Get summary
python3 query_metadata.py summary

# Search components
python3 query_metadata.py components --search "button"

# Filter styles by type
python3 query_metadata.py styles --type TEXT

# Get component details
python3 query_metadata.py component "Primary Button"

# Get style details (basic)
python3 query_metadata.py style "Heading 1"

# Get style details (with API fetch for full CSS properties)
python3 query_metadata.py style "Heading 1" --fetch-api
```

### 3. `init-figma-agents.js`

Initializes directory structure for a new page/section.

**Usage:**

```bash
node init-figma-agents.js [page-name] [section-name]

# Example:
node init-figma-agents.js landing-page hero-section
```

## 🔍 Verify Installation

Test if everything is set up correctly:

```bash
# Check Python version
python3 --version  # Should be 3.9+

# Check if packages are installed
pip3 list | grep -E "requests|python-dotenv"

# Check if token is accessible
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Token found!' if os.getenv('FIGMA_ACCESS_TOKEN') else 'Token NOT found')"
```

## ⚠️ Troubleshooting

### "pip: command not found"

Try using `pip3` instead of `pip`.

### "ModuleNotFoundError: No module named 'dotenv'"

Install the package:

```bash
pip3 install python-dotenv
```

### "Access denied" or "403 Forbidden"

- Check if your token is correct
- Verify the Figma file is accessible with your account
- Ensure your token has the required scopes

### Token not being read from `.env`

- Make sure `.env` is in the **project root** (same level as `figma-agent/`)
- Check there are no extra spaces: `FIGMA_ACCESS_TOKEN=token` (not `= token`)
- Verify the file is named exactly `.env` (not `.env.txt`)

## 📚 Additional Resources

- [Figma REST API Documentation](https://developers.figma.com/docs/rest-api/)
- [How to get a Figma Personal Access Token](https://help.figma.com/hc/en-us/articles/8085703771159-Manage-personal-access-tokens)

---

**Need help?** Check the main [INSTALL.md](../../../INSTALL.md) in the project root.
