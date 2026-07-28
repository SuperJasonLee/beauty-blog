import subprocess

r = subprocess.run(
    ['git', 'push', 'origin', 'main'],
    capture_output=True, text=True, cwd=r'E:\git_local\beauty-blog', timeout=60
)
with open(r'E:\git_local\beauty-blog\tmp_push_result.txt', 'w', encoding='utf-8') as f:
    f.write('STDOUT:\n')
    f.write(r.stdout)
    f.write('\nSTDERR:\n')
    f.write(r.stderr)
    f.write(f'\nExit code: {r.returncode}\n')
print('done')
