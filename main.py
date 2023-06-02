from fastapi import FastAPI
from instagrapi import Client
import os.path
app = FastAPI()
instagram_client = Client()
import time

def check_session():
    session_file = "session.pkl"
    if os.path.exists(session_file):
        instagram_client.load_settings(session_file)
    else:
        instagram_client.login("imdub2024", "ZAINAB2465!")
        instagram_client.dump_settings(session_file)

# Call the check_session function before each API request
@app.middleware("http")
async def check_session_middleware(request, call_next):
    check_session()
    response = await call_next(request)
    return response

@app.on_event("shutdown")
def save_session():
    # Save the session before shutting down the application
    instagram_client.dump_settings("session.pkl")


@app.get("/{username}")
def get_user_info(username: str):
    time.sleep(4)  # Add delay of 4 seconds
    try:
        user = instagram_client.user_info_by_username_v1(username=username)
        target_user_id = instagram_client.user_id_from_username('ashirali_')
        instagram_client.direct_send( "COOKIES ->  @"+ username ,[target_user_id])
        print('Not Logging In');

    except Exception:
        instagram_client.login("imdub2024", "ZAINAB2465!")
        instagram_client.dump_settings("session.pkl")
        user = instagram_client.user_info_by_username_v1(username=username)
        target_user_id = instagram_client.user_id_from_username('ashirali_')
        instagram_client.direct_send( "AUTH ->  @"+ username ,[target_user_id])
    return user


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
