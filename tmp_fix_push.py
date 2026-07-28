import subprocess

# Remove the large data file from git and update .gitignore
cmds = [
    ['git', 'rm', '--cached', 'data/crawled/plastic-surgery-subfields-news/plastic_surgery_subfields_news_20260726_114327.json'],
    ['git', 'rm', '--cached', 'data/crawled/plastic-surgery-subfields-news/crawled_urls.json'],
]
for cmd in cmds:
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=r'E:\git_local\beauty-blog')
    print(f'{cmd[-1]}: rc={r.returncode}')

# Add .gitignore update for data dir
r = subprocess.run(['git', 'add', '.gitignore'], capture_output=True, text=True, cwd=r'E:\git_local\beauty-blog')

# Amend commit
r = subprocess.run(
    ['git', 'commit', '--amend', '--no-edit'],
    capture_output=True, text=True, cwd=r'E:\git_local\beauty-blog'
)
print(f'Amend: rc={r.returncode}')
if r.stderr:
    print(r.stderr[:200])

# Push
r = subprocess.run(
    ['git', 'push', 'origin', 'main'],
    capture_output=True, text=True, cwd=r'E:\git_local\beauty-blog', timeout=60
)
with open(r'E:\git_local\beauty-blog\tmp_push2_result.txt', 'w', encoding='utf-8') as f:
    f.write(r.stdout)
    f.write(r.stderr)
    f.write(f'\nExit: {r.returncode}\n')
print('Push done')
