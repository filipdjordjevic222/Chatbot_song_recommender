import json
import pandas as pd
import os
from dotenv import load_dotenv
from functions import search_spotify_tracks, get_recommendations
load_dotenv()

def get_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "recommend_song",
                "description": "Recommend a song based on the user's query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The user's query, it includes information about the song, artist, album, genre, etc."
                        },
                    },
                    "required": ["query"],
                },
            },
        }
    ]

def parse_tool_call(message):
    if message.tool_calls:
        for tool_call in message.tool_calls:
            tool_call_arguments = json.loads(tool_call.function.arguments)
            print("TOOL CALL ARGUMENTS: ", tool_call_arguments)
            if tool_call.function.name == "recommend_song":
                query = tool_call_arguments["query"]
                search_results = search_spotify_tracks(query, 1)
                recommendations = get_recommendations(search_results, 0)
                print("RECOMMENDATIONS: ", recommendations)
                return "Here are my recommendations: ", recommendations
    return message.content, None