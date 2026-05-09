import base64
import requests
from django.conf import settings


def generate_recommendation(disease_name: str) -> str:
    if not disease_name:
        return "No recommendation available."

    disease = disease_name.lower()

    recommendations = {
        "algal_spot": "Prune affected leaves and improve air circulation. Apply approved treatment where necessary.",
        "brown_blight": "Maintain field hygiene and apply suitable fungicide if symptoms persist.",
        "gray_blight": "Remove infected material and reduce moisture around plants.",
        "healthy": "No disease detected. Continue regular monitoring and good agronomic practices.",
        "helopeltis": "Inspect nearby plants and apply integrated pest management measures to control helopeltis infestation.",
        "red_spot": "Remove affected leaves and consult an agricultural officer for suitable treatment.",
    }

    return recommendations.get(
        disease,
        "Consult an agricultural officer for expert validation and treatment guidance."
    )


MIN_CONFIDENCE_THRESHOLD = 0.40  # 40%


def parse_roboflow_prediction(data: dict) -> dict:
    predictions = data.get("predictions", {})

    best_class = None
    best_confidence = None

    if isinstance(predictions, dict) and predictions:
        for class_name, class_data in predictions.items():
            if isinstance(class_data, dict):
                confidence = class_data.get("confidence", 0)

                if best_confidence is None or confidence > best_confidence:
                    best_confidence = confidence
                    best_class = class_name

    if best_class is None:
        return {
            "disease_name": "Invalid / Unclear Image",
            "confidence": None,
            "is_valid_prediction": False,
        }

    if best_confidence is None or best_confidence < MIN_CONFIDENCE_THRESHOLD:
        return {
            "disease_name": "Invalid / Unclear Image",
            "confidence": best_confidence,
            "is_valid_prediction": False,
        }

    return {
        "disease_name": best_class,
        "confidence": best_confidence,
        "is_valid_prediction": True,
    }



def analyze_image_with_roboflow(image_path: str) -> dict:
    api_key = settings.ROBOFLOW_API_KEY
    model_id = settings.ROBOFLOW_MODEL_ID
    url = f"https://classify.roboflow.com/{model_id}"

    with open(image_path, "rb") as image_file:
        image_b64 = base64.b64encode(image_file.read()).decode("utf-8")

    response = requests.post(
        url,
        params={"api_key": api_key},
        data=image_b64,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=60,
    )

    response.raise_for_status()
    data = response.json()

    parsed = parse_roboflow_prediction(data)

    if not parsed.get("is_valid_prediction"):
        recommendation = (
            "The uploaded image does not appear to be a clear tea leaf disease sample. "
            "Please upload a clear image of a tea leaf for reliable diagnosis."
        )
    else:
        recommendation = generate_recommendation(parsed.get("disease_name"))

    return {
        "disease_name": parsed.get("disease_name"),
        "confidence": parsed.get("confidence"),
        "recommendation": recommendation,
        "raw_response": data,
        "is_valid_prediction": parsed.get("is_valid_prediction"),
    }
