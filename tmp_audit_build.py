import subprocess, json

# Run audit
r = subprocess.run(
    ['python', 'scripts/audit-posts.py', 'content/', '--severity', 'error', '--format', 'json'],
    capture_output=True, text=True, cwd=r'E:\git_local\beauty-blog', timeout=30
)
with open(r'E:\git_local\beauty-blog\tmp_audit_result.txt', 'w', encoding='utf-8') as f:
    f.write(r.stdout)
    if r.stderr:
        f.write('\nSTDERR:\n')
        f.write(r.stderr)
    f.write(f'\nExit: {r.returncode}\n')

# Try Hugo build
r2 = subprocess.run(
    ['hugo', '--gc', '--minify'],
    capture_output=True, text=True, cwd=r'E:\git_local\beauty-blog', timeout=120
)
with open(r'E:\git_local\beauty-blog\tmp_hugo_result.txt', 'w', encoding='utf-8') as f:
    f.write(r2.stdout)
    if r2.stderr:
        f.write('\nSTDERR:\n')
        f.write(r2.stderr)
    f.write(f'\nExit: {r2.returncode}\n')

print('Done')
