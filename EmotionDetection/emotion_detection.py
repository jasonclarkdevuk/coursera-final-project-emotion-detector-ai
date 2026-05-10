'''
This module is able to analyse text / emotion detection
'''
import json
import requests

def emotion_detector(text_to_analyze):
    '''
    A function that gathers emotion data.
    Provides scores for anger, disgust, fear, joy and sadness.
    Provides errors if there is invalid input.
    '''
    emotion_data = {}

    url = "https://sn-watson-emotion.labs.skills.network/v1"
    url_2 = "/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyze }}

    # HTTP Post request to get emotion data
    response = requests.post(url + url_2, json=input_json, headers=headers)

    # If status code 400, blank data entry provided
    if response.status_code == 400:
        # Set all data to None
        data_keys = ["anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"]

        for key in data_keys:
            emotion_data[key] = None
        
        return emotion_data

    # Successful response, set data using response
    # Convert response to JSON dictionary
    response_data = json.loads(response.text)

    # Return emotion data
    emotion_data["anger"] = response_data["emotionPredictions"][0]["emotion"]["anger"]
    emotion_data["disgust"] = response_data["emotionPredictions"][0]["emotion"]["disgust"]
    emotion_data["fear"] = response_data["emotionPredictions"][0]["emotion"]["fear"]
    emotion_data["joy"] = response_data["emotionPredictions"][0]["emotion"]["joy"]
    emotion_data["sadness"] = response_data["emotionPredictions"][0]["emotion"]["sadness"]

    # Figure out dominant emotion
    dominant_emotion = "anger"

    emotion_checks = ["disgust", "fear", "joy", "sadness"]

    for check in emotion_checks:
        if (emotion_data[check] > emotion_data[dominant_emotion]):
            dominant_emotion = check
    
    emotion_data["dominant_emotion"] = dominant_emotion

    return emotion_data