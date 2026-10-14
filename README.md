# insurance-fraud-poc

Personal prototype: transcribe an insurance-claim phone call and flag possible fraud signals with an LLM. **Synthetic or self-made audio only; not affiliated with any company; not a production system.**

## What it does
1. Upload an audio file (`.mp3`, `.wav`, `.m4a`).
2. `gpt-4o-transcribe` transcribes it, labelling customer vs. agent.
3. `gpt-4o-mini` looks for inconsistencies and classifies risk as High / Medium / Low with recommendations.
4. A follow-up chat lets you ask more about the case.

## Stack
Python · FastAPI · OpenAI API · plain HTML/CSS/JS served by FastAPI.

## Run locally
```bash
pip install -r requirements.txt
echo "OPENAI_API_KEY=your_api_key" > .env
python main.py   # http://localhost:8000
```

## Limitations
- Risk labels come from a prompt; no ground truth, no evaluation, no calibration. Do not use them to deny or investigate real claims.
- Transcription errors propagate into the analysis.
- No auth, no storage policy, no tests: demo only.

## License
MIT
