# YouTube Download API - Vercel Deployment

A simple API to get YouTube video download links with quality selection.

## Deployment Steps

1. Install Vercel CLI (if not installed):
```bash
npm install -g vercel
```

2. Navigate to the project folder:
```bash
cd vercel-deploy
```

3. Deploy to Vercel:
```bash
vercel
```

4. Follow the prompts:
   - Set up and deploy? Yes
   - Which scope? Select your account
   - Link to existing project? No
   - Project name? (press enter for default)
   - Directory? ./ (press enter)
   - Override settings? No

## API Usage

### Endpoint
```
GET /api/download?url=<youtube_url>&quality=<quality>
```

### Parameters
- `url` (required): YouTube video URL
- `quality` (optional): Video quality (default: 360P)
  - Options: 144P, 240P, 360P, 480P, 720P, 1080P, 1440P, 2160P

### Example Request
```
https://your-app.vercel.app/api/download?url=https://www.youtube.com/watch?v=VIDEO_ID&quality=720P
```

### Example Response
```json
{
  "success": true,
  "download_url": "https://...",
  "quality": "720P"
}
```

## Local Testing

```bash
pip install -r requirements.txt
python api/index.py
```

Then visit: `http://localhost:5000/api/download?url=YOUR_YOUTUBE_URL`
