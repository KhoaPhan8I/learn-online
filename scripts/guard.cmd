@echo off
REM Round 223 — pre-push guard chay tay: node --check + seo --check
python -c "import re;s=open('index.html',encoding='utf-8-sig').read();open('_syntax.ci.js','w',encoding='utf-8').write(chr(10).join(re.findall(r'<script>([\s\S]*?)</script>',s)))"
python -c "import re;s=open('gia/index.html',encoding='utf-8').read();open('_syntax.ci.js','a',encoding='utf-8').write(chr(10).join(re.findall(r'<script>([\s\S]*?)</script>',s)))"
node --check _syntax.ci.js || exit /b 1
del _syntax.ci.js
python scripts/seo_build.py --check || exit /b 1
echo GUARD_OK
