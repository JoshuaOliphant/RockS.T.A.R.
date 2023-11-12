delete_assistants:
    for id in $(curl "https://api.openai.com/v1/assistants?order=desc&limit=20" -H "Content-Type: application/json" -H "Authorization: Bearer $OPENAI_API_KEY" -H "OpenAI-Beta: assistants=v1" | jq -r '.data[].id'); do \
        curl "https://api.openai.com/v1/assistants/$id" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $OPENAI_API_KEY" \
            -H "OpenAI-Beta: assistants=v1" \
            -X DELETE; \
    done