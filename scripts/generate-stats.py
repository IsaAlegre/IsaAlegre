import requests
import os
from datetime import datetime
import sys

GITHUB_USERNAME = os.getenv('GITHUB_USERNAME', 'isaAlegre')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

try:
    print(f"[INFO] Starting stats generation for: {GITHUB_USERNAME}")
    
    headers = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}
    
    print("[INFO] Fetching user data...")
    user_url = f'https://api.github.com/users/{GITHUB_USERNAME}'
    user_response = requests.get(user_url, headers=headers)
    user_response.raise_for_status()
    user_data = user_response.json()
    
    print("[INFO] Fetching repos...")
    repos_url = f'https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100'
    repos_response = requests.get(repos_url, headers=headers)
    repos_response.raise_for_status()
    repos = repos_response.json()
    
    public_repos = user_data.get('public_repos', 0)
    followers = user_data.get('followers', 0)
    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos if isinstance(repos, list))
    
    print(f"[INFO] Stats: {public_repos} repos, {followers} followers, {total_stars} stars")
    
    stats = {'repos': public_repos, 'followers': followers, 'stars': total_stars}
    
    svg = f'''<svg width="500" height="280" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0d1117;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#161b22;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="500" height="280" fill="url(#grad1)"/>
  <rect width="500" height="280" fill="none" stroke="#AC4EF7" stroke-width="2" opacity="0.5"/>
  <text x="250" y="40" font-size="28" font-weight="bold" text-anchor="middle" fill="#AC4EF7" font-family="Fira Code">
    📊 GitHub Stats
  </text>
  <g>
    <rect x="30" y="70" width="140" height="85" fill="none" stroke="#AC4EF7" stroke-width="1.5" opacity="0.3" rx="5"/>
    <text x="100" y="95" font-size="32" text-anchor="middle" fill="#AC4EF7" font-weight="bold">{stats['repos']}</text>
    <text x="100" y="125" font-size="14" text-anchor="middle" fill="#8b5cf6" font-family="Fira Code">Repositories</text>
  </g>
  <g>
    <rect x="180" y="70" width="140" height="85" fill="none" stroke="#AC4EF7" stroke-width="1.5" opacity="0.3" rx="5"/>
    <text x="250" y="95" font-size="32" text-anchor="middle" fill="#AC4EF7" font-weight="bold">{stats['followers']}</text>
    <text x="250" y="125" font-size="14" text-anchor="middle" fill="#8b5cf6" font-family="Fira Code">Followers</text>
  </g>
  <g>
    <rect x="330" y="70" width="140" height="85" fill="none" stroke="#AC4EF7" stroke-width="1.5" opacity="0.3" rx="5"/>
    <text x="400" y="95" font-size="32" text-anchor="middle" fill="#AC4EF7" font-weight="bold">{stats['stars']}</text>
    <text x="400" y="125" font-size="14" text-anchor="middle" fill="#8b5cf6" font-family="Fira Code">Total Stars</text>
  </g>
  <text x="250" y="260" font-size="12" text-anchor="middle" fill="#6b7280" font-family="Fira Code" opacity="0.7">
    Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
  </text>
</svg>'''
    
    print("[INFO] Writing SVG file...")
    with open('stats.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    
    print("✅ stats.svg generated successfully!")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)