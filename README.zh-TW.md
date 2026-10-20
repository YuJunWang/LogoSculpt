# LogoSculpt

[English](README.md) | **繁體中文**

---

把有雜訊、低解析度、向量或帶有背景的商標（PNG / JPG / SVG / WEBP 等），批次轉換為極限貼齊邊界的純白向量 SVG 與 4K 透明 PNG。

---

## 快速開始

### 1. 安裝套件
需要 Python 3.10+：
```bash
pip install -r requirements.txt
```

### 2. 放入檔案
把要轉檔的圖片直接丟進 `input/` 資料夾（支援 SVG、PNG、JPG、WEBP、AVIF、GIF 等常見格式）。

### 3. 執行轉檔
* **Windows 使用者**：直接點擊 `run.bat`。
* **終端機指令**：
  ```bash
  python convert.py
  ```

### 4. 取得成果
輸出檔案會放在 `output/` 內，每個商標獨立建夾。直接用瀏覽器打開 `output/preview.html` 即可切換深色背景預覽並下載素材。

---

## 常用參數

```bash
# 強制重新處理已轉換過的檔案
python convert.py --force

# 自訂向量填色（預設純白 #FFFFFF，例如改為品牌金 #FFD700）
python convert.py --color "#FFD700"

# 調整邊界留白間距（預設 2.0px，貼齊內容極限）
python convert.py --padding 3.0

# 停用圖標與文字自動拆分（僅產出組合版）
python convert.py --no-split

# 自訂來源與輸出路徑
python convert.py -i "/path/to/input" -o "/path/to/output"
```

---

## 它自動處理了哪些爛圖問題？

不用進 Illustrator 手動鋼筆描邊，腳本會自動修復常見的來源瑕疵：

1. **截圖殘留黑邊**：自動偵測外圍 1~2px 裁切黑框並中和，避免背景被誤判為深色或產生額外方框。
2. **字體發胖與孔洞黏死**：自適應雙峰門檻與透明通道中位線校正，防止英文字母（`A`、`R`、`P`）和繁體字密部筆劃膨脹封閉。
3. **JPEG 壓縮噪點**：雙邊濾波加上連通面積過濾，清掉背景零碎雜斑，同時保留小寫字母 `i` 的圓點與標點符號。
4. **實物翻拍與印泥滲透**：色度防護機制，消除印泥陰刻線條內的浮動毛刺。
5. **彩度漸層保留**：具備 HSV 飽和度感應，明亮彩度漸層（如黃色、青色）不會被誤判為白色背景而消失。
6. **圖文自動分離**：符合橫式比例的商標自動拆成「完整版」、「獨立圖標 (Icon)」、「獨立標準字 (Text)」。

---

## 產出檔案清單

每個商標處理後會產出：

| 檔案名稱 | 說明 |
| :--- | :--- |
| `*_white_full.svg` | 完整向量版（極限貼齊 ViewBox，向量無限放大） |
| `*_white_full.png` | 原尺寸透明點陣圖（resvg 次像素渲染） |
| `*_white_full_4k.png` | 4K 超高解析透明點陣圖（長邊 $\ge 4000\text{px}$） |
| `*_white_icon.svg / .png` | 獨立圖標（長寬比符合且具備間隙時自動產出） |
| `*_white_text.svg / .png` | 獨立文字（長寬比符合且具備間隙時自動產出） |
| `output/preview.html` | 離線預覽看板，支援深黑、企業藍、棋盤格底色切換 |

---

## 授權

[MIT License](./LICENSE)
