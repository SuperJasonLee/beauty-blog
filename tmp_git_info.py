import subprocess

# Check git log
r = subprocess.run(['git', 'log', '--oneline', '-5'], capture_output=True, text=True, cwd=r'E:\git_local\beauty-blog')
with open(r'E:\git_local\beauty-blog\tmp_git_log.txt', 'w', encoding='utf-8') as f:
    f.write(r.stdout)
    f.write(r.stderr)

# Check git remote -v to confirm push target
r2 = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True, cwd=r'E:\git_local\beauty-blog')
with open(r'E:\git_local\beauty-blog\tmp_git_remote.txt', 'w', encoding='utf-8') as f:
    f.write(r2.stdout)

print('Done')
