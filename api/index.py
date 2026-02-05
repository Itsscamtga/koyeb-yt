# from flask import Flask, request, jsonify
# import requests
# import time
# import re
# from urllib.parse import urlparse, parse_qs

# app = Flask(__name__)

# class YouTubeDownloader:
#     def __init__(self):
#         self.headers = {
#             'accept': '*/*',
#             'accept-language': 'en-US,en;q=0.9',
#             'origin': 'https://downloaderto.com',
#             'priority': 'u=1, i',
#             'referer': 'https://downloaderto.com/',
#             'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
#             'sec-ch-ua-mobile': '?0',
#             'sec-ch-ua-platform': '"Windows"',
#             'sec-fetch-dest': 'empty',
#             'sec-fetch-mode': 'cors',
#             'sec-fetch-site': 'cross-site',
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
#         }
#         self.api_key = 'dfcb6d76f2f6a9894gjkege8a4ab232222'
    
#     def extract_video_id(self, url):
#         """Extract YouTube video ID from various URL formats"""
#         patterns = [
#             r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
#             r'(?:embed\/)([0-9A-Za-z_-]{11})',
#             r'(?:watch\?v=)([0-9A-Za-z_-]{11})',
#             r'^([0-9A-Za-z_-]{11})$'
#         ]
        
#         for pattern in patterns:
#             match = re.search(pattern, url)
#             if match:
#                 return match.group(1)
        
#         parsed = urlparse(url)
#         if parsed.query:
#             params = parse_qs(parsed.query)
#             if 'v' in params:
#                 return params['v'][0]
        
#         return None
    
#     def get_download_url(self, youtube_url, format='360', max_retries=30, retry_delay=2):
#         """Get download URL for a YouTube video"""
#         params = {
#             'copyright': '0',
#             'format': format,
#             'url': youtube_url,
#             'api': self.api_key,
#         }
        
#         response = requests.get('https://p.savenow.to/ajax/download.php', params=params, headers=self.headers)
#         data = response.json()
        
#         if not data.get('success'):
#             return {'error': 'Failed to initiate download', 'data': data}
        
#         download_id = data.get('id')
#         progress_params = {'id': download_id}
        
#         for attempt in range(max_retries):
#             progress_response = requests.get('https://p.savenow.to/api/progress', params=progress_params, headers=self.headers)
#             progress_data = progress_response.json()
            
#             if progress_data.get('success') == 1 and progress_data.get('progress') == 1000:
#                 return {
#                     'success': True,
#                     'video_id': self.extract_video_id(youtube_url),
#                     'download_url': progress_data.get('download_url'),
#                     'alternative_urls': progress_data.get('alternative_download_urls', []),
#                     'title': data.get('title'),
#                     'thumbnail': data.get('info', {}).get('image')
#                 }
            
#             time.sleep(retry_delay)
        
#         return {'error': 'Timeout waiting for download'}

# downloader = YouTubeDownloader()

# @app.route('/download', methods=['GET'])
# def download_video():
#     """
#     API endpoint to get YouTube video download URL
    
#     Parameters:
#         url (str): YouTube video URL or video ID
#         format (str): Video quality (default: 360)
    
#     Example:
#         /download?url=https://www.youtube.com/watch?v=6nFNIJBs6qw
#         /download?url=6nFNIJBs6qw&format=720
#     """
#     video_url = request.args.get('url')
#     format_quality = request.args.get('format', '360')
    
#     if not video_url:
#         return jsonify({'error': 'Missing url parameter'}), 400
    
#     # Extract video ID
#     video_id = downloader.extract_video_id(video_url)
    
#     if not video_id:
#         return jsonify({'error': 'Invalid YouTube URL or video ID'}), 400
    
#     # Construct full YouTube URL if only ID was provided
#     full_url = f"https://www.youtube.com/watch?v={video_id}"
    
#     # Get download URL
#     result = downloader.get_download_url(full_url, format=format_quality)
    
