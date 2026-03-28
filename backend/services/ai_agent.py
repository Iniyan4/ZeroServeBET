import openai
import json


def analyze_user(data):
    prompt = f"""
You are an AI system analyzing user reliability.

User Data:
- Trust score: {data['trust_score']}
- Violations: {data['violations']}
- No-shows: {data['no_show']}
- Complaints: {data['complaints']}

Return ONLY valid JSON in this exact format:

{{
  "summary": "short explanation of user behavior",
  "risk_level": "low | medium | high | critical",
  "recommendation": "approve | review | restrict"
}}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        content = response['choices'][0]['message']['content']

        # 🔥 Parse JSON safely
        parsed = json.loads(content)

        return parsed

    except Exception as e:
        # 🔒 Fallback (VERY IMPORTANT)
        return {
            "summary": f"User has trust score {data['trust_score']} with {data['violations']} violations",
            "risk_level": "high" if data['trust_score'] < 50 else "medium",
            "recommendation": "review"
        }