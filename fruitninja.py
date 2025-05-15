import cv2
import mediapipe as mp
import asyncio
import websockets
import json

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    model_complexity=0
)

async def process_frame(websocket, path):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                return

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            landmarks = []
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    landmarks.append({
                        'x': 1 - hand_landmarks.landmark[8].x,
                        'y': hand_landmarks.landmark[8].y,
                        'z': hand_landmarks.landmark[8].z
                    })

            await websocket.send(json.dumps({
                'landmarks': landmarks
            }))
            await asyncio.sleep(1/30)
    except Exception as e:
        print(f"Error in process_frame: {e}")
    finally:
        cap.release()

async def main():
    server = await websockets.serve(process_frame, "localhost", 8765)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())