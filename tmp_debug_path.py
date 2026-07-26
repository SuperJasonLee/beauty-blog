from pathlib import Path
p = Path(r'E:\git_local\beauty-blog\scripts\crawl-plastic-surgery-subfields-2026-07\image_downloader.py').resolve()
print('file:', p)
for i in range(5):
    p = p.parent
    print(f'parent.{i+1}:', p)
print()
repo_root = Path(r'E:\git_local\beauty-blog\scripts\crawl-plastic-surgery-subfields-2026-07\image_downloader.py').resolve().parent.parent.parent.parent
print('REPO_ROOT (4 parents):', repo_root)
print('IMAGES_DIR:', repo_root / 'static' / 'images' / 'posts' / 'plastic-surgery-subfields-2026-07')
print('exists:', (repo_root / 'static' / 'images' / 'posts' / 'plastic-surgery-subfields-2026-07').exists())