#     if result.get('success'):
#         return jsonify(result), 200
#     else:
#         return jsonify(result), 500

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({
#         'message': 'YouTube Downloader API',
#         'usage': '/download?url=<youtube_url>&format=<quality>',
#         'example': '/download?url=https://www.youtube.com/watch?v=6nFNIJBs6qw&format=360'
#     })

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
import requests
import json as json_module

app = Flask(__name__)

# Step 1: Get resource_id from YouTube URL
def get_resource_id(yt_url, quality='360P'):
    # Try both 'cache' and 'source' origins
    errors = []
    
    for origin_type in ['cache', 'source']:
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'http://vidssave.com',
            'referer': 'http://vidssave.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        }

        data = {
            'auth': '20250901majwlqo',
            'domain': 'api-ak.vidssave.com',
            'origin': origin_type,
            'link': yt_url,
        }

        try:
            print(f"Trying origin: {origin_type}")
            response = requests.post('https://api.vidssave.com/api/contentsite_api/media/parse', 
                                    headers=headers, data=data, timeout=30)
            
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text[:500]}")
            
            response.raise_for_status()
            result = response.json()
            
            print(f"Result status: {result.get('status')}")
            
            if result.get('status') == 1:
                resources = result['data']['resources']
                
                # Find the best matching resource based on quality
                resource = None
                
                # First, try to find exact quality match
                for res in resources:
                    if res['quality'] == quality and res['type'] == 'video':
                        resource = res
                        break
                
                # If requested quality not found, find the best available MP4 video
                if not resource:
                    # Quality priority order (highest to lowest)
                    quality_order = ['2160P', '1440P', '1080P', '720P', '480P', '360P', '240P', '144P']
                    
                    # Filter only video resources
                    video_resources = [res for res in resources if res['type'] == 'video']
                    
                    # Sort by quality priority
                    for q in quality_order:
                        for res in video_resources:
                            if res['quality'] == q:
                                resource = res
                                break
                        if resource:
                            break
                    
                    # If still not found, get first available video
                    if not resource and video_resources:
                        resource = video_resources[0]
                
                if not resource:
                    continue  # Try next origin
                
                # Check download_mode to determine the flow
                download_mode = resource.get('download_mode', '')
                
                if download_mode == 'direct':
                    # For direct mode, return the download_url directly
                    download_url = resource.get('download_url')
                    if download_url:
                        return {'mode': 'direct', 'url': download_url}, None
                
                elif download_mode == 'check_download' or download_mode == '':
                    # For check_download mode or empty, need to go through the full process
                    if 'resource_content' in resource and 'resource_id' in resource:
                        return {
                            'mode': 'check_download',
                            'resource_id': resource['resource_id'],
                            'resource_content': resource['resource_content']
                        }, None
        
        except Exception as e:
            error_msg = f"Origin {origin_type}: {str(e)}"
            print(error_msg)
            errors.append(error_msg)
            continue
    
    return None, f"Failed to parse video. Errors: {'; '.join(errors)}"

# Step 2: Get task_id from resource_content
def get_task_id(resource_content):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'http://vidssave.com',
        'referer': 'http://vidssave.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    }

    data = {
        'auth': '20250901majwlqo',
        'domain': 'api-ak.vidssave.com',
        'request': resource_content,
        'no_encrypt': '1',
    }

    try:
        print(f"Getting task_id with resource_content length: {len(resource_content)}")
        response = requests.post('https://api.vidssave.com/api/contentsite_api/media/download', 
                                headers=headers, data=data, timeout=30)
        
        print(f"Task response status: {response.status_code}")
        response.raise_for_status()
        result = response.json()
        
        print(f"Task result: {result}")
        
        if result.get('status') != 1:
            return None, "Failed to get task_id"
        
        task_id = result['data']['task_id']
        return task_id, None
        
    except Exception as e:
        print(f"Task error: {str(e)}")
        return None, str(e)

# Step 3: Get download link from task_id
def get_download_link(task_id, max_retries=3):
    headers = {
        'accept': 'text/event-stream',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'http://vidssave.com',
        'referer': 'http://vidssave.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    }

    url = f'https://api.vidssave.com/sse/contentsite_api/media/download_query?auth=20250901majwlqo&domain=api-ak.vidssave.com&task_id={task_id}&download_domain=vidssave.com&origin=content_site'
    
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()
            
            # Parse SSE response
            download_url = None
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        import json
                        data = json.loads(line[6:])
                        if data.get('status') == 'success':
                            download_url = data.get('download_link')
                            if download_url:
                                return download_url, None
            
            if attempt < max_retries:
                continue
            else:
                return None, f"Download link not found after {max_retries} attempts"
            
        except Exception as e:
            if attempt < max_retries:
                continue
            else:
                return None, f"Failed after {max_retries} attempts: {str(e)}"
    
    return None, f"Download link not found after {max_retries} attempts"

@app.route('/api/download', methods=['GET'])
def download():
    """
    API endpoint to get YouTube video download link
    Query parameters:
    - url: YouTube video URL (required)
    - quality: Video quality (optional, default: 360P)
    """
    try:
        yt_url = request.args.get('url')
        quality = request.args.get('quality', '360P').upper()
        
        print(f"Request received - URL: {yt_url}, Quality: {quality}")
        
        if not yt_url:
            return jsonify({
                'success': False,
                'error': 'YouTube URL is required'
            }), 400
        
        # Step 1: Get resource data
        resource_data, error = get_resource_id(yt_url, quality)
        
        if error:
            print(f"Error in get_resource_id: {error}")
            return jsonify({
                'success': False,
                'error': error
            }), 500
        
        # Check the download mode
        if resource_data['mode'] == 'direct':
            return jsonify({
                'success': True,
                'download_url': resource_data['url'],
                'quality': quality,
                'mode': 'direct',
                'owner': '@scammer_botxz'
            })
        
        elif resource_data['mode'] == 'check_download':
            resource_content = resource_data['resource_content']
            
            # Step 2: Get task_id
            task_id, error = get_task_id(resource_content)
            
            if error:
                print(f"Error in get_task_id: {error}")
                return jsonify({
                    'success': False,
                    'error': error
                }), 500
            
            # Step 3: Get download link
            download_url, error = get_download_link(task_id)
            
            if error:
                print(f"Error in get_download_link: {error}")
                return jsonify({
                    'success': False,
                    'error': error
                }), 500
            
            return jsonify({
                'success': True,
                'download_url': download_url,
                'quality': quality,
                'mode': 'check_download',
                'owner': '@scammer_botxz'
            })
        
        else:
            return jsonify({
                'success': False,
                'error': 'Unknown download mode'
            }), 500
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }), 500

@app.route('/api/test', methods=['GET'])
def test():
    """Test endpoint to check if API is working"""
    try:
        # Test external request
        test_response = requests.get('https://httpbin.org/get', timeout=10)
        return jsonify({
            'success': True,
            'message': 'API is working',
            'test_request_status': test_response.status_code,
            'python_version': __import__('sys').version
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api', methods=['GET'])
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'YouTube Download API',
        'usage': '/api/download?url=<youtube_url>&quality=<quality>',
        'qualities': ['144P', '240P', '360P', '480P', '720P', '1080P', '1440P', '2160P'],
        'default_quality': '360P',
        'owner': '@scammer_botxz'
    })

# For Vercel
# app.debug = False



