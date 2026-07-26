import httpx, re

urls = [
    ('nose', 'https://images.pexels.com/photos/3220552/pexels-photo-3220552.jpeg?auto=compress&cs=tinysrgb&w=800'),
    ('breast', 'https://images.pexels.com/photos/3768133/pexels-photo-3768133.jpeg?auto=compress&cs=tinysrgb&w=800'),
    ('weight', 'https://images.pexels.com/photos/3822622/pexels-photo-3822622.jpeg?auto=compress&cs=tinysrgb&w=800'),
]
for name, url in urls:
    r = httpx.head(url, timeout=15)
    print(f'{name}: {r.status_code}')
    if r.status_code == 200:
        print(f'  type: {r.headers.get("Content-Type","")}')
