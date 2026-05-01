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


def parse_roboflow_prediction(data: dict) -> dict:
    predictions = data.get("predictions", {})

    if isinstance(predictions, dict) and predictions:
        best_class = None
        best_confidence = -1

        for class_name, class_data in predictions.items():
            if isinstance(class_data, dict):
                confidence = class_data.get("confidence", 0)
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_class = class_name

        return {
            "disease_name": best_class if best_class else "Unknown",
            "confidence": best_confidence if best_confidence >= 0 else None,
        }

    predicted_classes = data.get("predicted_classes", [])
    if predicted_classes:
        disease_name = predicted_classes[0]
        confidence = None

        if isinstance(predictions, dict) and disease_name in predictions:
            class_info = predictions[disease_name]
            if isinstance(class_info, dict):
                confidence = class_info.get("confidence")

        return {
            "disease_name": disease_name,
            "confidence": confidence,
        }

    return {
        "disease_name": "No disease detected",
        "confidence": None,
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

    return {
        "disease_name": parsed.get("disease_name"),
        "confidence": parsed.get("confidence"),
        "recommendation": generate_recommendation(parsed.get("disease_name")),
        "raw_response": data,
    }