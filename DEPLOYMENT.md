# Railway Deployment Guide for Sartel.io

This guide will help you deploy Sartel.io to Railway.

## Prerequisites

- A [Railway](https://railway.app) account
- Git installed locally
- Your code pushed to a GitHub repository

## Railway Setup Steps

### 1. Create a New Project on Railway

1. Go to [Railway](https://railway.app) and log in
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `sartel.io` repository
5. Railway will automatically detect the project and start deploying

### 2. Configure Environment Variables (Optional)

Railway will automatically assign a PORT variable. If you need additional environment variables:

1. In your Railway project dashboard, click on your service
2. Go to the **"Variables"** tab
3. Add any custom environment variables if needed

**Note:** The current application doesn't require any additional environment variables, but you may want to add:
- `CORS_ORIGINS` - Comma-separated list of allowed origins (defaults to "*")
- Any analytics or monitoring service keys in the future

### 3. Deployment

Railway will automatically:
- Install Node.js and Python dependencies
- Build the frontend (React + Vite)
- Start the FastAPI backend server
- Serve both API and frontend from a single service

The deployment process:
1. Installs backend Python dependencies from `backend/requirements.txt`
2. Installs frontend npm dependencies
3. Builds the frontend with `npm run build`
4. Starts the server with `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 4. Access Your Application

Once deployed, Railway will provide you with a public URL:
- Go to your service in Railway dashboard
- Click **"Settings"** tab
- Under **"Domains"**, you'll see your public URL
- You can also add a custom domain here

## Automatic Deployments

Railway is configured to automatically deploy when you push to your main branch:
- Push code to GitHub → Railway automatically deploys
- Check deployment status in the Railway dashboard
- View logs in real-time during deployment

## Monitoring

### Health Check
Your application has a health check endpoint at `/health` that Railway can use to monitor service health.

### Logs
- View application logs in the Railway dashboard
- Go to your service → **"Deployments"** tab → Click on a deployment → View logs

### Analytics
Access analytics at `/api/analytics` to see:
- Total lobbies created
- Total players
- Total words submitted
- Active lobbies

## Troubleshooting

### Build Fails
- Check the build logs in Railway dashboard
- Ensure `package.json` and `requirements.txt` are up to date
- Verify that the build commands work locally

### Application Not Starting
- Check that the PORT environment variable is being used correctly
- Review application logs for errors
- Verify that all dependencies are installed

### WebSocket Issues
- Railway supports WebSockets out of the box
- Ensure your frontend is connecting to the correct WebSocket URL
- Check that the `/ws/{lobby_id}/{player_id}` endpoint is accessible

## Local Testing Before Deployment

To test the production build locally:

```bash
# Build the frontend
cd frontend
npm install
npm run build
cd ..

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000` to test the application.

## Configuration Files

The deployment uses these configuration files:
- `railway.json` - Railway-specific configuration
- `nixpacks.toml` - Build and install instructions
- `Procfile` - Process configuration for starting the server

## Support

If you encounter issues:
1. Check Railway's [documentation](https://docs.railway.app)
2. Review the deployment logs in Railway dashboard
3. Ensure your local build works before pushing to production
