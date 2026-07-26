import httpx, re

pages = [
    ('nose', 'https://www.pexels.com/photo/woman-with-nose-ring-3220552/'),
    ('breast', 'https://www.pexels.com/photo/confident-woman-in-white-bra-smiling-at-camera-3768133/'),
    ('weight', 'https://www.pexels.com/photo/woman-measuring-her-weight-3822622/'),
]

for name, url in pages:
    r = httpx.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
    print(f'{name}: {r.status_code}')
    if r.status_code == 200:
        text = r.text
        if 'Pexels License' in text or 'pexels license' in text.lower():
            print(f'  License: Pexels License found')
        else:
            print(f'  License: NOT found in HTML')
        # Find photographer
        m = re.search(r'"photographer"[^>]*>([^<]+)', text, re.I)
        if m: print(f'  Photographer: {m.group(1)}')
        m2 = re.search(r'"@([^"]+)"', text)
        if m2: print(f'  Handle: {m2.group(1)}')
