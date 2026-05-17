import os
import json
from typing import Optional
from app.models.calculation import ChatRequest

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


SYSTEM_PROMPT = open(
    os.path.join(os.path.dirname(__file__), "../prompts/system_prompt.txt"), "r"
).read()


async def get_ai_response(request: ChatRequest) -> str:
    """
    Get an AI response using Anthropic Claude (primary) or OpenAI (fallback).
    """
    context_str = ""
    if request.context:
        context_str = f"\n\nCurrent Calculation Context:\n{json.dumps(request.context, indent=2)}"

    system = SYSTEM_PROMPT + context_str

    # Build conversation history
    history = [
        {"role": m.role, "content": m.content}
        for m in request.history[-8:]  # Last 8 messages
    ]

    # Try Anthropic first
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if ANTHROPIC_AVAILABLE and anthropic_key:
        client = anthropic.Anthropic(api_key=anthropic_key)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            system=system,
            messages=history + [{"role": "user", "content": request.message}],
        )
        return response.content[0].text

    # Fallback to OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if OPENAI_AVAILABLE and openai_key:
        client = openai.AsyncOpenAI(api_key=openai_key)
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=600,
            messages=[{"role": "system", "content": system}] + history + [
                {"role": "user", "content": request.message}
            ],
        )
        return response.choices[0].message.content

    # Fallback: rule-based responses
    return _rule_based_response(request.message, request.context)


def _rule_based_response(message: str, context: Optional[dict]) -> str:
    """Simple rule-based fallback when no AI API is configured."""
    msg = message.lower()
    if "benchmark" in msg:
        return (
            "Industry benchmarks (India, 2024): Product companies average 28–35 hires/recruiter/year. "
            "Consulting firms average 50–65 hires/recruiter/year. GCCs average 30–40. "
            "Source: Naukri Hiring Index."
        )
    if "dropout" in msg or "attrition" in msg:
        return (
            "Dropout ratio accounts for offer declines and no-shows. A 25% dropout means "
            "you need to make 800 offers to onboard 600 people. IT sector average dropout is 20–30%. "
            "Niche AI roles can see 35–45% dropout due to counter-offers."
        )
    if "cost" in msg or "budget" in msg:
        return (
            "TA team cost typically runs 8–15% of total annual recruitment budget. "
            "For product companies, avg recruiter CTC is ₹12–18L/year. "
            "Consulting firms average ₹8–12L/year."
        )
    if "timeline" in msg:
        return (
            "Hiring timelines depend heavily on role complexity. Product/AI roles average 45–90 days. "
            "Volume consulting hiring averages 20–30 days. "
            "Increasing recruiter count by 20% typically reduces timeline by 15–18%."
        )
    return (
        "I can help you analyze your TA structure, understand benchmarks, or optimize your hiring plan. "
        "Please configure an API key (ANTHROPIC_API_KEY or OPENAI_API_KEY) in your backend .env for full AI responses."
    )
