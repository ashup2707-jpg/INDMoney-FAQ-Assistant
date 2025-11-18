# Streamlit Deployment Instructions

## Deploying to Streamlit Community Cloud

1. Push your code to GitHub
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository
6. Set the following options:
   - Main file: `streamlit_app.py`
   - Python version: 3.9
7. Click "Deploy"

## Environment Variables

Set the following environment variables in Streamlit:
- `BACKEND_URL` - URL of your deployed backend API

## Running Locally

To run locally:
```bash
pip install -r requirements-streamlit.txt
streamlit run streamlit_app.py
```

The app will be available at http://localhost:8501