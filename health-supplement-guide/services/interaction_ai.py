import json

from config import Config


def analyze_with_ai(substance_list):
    """Use Gemini 1.5 Flash to analyze supplement interactions.

    Args:
        substance_list: List of supplement/substance names.

    Returns:
        dict with keys: available (bool), message (str), results (list).
    """
    api_key = Config.GEMINI_API_KEY
    model_name = Config.GEMINI_MODEL

    if not api_key:
        return {
            "available": False,
            "message": "مفتاح Gemini API غير مُعدّ. يُرجى التحقق من الإعدادات.",
            "results": [],
        }

    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        substances = "، ".join(substance_list)
        prompt = f"""
أنت صيدلي سريري ذكي. قم بتحليل القائمة التالية من المكملات الغذائية والأدوية لاكتشاف التفاعلات الدوائية والموانع والاستشارات الصحية المحتملة.

المكملات/Aldawaa: {substances}

لكل تفاعل تم اكتشافه، قدم:
- substance_a (اسم العنصر الأول بالعربية)
- substance_b (اسم العنصر الثاني بالعربية)
- severity (شدة التفاعل: high/moderate/low)
- description (وصف التفاعل بالعربية)
- recommendation (التوصية بالعربية)

أرجع النتيجة كمصفوفة JSON من الكائنات بالمفاتيح: substance_a, substance_b, severity, description, recommendation.
إذا لم يتم اكتشاف أي تفاعلات، أرجع مصفوفة فارغة [].
أرجع JSON صالح فقط، بدون أي نص إضافي أو كود markdown.
"""

        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )

        content = response.text.strip()

        if content.startswith("```"):
            content = content.split("\n", 1)[1]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

        results = json.loads(content)

        return {
            "available": True,
            "message": f"تم التحليل بنجاح باستخدام {model_name}.",
            "results": results if isinstance(results, list) else [],
        }

    except ImportError:
        return {
            "available": False,
            "message": "مكتبة google-genai غير مثبتة. قم بتشغيل: pip install google-genai",
            "results": [],
        }
    except Exception as e:
        return {
            "available": False,
            "message": f"خطأ في التحليل بالذكاء الاصطناعي: {str(e)}",
            "results": [],
        }
