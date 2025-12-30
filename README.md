# Movie Finder

An intelligent movie recommendation system powered by AI that understands natural language queries and provides personalized movie suggestions with detailed information.

## Features

- **Natural Language Search**: Ask for movies in plain English - "recent sci-fi thrillers" or "movies like Inception"
- **AI-Powered Analysis**: Uses Groq AI (Llama 3.3 70B) to understand your preferences and match them with perfect recommendations
- **Smart Filtering**: Automatically considers:
  - Genres and subgenres
  - Time periods (recent, classic, modern)
  - Mood and tone
  - Themes and storylines
  - Language preferences (defaults to English)
  - Similar movies
- **Detailed Movie Information**: Get comprehensive details including:
  - Plot summaries
  - Cast and directors
  - IMDB ratings
  - Release year
  - Runtime and rating
  - Movie posters
- **Context-Aware Recommendations**: The AI understands temporal context - "recent" means current year movies, not 5 years ago
- **10-20 Curated Suggestions**: Each search returns carefully selected movies that match your criteria

## Tech Stack

- **Backend**: Python with Flask
- **Frontend**: React
- **AI**: Groq API (Llama 3.3 70B Versatile)
- **Movie Data**: OMDB API
- **CORS**: Flask-CORS for cross-origin requests

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm (comes with Node.js)
- A Groq API key ([Get one here](https://console.groq.com))
- An OMDB API key ([Get one here](http://www.omdbapi.com/apikey.aspx))

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/thelonMusk/Movie-Finder.git
   cd Movie-Finder
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   
   Create a `.env` file in the `backend` directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   OMDB_API_KEY=your_omdb_api_key_here
   ```

6. **Set up the frontend**
   ```bash
   cd ../frontend
   npm install
   ```

## Usage

### Starting the Backend

1. Navigate to the backend directory
   ```bash
   cd backend
   ```

2. Activate the virtual environment (if not already activated)
   ```bash
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
   ```

3. Run the Flask server
   ```bash
   python app.py
   ```

   The backend will start on `http://localhost:5000`

### Starting the Frontend

1. Open a new terminal and navigate to the frontend directory
   ```bash
   cd frontend
   ```

2. Start the React development server
   ```bash
   npm start
   ```

   The frontend will start on `http://localhost:3000` and automatically open in your browser

### Using the Application

Simply type your movie preferences in natural language! Examples:

**By Genre:**
- "Recent psychological thrillers"
- "Classic westerns from the 60s"
- "Indie coming-of-age movies"

**By Mood/Tone:**
- "Dark and gritty crime movies"
- "Uplifting feel-good comedies"
- "Mind-bending sci-fi"

**By Similar Movies:**
- "Movies like Interstellar"
- "Films similar to The Grand Budapest Hotel"
- "Something like Parasite but in English"

**By Theme:**
- "Time travel movies"
- "Movies about artificial intelligence"
- "Heist films with clever twists"

**By Time Period:**
- "Latest action movies" (current year)
- "Recent releases" (last 1-2 years)
- "Modern thrillers" (2020s)
- "Classic films" (pre-2000s)

**International Films:**
- "Korean thrillers" (will include non-English)
- "Foreign psychological dramas"
- By default, recommendations are English-language only

## Project Structure

```
Movie-Finder/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── venv/              # Virtual environment (not in repo)
│   └── .env               # Environment variables (not in repo)
├── frontend/
│   ├── public/            # Static files
│   ├── src/
│   │   ├── App.js        # Main React component
│   │   ├── App.css       # Styling
│   │   └── ...           # Other React components
│   ├── package.json      # Node dependencies
│   └── package-lock.json # Dependency lock file
├── .gitignore
└── README.md
```

## API Endpoints

### `POST /api/search`
Search for movies based on natural language query.

**Request Body:**
```json
{
  "query": "recent sci-fi thrillers"
}
```

**Response:**
```json
{
  "analysis": "AI's analysis of what you're looking for",
  "movies": [
    {
      "title": "Movie Title",
      "year": "2024",
      "rated": "PG-13",
      "runtime": "148 min",
      "genre": "Sci-Fi, Thriller",
      "director": "Director Name",
      "actors": "Actor 1, Actor 2",
      "plot": "Movie plot summary...",
      "poster": "URL to poster",
      "imdbRating": "8.5",
      "imdbID": "tt1234567"
    }
  ],
  "query": "recent sci-fi thrillers"
}
```

### `GET /api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "Movie Finder API is running"
}
```

## Environment Variables

Create a `.env` file in the `backend` directory with the following:

```env
GROQ_API_KEY=your_groq_api_key_here
OMDB_API_KEY=your_omdb_api_key_here
```

**Important**: Never commit your `.env` file to version control. It contains sensitive API keys.

## How It Works

1. **User Input**: You enter a natural language query describing what kind of movie you want to watch

2. **AI Analysis**: Groq AI (Llama 3.3 70B) analyzes your query to understand:
   - Specific genres and subgenres
   - Time period preferences
   - Mood and tone
   - Themes and storytelling style
   - Language preferences

3. **Smart Recommendations**: The AI generates 15-20 highly specific movie recommendations that match your criteria

4. **Movie Details**: For each recommendation, the system fetches detailed information from OMDB API including:
   - Plot summaries
   - Cast and crew
   - Ratings and reviews
   - Posters and metadata

5. **Results Display**: You receive a curated list of movies with all the information you need to make your choice

## Key Features of the AI System

- **Temporal Intelligence**: Understands "recent" means current year, not 5 years ago
- **Genre Precision**: Distinguishes between "thriller" and "psychological thriller"
- **Mood Matching**: Captures atmosphere and emotional tone
- **Style Recognition**: Identifies filmmaking styles (indie, blockbuster, arthouse)
- **Cultural Context**: Respects language preferences and international cinema
- **Similar Movie Logic**: Finds films with matching themes, style, and feel

## Security Note

- The `.env` file is excluded from version control via `.gitignore`
- Always keep your API keys secure and never share them publicly
- Regenerate your API keys immediately if you suspect they have been exposed
- The `venv` directory is also excluded as it should be created locally

## Development

### Installing New Dependencies

Backend:
```bash
cd backend
pip install package_name
pip freeze > requirements.txt
```

Frontend:
```bash
cd frontend
npm install package_name
```

### Running Tests

Frontend:
```bash
cd frontend
npm test
```

### Building for Production

Frontend:
```bash
cd frontend
npm run build
```

The production-ready files will be in the `frontend/build` directory.

## Common Issues

**Issue**: Backend won't start
- **Solution**: Make sure you've activated the virtual environment and installed all dependencies from `requirements.txt`

**Issue**: "API key not found" error
- **Solution**: Ensure your `.env` file exists in the `backend` directory with valid API keys

**Issue**: Frontend can't connect to backend
- **Solution**: Ensure the backend is running on port 5000 and check CORS settings in `app.py`

**Issue**: No movie results returned
- **Solution**: Check that your OMDB API key is valid and has not exceeded rate limits

**Issue**: AI gives irrelevant recommendations
- **Solution**: Try being more specific with your query. Include genre, time period, and mood preferences

## API Rate Limits

- **Groq API**: Check your plan's rate limits at console.groq.com
- **OMDB API**: Free tier allows 1,000 requests per day

## Future Enhancements

- [ ] Save favorite movies
- [ ] User profiles and personalized recommendations
- [ ] Watch history tracking
- [ ] Streaming availability information
- [ ] Advanced filtering options
- [ ] Social sharing features
- [ ] Movie lists and collections

## Contributing

Feel free to fork this project and submit pull requests for any improvements!



## Acknowledgments

- Powered by [Groq](https://groq.com) AI (Llama 3.3 70B Versatile)
- Movie data from [OMDB API](http://www.omdbapi.com/)
- Built with Flask and React

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Enjoy discovering your next favorite movie!** 🎬🍿
