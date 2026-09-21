# Suggestive Inquiry: Summaries and Hermetic Lorebook

Chapter-by-chapter summaries of Mary Anne Atwood's *A Suggestive Inquiry into the Hermetic Mystery* (1850), published as an mdBook, with a SillyTavern lorebook extracted from those summaries.

Read the book online: <https://elana-voss.github.io/suggestive-inquiry/>

## Lorebook

The generated SillyTavern World Info file ships in this repo:
[`lorebook/Atwood_Hermetic_Mystery.json`](https://raw.githubusercontent.com/elana-voss/suggestive-inquiry/main/lorebook/Atwood_Hermetic_Mystery.json). Download it and import it in SillyTavern under World Info, Import.

Entries ship in Normal mode and trigger on their keywords. If those terms rarely come up naturally in your chats, switching entries to Vectorized may give better results. Note that this requires embeddings to be set up under Data Bank / Vector Storage.

To regenerate it from the chapter summaries:

```bash
pip install openai pydantic
export LLM_API_KEY="your_api_key"                  # required, any OpenAI-compatible provider
export LLM_BASE_URL="https://nano-gpt.com/api/v1"  # optional, defaults to OpenAI
export LLM_MODEL="z-ai/glm-5.3:thinking"           # optional, must support structured output
python lorebook/generate_lorebook.py
```

The script reads all summaries from `src/` and writes `lorebook/Atwood_Hermetic_Mystery.json`.
