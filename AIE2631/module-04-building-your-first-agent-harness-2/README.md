# Refund Flow

Run the tutorial's customer-facing chat UI locally:

```powershell
uv run streamlit run app.py
```

Set `OPENAI_API_KEY` in `.env` before starting the app. The UI uses the existing
refund agent, `gpt-6-luna`, and the example purchase records in `agent/data.py`.

Try a request such as: `I would like a refund for customer201's laptop_stand`.
