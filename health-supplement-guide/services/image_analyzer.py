import base64
import json
import os

from config import Config


def analyze_medicine_image(image_bytes, filename=""):
    """Analyze a medicine image using Gemini 1.5 Flash.

    Args:
        image_bytes: Raw bytes of the uploaded image.
        filename: Original filename (used to determine MIME type).

    Returns:
        dict with keys: available (bool), message (str), result (dict or None).
    """
    api_key = Config.GEMINI_API_KEY
    model_name = Config.GEMINI_MODEL

    if not api_key:
        return {
            "available": False,
            "message": "مفتاح Gemini API غير مُعدّ. يرجى التحقق من الإعدادات.",
            "result": None,
        }

    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        ext = os.path.splitext(filename)[1].lower() if filename else ".jpg"
        mime_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp",
            ".bmp": "image/bmp",
        }
        mime_type = mime_map.get(ext, "image/jpeg")

        image_data = base64.b64encode(image_bytes).decode("utf-8")

        prompt = """
أنت طبيب صيدلي ذكي متخصص في تحليل الأدوية والمكملات الغذائية. قم بتحليل الصورة المرفقة لعلبة الدواء أو الشريط وقدم التحليل التالي باللغة العربية:

1. **المعلومات الأساسية:**
   - الاسم التجاري للدواء
   - الاسم العلمي (المادة الفعالة)
   - الشركة المصنعة وبلد الصنع (إن ظهر)

2. **دواعي الاستعمال:**
   - اشرح بوضوح لماذا يُستخدم هذا الدواء

3. **الجرعة والطريقة:**
   - الجرعة الموصى بها
   - طريقة التناول (قبل أو بعد الطعام)

4. **التحذيراتandestWarnings:**
   - تحذيرات خاصة بالحوامل والمرضعات
   - تحذيرات لمرضى الضغط
   - تحذيرات لمرضى السكري
   - تحذيرات لمرضى الكلى والكبد
   - أي حالات مزمنة أخرى

5. **التأثيرات الجانبية:**
   - الأثر الجانبية الشائعة
   - الأثر الجانبية النادرة لكن الخطيرة

6. **نصائح التخزين وصلاحية:**
   - طريقة التخزين المناسبة
   - ملاحظات حول تاريخ الصلاحية

7. **التفاعلات الدوائية:**
   - تفاعلات مع الأدوية الأخرى إن أمكن تحديدها

أرجو تقديم المعلومات بشكل واضح ومرتب باستخدام التنسيق التالي:
{
    "name_arabic": "الاسم التجاري",
    "name_scientific": "الاسم العلمي / المادة الفعالة",
    "manufacturer": "الشركة المصنعة / بلد الصنع",
    "indications": "دواعي الاستعمال",
    "dosage": "الجرعة والطريقة",
    "warnings": {
        "pregnancy": "تحذيرات الحوامل والمرضعات",
        "pressure": "تحذيرات مرضى الضغط",
        "diabetes": "تحذيرات مرضى السكري",
        "kidney": "تحذيرات مرضى الكلى",
        "general": "تحذيرات عامة"
    },
    "side_effects": "التأثيرات الجانبية",
    "storage": "طريقة التخزين والصلاحية",
    "interactions": "التفاعلات الدوائية",
    "important_note": "ملاحظة هامة"
}

أرجع النتيجة كJSON صالح فقط، بدون أي نص إضافي أو كود markdown.
"""

        response = client.models.generate_content(
            model=model_name,
            contents=[
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": image_data,
                            }
                        },
                    ]
                }
            ],
        )

        content = response.text.strip()

        if content.startswith("```"):
            content = content.split("\n", 1)[1]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

        result = json.loads(content)

        return {
            "available": True,
            "message": f"تم تحليل الصورة بنجاح باستخدام {model_name}.",
            "result": result,
        }

    except ImportError:
        return {
            "available": False,
            "message": "مكتبة google-genai غير مثبتة. قم بتشغيل: pip install google-genai",
            "result": None,
        }
    except json.JSONDecodeError:
        return {
            "available": True,
            "message": "تم تحليل الصورة لكن لم يتم التعرف على الدواء بوضوح. يرجى المحاولة بصورة أوضح.",
            "result": {
                "name_arabic": "غير مُعرّف",
                "name_scientific": "لم يتم التعرف على المادة الفعالة",
                "manufacturer": "غير مُعرّف",
                "indications": "لم يتم التعرف على دواعي الاستعمال من الصورة",
                "dosage": "يرجى مراجعة النشرة الداخلية للدواء",
                "warnings": {
                    "pregnancy": "استشرط طبيبك قبل استخدام أي دواء أثناء الحمل",
                    "pressure": "استشرط طبيبك إذا كنت تعاني من ارتفاع ضغط الدم",
                    "diabetes": "استشرط طبيبك إذا كنت تعاني من مرض السكري",
                    "kidney": "استشرط طبيبك إذا كنت تعاني من مشاكل في الكلى",
                    "general": "استشرط دائماً طبيبك أو الصيدلي قبل تناول أي دواء",
                },
                "side_effects": "راجع النشرة الداخلية للدواء",
                "storage": "احفظ الدواء في مكان جاف وبارد بعيداً عن أشعة الشمس",
                "interactions": "استشرط طبيبك حول التفاعلات الدوائية المحتملة",
                "important_note": "لم يتم التعرف على الدواء بوضوح من الصورة. يرجى المحاولة بصورة أوضح ومباشرة للعلبة.",
            },
        }
    except Exception as e:
        return {
            "available": False,
            "message": f"خطأ في تحليل الصورة: {str(e)}",
            "result": None,
        }
