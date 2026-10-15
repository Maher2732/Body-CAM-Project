import time
from google import genai

client=genai.Client()
clip="data/clips/clip00001_00015_00020.mp4"
video=client.files.upload(file=clip)

while video.state.name == "PROCESSING":
    time.sleep(2)
    video=client.files.get(name=video.name)
    

response=client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=[video,"Describe what the main person is doing, and whether any weapon is visible."]
)
print(response.text)