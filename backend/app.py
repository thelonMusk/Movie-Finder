from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app)

# API Keys from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/api/search', methods=['POST'])
def search_movies():
    try:
        data = request.json
        user_query = data.get('query', '')
        
        if not user_query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Step 1: Use Groq AI to understand the query and extract movie criteria
        current_year = datetime.now().year
        current_date = datetime.now().strftime("%B %Y")
        
        groq_response = requests.post(
            GROQ_API_URL,
            headers={
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'llama-3.3-70b-versatile',
                'messages': [
                    {
                        'role': 'system',
                        'content': f'''You are an expert movie critic and recommendation specialist with deep knowledge of cinema history, genres, themes, and filmmaking styles.

CURRENT DATE: {current_date}
CURRENT YEAR: {current_year}

IMPORTANT TIME CONTEXT:
- "Recent" or "new" movies = {current_year} and {current_year - 1}
- "Latest" or "this year" = {current_year} only
- "Last few years" = {current_year - 3} to {current_year}
- Movies from 2022 and earlier are NOT recent anymore

LANGUAGE PREFERENCES:
- DEFAULT: Only recommend English-language movies unless user specifically asks for foreign/international films
- If user mentions a specific country or language (Korean, Japanese, French, Spanish, etc.), include those
- If user says "foreign films" or "international", include non-English movies
- ALWAYS prioritize English movies unless explicitly asked otherwise

CRITICAL INSTRUCTIONS:
1. Analyze the user's query to understand EXACTLY what they want:
   - Specific genre or subgenre (e.g., "psychological thriller" not just "thriller")
   - Time period/era - PAY SPECIAL ATTENTION to temporal keywords:
     * "recent", "new", "latest", "this year" → {current_year} and {current_year - 1}
     * "modern" → 2020s
     * "classic" → pre-2000s
   - Mood/tone (e.g., "dark", "uplifting", "thought-provoking")
   - Similar movies mentioned
   - Themes (e.g., "time travel", "revenge", "coming of age")
   - Style preferences (e.g., "indie", "big budget", "foreign")
   - Language preferences (default to English)

2. Recommend 15-20 HIGHLY SPECIFIC movies that PERFECTLY match ALL criteria:
   - Prioritize exact matches over popular movies
   - Include a mix of well-known and hidden gems
   - Consider director, cinematography, pacing, and storytelling style
   - Match the emotional tone and atmosphere
   - If they mention a specific movie, find movies with similar themes, style, and feel
   - RESPECT the time period - if they ask for recent, give {current_year} and {current_year - 1}!
   - DEFAULT to English-language films only

3. Be PRECISE with movie titles - use exact official titles as they appear on IMDB

4. Provide diversity in your recommendations (different years, directors) while staying true to the request

Return ONLY a JSON object (no markdown, no code blocks):
{{
    "analysis": "Detailed 2-3 sentence analysis explaining what they're looking for and why these recommendations fit",
    "movies": ["Exact Movie Title 1 (Year)", "Exact Movie Title 2 (Year)", ...]
}}

Example - if they ask "recent sci-fi movies":
Good: "Dune: Part Two (2024)", "The Creator (2023)", "Elevation (2024
Bad: Anything before 2024, non-English films (unless requested)'''
                    },
                    {
                        'role': 'user',
                        'content': user_query
                    }
                ],
                'temperature': 0.5,
                'max_tokens': 1500
            }
        )
        
        if groq_response.status_code != 200:
            return jsonify({'error': 'Groq API error', 'details': groq_response.text}), 500
        
        groq_data = groq_response.json()
        ai_response = groq_data['choices'][0]['message']['content']
        
        # Parse the AI response
        try:
            # Remove markdown code blocks if present
            ai_response = ai_response.strip()
            if ai_response.startswith('```'):
                ai_response = ai_response.split('```')[1]
                if ai_response.startswith('json'):
                    ai_response = ai_response[4:]
            ai_response = ai_response.strip()
            
            parsed_response = json.loads(ai_response)
            movie_titles = parsed_response.get('movies', [])
            analysis = parsed_response.get('analysis', '')
        except json.JSONDecodeError:
            # Fallback: extract movie titles manually
            movie_titles = []
            analysis = ai_response
        
        # Step 2: Fetch movie details from OMDB
        movies_data = []
        for title in movie_titles[:10]:  # Limit to 10 movies
            # Clean the title (remove year if included in parentheses)
            clean_title = title.split('(')[0].strip() if '(' in title else title.strip()
            
            omdb_response = requests.get(
                'http://www.omdbapi.com/',
                params={
                    'apikey': OMDB_API_KEY,
                    't': clean_title,
                    'type': 'movie'
                }
            )
            
            if omdb_response.status_code == 200:
                movie_info = omdb_response.json()
                if movie_info.get('Response') == 'True':
                    movies_data.append({
                        'title': movie_info.get('Title'),
                        'year': movie_info.get('Year'),
                        'rated': movie_info.get('Rated'),
                        'runtime': movie_info.get('Runtime'),
                        'genre': movie_info.get('Genre'),
                        'director': movie_info.get('Director'),
                        'actors': movie_info.get('Actors'),
                        'plot': movie_info.get('Plot'),
                        'poster': movie_info.get('Poster'),
                        'imdbRating': movie_info.get('imdbRating'),
                        'imdbID': movie_info.get('imdbID')
                    })
        
        return jsonify({
            'analysis': analysis,
            'movies': movies_data,
            'query': user_query
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Movie Finder API is running'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)