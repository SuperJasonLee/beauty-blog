import subprocess
result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True, cwd=r'E:\git_local\beauty-blog')
with open(r'E:\git_local\beauty-blog\tmp_git_status.txt', 'w', encoding='utf-8') as f:
    f.write(result.stdout)
    f.write(result.stderr)
print('done')
