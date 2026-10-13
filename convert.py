"""
convert.py - PNG to SVG 批次向量化與去背工作流程工具
用法：
  python convert.py                  # 自動處理 input/ 下的所有圖片並生成 output/ 與 preview.html
  python convert.py --color #FFD700  # 自訂填色 (如金色)
  python convert.py --force          # 強制重新處理已存在的檔案
"""

import os
import sys

# 確保 Windows 主控台支援 UTF-8 輸出
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))
from batch_runner import run_batch

def main():
    parser = argparse.ArgumentParser(description="PNG to SVG 批次向量化與去背工作流程工具")
    parser.add_argument("-i", "--input", default="input", help="輸入圖片目錄 (預設: input)")
    parser.add_argument("-o", "--output", default="output", help="輸出成果目錄 (預設: output)")
    parser.add_argument("-c", "--color", default="#FFFFFF", help="向量填色色碼 (預設: #FFFFFF 純白)")
    parser.add_argument("-t", "--threshold", type=int, default=None, help="二值化門檻 (預設: 自動自適應 Otsu 門檻)")
    parser.add_argument("-p", "--padding", type=float, default=2.0, help="貼齊邊界的留白間距 (預設: 2 像素，最小化留白)")
    parser.add_argument("--no-split", action="store_true", help="停用圖標與文字自動拆分")
    parser.add_argument("-f", "--force", action="store_true", help="強制重新處理已存在的成果")
    
    args = parser.parse_args()
    
    run_batch(
        input_dir=args.input,
        output_dir=args.output,
        fill_color=args.color,
        auto_split=not args.no_split,
        force=args.force,
        threshold=args.threshold,
        padding=args.padding
    )

if __name__ == "__main__":
    main()
