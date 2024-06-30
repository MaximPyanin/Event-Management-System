from dotenv import load_dotenv
import os

load_dotenv()


async def get_access_token(
    integration_client,
    role: str = "ORGANIZER",
):
    match role:
        case "ORGANIZER":
            response = await integration_client.post(
                "/api/v1/signin",
                data={
                    "username": os.getenv("ORGANIZER_USERNAME"),
                    "password": os.getenv("ORGANIZER_PASSWORD"),
                },
            )
        case _:
            response = await integration_client.post(
                "/api/v1/signin",
                data={
                    "username": os.getenv("ATTENDEE_USERNAME"),
                    "password": os.getenv("ATTENDEE_PASSWORD"),
                },
            )
    return response.json()
