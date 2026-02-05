# Deploy to Koyeb

Your API is now ready for Koyeb deployment!

## Quick Deploy

### Option 1: Deploy via GitHub (Recommended)

1. Push your code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. Go to [Koyeb Dashboard](https://app.koyeb.com/)

3. Click "Create App" → "Deploy from GitHub"

4. Select your repository

5. Configure:
   - **Build command**: (leave empty, auto-detected)
   - **Run command**: (leave empty, uses Procfile)
   - **Port**: 8000
   - **Instance type**: Nano (free tier)

6. Click "Deploy"

### Option 2: Deploy via Koyeb CLI

1. Install Koyeb CLI:
```bash
# Windows (PowerShell)
iwr https://cli.koyeb.com/install.ps1 -useb | iex

# Or download from: https://github.com/koyeb/koyeb-cli/releases
```

2. Login to Koyeb:
```bash
koyeb login
```

3. Deploy:
```bash
koyeb app init youtube-api --git github.com/YOUR_USERNAME/YOUR_REPO --git-branch main
```

### Option 3: Deploy via Docker (Advanced)

Create a Dockerfile if you prefer Docker deployment.

## Configuration Files

- **Procfile**: Tells Koyeb how to run your app
- **requirements.txt**: Python dependencies (now includes gunicorn)
- **runtime.txt**: Specifies Python version
- **.koyeb.yml**: Optional Koyeb configuration

## Environment Variables

No environment variables are required for basic functionality.

## API Endpoints

Once deployed, your API will be available at:
```
https://your-app-name.koyeb.app/api/download?url=<youtube_url>&quality=<quality>
```

### Test Endpoint
```
https://your-app-name.koyeb.app/api/test
```

### Home
```
https://your-app-name.koyeb.app/
```

## Monitoring

- View logs in Koyeb Dashboard
- Monitor performance and uptime
- Set up health checks (automatic with Koyeb)

## Free Tier Limits

Koyeb free tier includes:
- 1 nano instance
- 512 MB RAM
- Shared CPU
- Auto-scaling disabled

## Troubleshooting

If deployment fails:
1. Check logs in Koyeb Dashboard
2. Verify all dependencies in requirements.txt
3. Ensure PORT environment variable is used (already configured)
4. Check Python version compatibility

## Notes

- The app automatically binds to the PORT environment variable provided by Koyeb
- Gunicorn is used as the production WSGI server
- Health checks are handled automatically by Koyeb
