@echo off
echo ZH EXISTS: > E:\git_local\beauty-blog\tmp_check.txt
if exist E:\git_local\beauty-blog\public\zh-cn\posts\plastic-surgery-subfields-deep-analysis-2026-07\index.html (
    echo YES >> E:\git_local\beauty-blog\tmp_check.txt
) else (
    echo NO >> E:\git_local\beauty-blog\tmp_check.txt
)
echo EN EXISTS: >> E:\git_local\beauty-blog\tmp_check.txt
if exist E:\git_local\beauty-blog\public\en\posts\plastic-surgery-subfields-deep-analysis-2026-07\index.html (
    echo YES >> E:\git_local\beauty-blog\tmp_check.txt
) else (
    echo NO >> E:\git_local\beauty-blog\tmp_check.txt
)
echo ZH SIZE: >> E:\git_local\beauty-blog\tmp_check.txt
for %%F in (E:\git_local\beauty-blog\content\zh-cn\posts\plastic-surgery-subfields-deep-analysis-2026-07.md) do echo %%~zF >> E:\git_local\beauty-blog\tmp_check.txt
echo EN SIZE: >> E:\git_local\beauty-blog\tmp_check.txt
for %%F in (E:\git_local\beauty-blog\content\en\posts\plastic-surgery-subfields-deep-analysis-2026-07.md) do echo %%~zF >> E:\git_local\beauty-blog\tmp_check.txt
