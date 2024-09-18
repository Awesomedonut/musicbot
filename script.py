import requests
from bs4 import BeautifulSoup
import yt_dlp
import time

def get_playlist_videos(playlist_url):
    ydl_opts = {
        'extract_flat': True,
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)
        return [entry['url'] for entry in playlist_info['entries']]

def convert_to_mp3(video_url):
    session = requests.Session()
    response = session.get('https://cnvmp3.com/')
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the form and extract necessary data
    form = soup.find('form', {'id': 'conversionForm'})
    action_url = form['action']
    token = form.find('input', {'name': '_token'})['value']
    
    # Prepare the payload
    payload = {
        '_token': token,
        'url': video_url,
        'format': 'mp3'
    }
    
    # Submit the form
    response = session.post(f'https://cnvmp3.com{action_url}', data=payload)
    
    # Extract download link
    soup = BeautifulSoup(response.text, 'html.parser')
    download_link = soup.find('a', {'class': 'btn-success'})['href']
    
    # Download the MP3 file
    filename = download_link.split('/')[-1]
    mp3_content = session.get(download_link).content
    with open(filename, 'wb') as f:
        f.write(mp3_content)
    
    print(f"Downloaded: {filename}")

def main():
    playlist_url = input("Enter the YouTube playlist URL: ")
    video_urls = get_playlist_videos(playlist_url)
    
    for video_url in video_urls:
        try:
            convert_to_mp3(video_url)
            time.sleep(5)  # Be nice to the server, add a delay between requests
        except Exception as e:
            print(f"Error processing {video_url}: {str(e)}")

if __name__ == "__main__":
    main()