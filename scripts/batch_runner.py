"""
batch_runner.py
批次掃描 input/ 資料夾中的圖檔 (PNG, JPG, JPEG, WEBP, AVIF, GIF, BMP, TIFF, ICO)，依序執行向量化去背，並在完成後生成預覽報告
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from core_vectorizer import process_vector_asset
from html_reporter import generate_preview_html

def run_batch(input_dir="input", output_dir="output", fill_color="#FFFFFF", auto_split=True, force=False, threshold=None, padding=2.0):
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    valid_exts = (
        ".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif", 
        ".bmp", ".tiff", ".tif", ".ico"
    )
    
    all_files = os.listdir(input_dir)
    files = []
    for f in all_files:
        ext = os.path.splitext(f)[1].lower()
        if ext in valid_exts:
            files.append(os.path.join(input_dir, f))
            
    files = sorted(files)
    
    if not files:
        print(f"[提示] 未在 '{input_dir}' 資料夾中找到任何圖片檔。")
        print(f"       支援格式：PNG, JPG, WEBP, AVIF, GIF, BMP, TIFF")
        return []
        
    print("=" * 60)
    print(f">> 開始批次向量化轉換流程 (共 {len(files)} 個檔案)")
    print(f"   填色模式：{fill_color} (純白反白版)")
    print(f"   保真門檻：{'自適應 Otsu (防字體變粗與雜訊消除)' if threshold is None else threshold}")
    print(f"   邊界留白：{padding}px (緊密貼齊內容邊界)")
    print(f"   自動組件拆分：{'啟用 (Icon / Text)' if auto_split else '停用'}")
    print("=" * 60)
    
    success_count = 0
    results_list = []
    
    for idx, fpath in enumerate(files, 1):
        filename = os.path.basename(fpath)
        base_name, _ = os.path.splitext(filename)
        clean_name = base_name.replace(" ", "_")
        
        target_subfolder = os.path.join(output_dir, clean_name)
        full_svg = os.path.join(target_subfolder, f"{clean_name}_white_full.svg")
        
        if os.path.exists(full_svg) and not force:
            print(f"[{idx}/{len(files)}] [跳過] 成果已存在: {filename}")
            results_list.append({"name": clean_name, "status": "cached"})
            continue
            
        print(f"[{idx}/{len(files)}] [處理中] {filename} ... ", end="", flush=True)
        try:
            res = process_vector_asset(
                input_path=fpath,
                output_dir=target_subfolder,
                base_name=clean_name,
                fill_color=fill_color,
                auto_split=auto_split,
                threshold=threshold,
                padding=padding
            )
            print("[完成]")
            success_count += 1
            results_list.append({"name": clean_name, "status": "success", "details": res})
        except Exception as e:
            print(f"[失敗] {e}")
            results_list.append({"name": clean_name, "status": "error", "error": str(e)})
            
    # 生成/更新 HTML 預覽報告
    report_path = os.path.join(output_dir, "preview.html")
    generate_preview_html(output_dir, report_path)
    
    print("=" * 60)
    print(f">> 批次處理完畢！成功處理：{success_count} 個新檔案")
    print(f">> 預覽看板已更新：{report_path}")
    print("=" * 60)
    
    return results_list
