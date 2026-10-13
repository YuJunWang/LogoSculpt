@echo off
chcp 65001 >nul
title PNG to SVG 批次向量化工具

echo ========================================================
echo   ⚡ PNG to SVG 批次向量化與去背工作流程
echo ========================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [錯誤] 找不到 Python 環境，請確認已安裝 Python 並加入 PATH。
    pause
    exit /b 1
)

echo [1/3] 檢查環境與相依套件...
python -c "import vtracer, resvg_py, PIL, cv2, numpy" >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [提示] 正在安裝相依套件 (pillow, vtracer, resvg_py, opencv-python, numpy)...
    pip install -r requirements.txt
)

echo [2/3] 開始執行轉換...
python convert.py

echo.
echo [3/3] 正在開啟成果預覽網頁...
if exist "output\preview.html" (
    start "" "output\preview.html"
)

echo ========================================================
echo   ✅ 處理完畢！
echo ========================================================
echo.
pause
