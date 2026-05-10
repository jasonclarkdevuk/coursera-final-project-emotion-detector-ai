''' Executing this function initiates the application of emotion
    analysis to be executed over the Flask channel and deployed on
    localhost:5000.
'''
#Import Flask, render_template, request from flask framework
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

#Initiate the Flask app
app = Flask("EmotionDetector")

@app.route("/emotionDetector")
def emotion_analyser():
    ''' This code receives the text from the HTML interface and 
        runs emotion detection over it using emotion_detector()
        function. The output returned shows each emotion score
        and the dominant emotion.
    '''
    # Get text to analyse from query parameters
    text_to_analyse = request.args["textToAnalyze"]

    # Call detector for a response
    response = emotion_detector(text_to_analyse)

    # Extract data
    anger = response["anger"]
    disgust = response["disgust"]
    fear = response["fear"]
    joy = response["joy"]
    sadness = response["sadness"]
    dominant_emotion = response["dominant_emotion"]

    # No dominant emotion set, presume invalid input
    if dominant_emotion is None:
        return "<strong>Invalid text! Please try again!</strong>"

    # Return data since dominant emotion is present
    intro = "For the given statement, the system response is "
    anger_info = f"'anger': {anger}"
    disgust_info = f", 'disgust': {disgust}"
    fear_info = f", 'fear': {fear}"
    joy_info = f", 'joy': {joy}"
    sadness_info = f", 'sadness': {sadness}."
    dominant_info = f" The dominant emotion is <strong>{dominant_emotion}</strong>."

    return intro + anger_info + disgust_info + fear_info + joy_info + sadness_info + dominant_info

@app.route("/")
def render_index_page():
    ''' This function initiates the rendering of the main application
        page over the Flask channel
    '''
    return render_template("index.html")

if __name__ == "__main__":
    # This functions executes the flask app and deploys it on localhost:5000

    # Run the Flask app
    app.run(debug=True) # Debug mode is enabled
