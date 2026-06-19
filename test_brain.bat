@echo off
chcp 65001 >nul
cd /d "C:\Users\asifg\OneDrive\Desktop\ai"
python -c "
import sys
sys.path.insert(0, '.')
sys.path.insert(0, 'core')
import warnings
warnings.filterwarnings('ignore')

from core.brain import JarvisBrain
brain = JarvisBrain()
print('Keys loaded:', len(brain.api_keys))
print('Models:', brain.models[:3])
print('Connected:', brain.is_connected)
print()
print('Testing: kamon acho...')
res = brain.think('kamon acho? tumi ki korte paro? banglay bolo')
print('Response:', res[:200] if res else 'NO RESPONSE')
" > test_brain_result.txt 2>&1
type test_brain_result.txt
pause
