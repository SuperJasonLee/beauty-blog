import urllib.request, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://api.github.com/repos/SuperJasonLee/beauty-blog/actions/runs?per_page=3'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github+json'})
try:
    with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
        data = json.loads(resp.read())
    with open(r'E:\git_local\beauty-blog\tmp_gh_actions.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=2)[:3000])
    print('OK')
except Exception as e:
    with open(r'E:\git_local\beauty-blog\tmp_gh_actions.txt', 'w', encoding='utf-8') as f:
        f.write(f'Error: {e}')
    print(f'Error: {e}')
