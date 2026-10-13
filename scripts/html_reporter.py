"""
html_reporter.py
自動掃描 output/ 資料夾內的所有產出資產，生成美觀且具備即時底色切換功能之預覽看板 (preview.html)
"""

import os
import glob

def generate_preview_html(output_root: str, html_file_path: str):
    subdirs = [d for d in os.listdir(output_root) if os.path.isdir(os.path.join(output_root, d))]
    cards_html = []
    
    for folder in sorted(subdirs):
        folder_path = os.path.join(output_root, folder)
        
        # 彈性搜尋 full.svg
        full_svg_candidates = glob.glob(os.path.join(folder_path, "*white*full*.svg")) + \
                              glob.glob(os.path.join(folder_path, "*full*.svg")) + \
                              glob.glob(os.path.join(folder_path, "*.svg"))
        if not full_svg_candidates:
            continue
            
        full_svg = full_svg_candidates[0]
        full_svg_name = os.path.basename(full_svg)
        
        # 搜尋 icon 與 text svg
        icon_candidates = glob.glob(os.path.join(folder_path, "*icon*.svg"))
        text_candidates = glob.glob(os.path.join(folder_path, "*text*.svg"))
        color_candidates = glob.glob(os.path.join(folder_path, "*color*.svg"))
        
        with open(full_svg, "r", encoding="utf-8") as f:
            full_svg_content = f.read()
            
        has_icon = len(icon_candidates) > 0
        has_text = len(text_candidates) > 0
        has_color = len(color_candidates) > 0
        
        icon_svg_content = ""
        icon_svg_name = ""
        if has_icon:
            icon_svg_name = os.path.basename(icon_candidates[0])
            with open(icon_candidates[0], "r", encoding="utf-8") as f:
                icon_svg_content = f.read()
                
        text_svg_content = ""
        text_svg_name = ""
        if has_text:
            text_svg_name = os.path.basename(text_candidates[0])
            with open(text_candidates[0], "r", encoding="utf-8") as f:
                text_svg_content = f.read()
                
        # 搜尋 PNG 檔案
        full_pngs = glob.glob(os.path.join(folder_path, "*white*full*.png")) + glob.glob(os.path.join(folder_path, "*full*.png"))
        std_png_name = os.path.basename(full_pngs[0]) if full_pngs else ""
        png_4k_candidates = [p for p in full_pngs if "4k" in p.lower()]
        png_4k_name = os.path.basename(png_4k_candidates[0]) if png_4k_candidates else ""
        
        card_content = f'''
        <div class="asset-card">
          <div class="card-header">
            <div class="asset-name">📁 {folder}</div>
            <div class="badge-group">
              <span class="badge">完整純白版</span>
              {'<span class="badge badge-sub">圖標版</span>' if has_icon else ''}
              {'<span class="badge badge-sub">標準字版</span>' if has_text else ''}
              {'<span class="badge" style="background:#059669;">原色版</span>' if has_color else ''}
            </div>
          </div>
          
          <!-- 完整版預覽 -->
          <div class="preview-stage bg-dark" id="stage-{folder}-full">
            <div class="svg-container full-view">
              {full_svg_content}
            </div>
          </div>
          
          <div class="download-bar">
            <span>向量檔：<a href="{folder}/{full_svg_name}" download>{full_svg_name}</a></span>
            <span>透明點陣：{f'<a href="{folder}/{std_png_name}" download>標準 (1x)</a>' if std_png_name else ''} {f'| <a href="{folder}/{png_4k_name}" download>超清 (4K)</a>' if png_4k_name else ''}</span>
          </div>
        '''
        
        if has_icon or has_text:
            card_content += '<div class="split-row">'
            if has_icon:
                card_content += f'''
                <div class="split-col">
                  <div class="split-label">獨立標誌 (Icon)</div>
                  <div class="preview-stage split-stage bg-dark" id="stage-{folder}-icon">
                    <div class="svg-container icon-view">
                      {icon_svg_content}
                    </div>
                  </div>
                  <div class="download-bar">
                    <a href="{folder}/{icon_svg_name}" download>{icon_svg_name}</a>
                  </div>
                </div>
                '''
            if has_text:
                card_content += f'''
                <div class="split-col">
                  <div class="split-label">獨立標準字 (Text)</div>
                  <div class="preview-stage split-stage bg-dark" id="stage-{folder}-text">
                    <div class="svg-container text-view">
                      {text_svg_content}
                    </div>
                  </div>
                  <div class="download-bar">
                    <a href="{folder}/{text_svg_name}" download>{text_svg_name}</a>
                  </div>
                </div>
                '''
            card_content += '</div>'
            
        card_content += '</div>'
        cards_html.append(card_content)
        
    all_cards = "\n".join(cards_html) if cards_html else '<p style="text-align:center;color:#64748b;padding:40px;">目前 output 資料夾尚無處理成果，請將圖片放入 input 並執行工作流程。</p>'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>向量化轉換專案預覽看板 (PNG to SVG Asset Gallery)</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Microsoft JhengHei", sans-serif;
    background-color: #0b1120;
    color: #e2e8f0;
    padding: 30px 20px;
  }}
  .container {{ max-width: 1040px; margin: 0 auto; }}
  header {{ margin-bottom: 25px; }}
  h1 {{ font-size: 24px; color: #f8fafc; margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }}
  p.desc {{ color: #94a3b8; font-size: 14px; }}
  
  .toolbar {{
    background: #1e293b;
    border: 1px solid #334155;
    padding: 12px 18px;
    border-radius: 10px;
    margin-bottom: 25px;
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
  }}
  .toolbar-label {{ font-size: 13px; font-weight: 600; color: #cbd5e1; }}
  .btn-theme {{
    background: #334155;
    color: #f1f5f9;
    border: 1px solid #475569;
    padding: 6px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
    transition: all 0.2s;
  }}
  .btn-theme:hover {{ background: #475569; }}
  .btn-theme.active {{ background: #38bdf8; color: #0f172a; font-weight: 700; border-color: #38bdf8; }}
  
  .asset-card {{
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 22px;
    margin-bottom: 24px;
  }}
  .card-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
  }}
  .asset-name {{ font-size: 17px; font-weight: 700; color: #f8fafc; font-family: monospace; }}
  .badge-group {{ display: flex; gap: 6px; }}
  .badge {{
    font-size: 11px;
    padding: 3px 8px;
    border-radius: 12px;
    background: #0284c7;
    color: #fff;
    font-weight: 600;
  }}
  .badge-sub {{ background: #334155; color: #cbd5e1; border: 1px solid #475569; }}
  
  .preview-stage {{
    border-radius: 8px;
    padding: 24px 16px;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: background-color 0.25s;
    min-height: 120px;
    overflow: hidden;
  }}
  
  /* Themes */
  .bg-dark {{ background-color: #0b1120; }}
  .bg-navy {{ background-color: #1e3a8a; }}
  .bg-charcoal {{ background-color: #27272a; }}
  .bg-checkers {{
    background-color: #ffffff;
    background-image: 
      linear-gradient(45deg, #e2e8f0 25%, transparent 25%), 
      linear-gradient(-45deg, #e2e8f0 25%, transparent 25%), 
      linear-gradient(45deg, transparent 75%, #e2e8f0 75%), 
      linear-gradient(-45deg, transparent 75%, #e2e8f0 75%);
    background-size: 16px 16px;
    background-position: 0 0, 0 8px, 8px -8px, -8px 0px;
  }}
  
  .svg-container svg {{ display: block; max-width: 100%; height: auto; }}
  .svg-container.full-view svg {{ max-height: 110px; }}
  .svg-container.icon-view svg {{ max-height: 80px; }}
  .svg-container.text-view svg {{ max-height: 70px; }}
  
  .download-bar {{
    margin-top: 10px;
    font-size: 12px;
    color: #94a3b8;
    display: flex;
    justify-content: space-between;
    font-family: monospace;
    padding: 0 4px;
  }}
  .download-bar a {{ color: #38bdf8; text-decoration: none; font-weight: 600; }}
  .download-bar a:hover {{ text-decoration: underline; }}
  
  .split-row {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 16px;
    padding-top: 14px;
    border-top: 1px dashed #334155;
  }}
  .split-label {{ font-size: 12px; color: #94a3b8; margin-bottom: 6px; font-weight: 600; }}
  .split-stage {{ min-height: 90px; padding: 14px; }}
  @media (max-width: 640 {{
    .split-row {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>⚡ 向量化去背專案成果看板 (Asset Gallery)</h1>
    <p class="desc">所有已處理之純白向量 SVG、透明 PNG 與自動分離組件均已收錄於此，支援即時切換各類底色檢視效果。</p>
  </header>
  
  <div class="toolbar">
    <span class="toolbar-label">預覽底色切換：</span>
    <button class="btn-theme active" onclick="setTheme('bg-dark')">深黑 (#0b1120)</button>
    <button class="btn-theme" onclick="setTheme('bg-navy')">企業深藍 (#1e3a8a)</button>
    <button class="btn-theme" onclick="setTheme('bg-charcoal')">極簡碳灰 (#27272a)</button>
    <button class="btn-theme" onclick="setTheme('bg-checkers')">透明棋盤格</button>
  </div>
  
  <div id="assets-list">
    {all_cards}
  </div>
</div>

<script>
  function setTheme(cls) {{
    const stages = document.querySelectorAll('.preview-stage');
    stages.forEach(st => {{
      st.classList.remove('bg-dark', 'bg-navy', 'bg-charcoal', 'bg-checkers');
      st.classList.add(cls);
    }});
    document.querySelectorAll('.btn-theme').forEach(btn => {{
      btn.classList.remove('active');
      if (btn.getAttribute('onclick').includes(cls)) {{
        btn.classList.add('active');
      }}
    }});
  }}
</script>
</body>
</html>
'''
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(html)
    return html_file_path
