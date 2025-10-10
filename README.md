# 網頁爬蟲 CLI 工具

使用 [Firecrawl](https://firecrawl.dev) API 的 Python CLI 工具，支援多種輸出格式的網頁爬取。

## 功能特色

- 🌐 透過 Firecrawl API 爬取單一網頁
- 📝 多種輸出格式（Markdown、HTML）
- 💾 儲存至檔案或輸出至主控台
- ⚡ 快速可靠，具備完善的錯誤處理
- 🔒 使用 Pydantic 模型確保型別安全
- ✅ 核心功能 100% 測試覆蓋率
- 🎯 測試驅動開發（TDD）

## 系統需求

- **Python**：3.10 或更高版本
- **套件管理器**：[UV](https://docs.astral.sh/uv/)（必要）
- **Firecrawl 實例**：自架 Firecrawl API 伺服器

## 快速開始

### 1. 安裝 UV（如果尚未安裝）

**Windows (PowerShell)**：
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux**：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 複製專案並設定

```bash
git clone <repository-url>
cd crawler
git checkout 002-python3-uv-n

# 建立虛擬環境
uv venv

# 啟動虛擬環境
# Windows (PowerShell)：
.venv\Scripts\Activate.ps1
# macOS/Linux：
source .venv/bin/activate

# 安裝依賴項
uv pip install -e ".[dev]"
```

### 3. 設定環境變數

```bash
# 複製範例設定檔
cp .env.example .env

# 編輯 .env 並設定你的 Firecrawl API URL
# FIRECRAWL_API_URL=http://localhost:3002
# FIRECRAWL_API_KEY=  # 自架版本可選
```

### 4. 執行第一次爬取

```bash
# 爬取至主控台（markdown）
uv run crawler scrape --url https://example.com

# 爬取至檔案
uv run crawler scrape --url https://example.com --output page.md

# 爬取為 HTML 格式
uv run crawler scrape --url https://example.com --html --output page.html
```

## 使用方式

### 基本指令

```bash
# 取得說明
uv run crawler scrape --help

# 爬取至主控台（預設：markdown）
uv run crawler scrape --url <URL>

# 爬取至檔案
uv run crawler scrape --url <URL> --output <FILE>

# 使用 HTML 格式
uv run crawler scrape --url <URL> --html --output page.html
```

### 使用範例

**爬取部落格文章為 markdown**：
```bash
uv run crawler scrape \
  --url https://blog.example.com/article \
  --output ./articles/article.md
```

**爬取文件為 HTML**：
```bash
uv run crawler scrape \
  --url https://docs.example.com \
  --html \
  --output ./docs/reference.html
```

**將輸出導向其他指令**：
```bash
uv run crawler scrape --url https://example.com | grep "關鍵字"
```

## 開發

### 執行測試

```bash
# 執行所有單元測試
uv run pytest tests/unit -v

# 執行測試並產生覆蓋率報告
uv run pytest tests/unit --cov=src --cov-report=html

# 執行特定測試檔案
uv run pytest tests/unit/test_models.py -v

# 執行整合測試（需要 Firecrawl 實例）
uv run pytest tests/integration -v

# 執行契約測試
uv run pytest tests/contract -v -m contract
```

### 程式碼品質

```bash
# 格式化程式碼
uv run ruff format src/ tests/

# 檢查程式碼
uv run ruff check src/ tests/

# 型別檢查
uv run mypy src/ --strict

# 安全性掃描
uv run bandit -r src/
```

### 專案架構

```
src/
├── models/          # Pydantic 資料模型
│   └── scrape.py    # ScrapeRequest、ScrapeResponse 等
├── services/        # 業務邏輯
│   ├── firecrawl.py # Firecrawl API 整合
│   └── output.py    # 檔案/主控台輸出
├── cli/             # CLI 介面
│   ├── main.py      # 入口點
│   └── scrape.py    # 爬取指令
├── config/          # 設定
│   └── settings.py  # 環境設定
└── lib/             # 工具程式
    ├── exceptions.py # 自訂例外
    └── validators.py # 輸入驗證

tests/
├── unit/            # 單元測試（模擬）
├── integration/     # 整合測試
└── contract/        # API 契約測試
```

## 設定

### 環境變數

| 變數 | 必要 | 預設值 | 說明 |
|------|------|--------|------|
| `FIRECRAWL_API_URL` | 是 | - | Firecrawl API 基礎 URL |
| `FIRECRAWL_API_KEY` | 否 | `""` | API 金鑰（自架版本可選） |

### 退出代碼

| 代碼 | 意義 |
|------|------|
| 0 | 成功 |
| 1 | 一般錯誤（無效 URL、網路失敗） |
| 2 | 設定錯誤（缺少 API URL） |
| 3 | 超過速率限制 |

## 架構

### 技術堆疊

- **CLI 框架**：Typer（型別安全的 CLI，自動產生說明）
- **API 客戶端**：firecrawl-py（官方 Firecrawl Python SDK）
- **資料驗證**：Pydantic v2（執行期型別檢查）
- **設定管理**：python-dotenv + pydantic-settings
- **測試**：pytest + pytest-cov + pytest-mock
- **程式碼品質**：ruff（檢查/格式化）+ mypy（型別檢查）+ bandit（安全性）

### 設計原則

遵循專案規範（`.specify/memory/constitution.md`）：

1. **Python 3.10+ 標準**：現代 Python 與型別提示
2. **UV 套件管理**：快速、可靠的依賴項管理（不可協商）
3. **測試驅動開發**：所有程式碼都先寫測試（不可協商）
4. **整合測試**：真實 API 和檔案系統測試
5. **程式碼品質**：80%+ 覆蓋率、嚴格型別檢查、完整文件

## 疑難排解

### "錯誤：缺少必要設定：FIRECRAWL_API_URL"

**解決方法**：建立 `.env` 檔案並設定 Firecrawl API URL：
```bash
echo "FIRECRAWL_API_URL=http://localhost:3002" > .env
```

### "錯誤：無法連線至 Firecrawl API"

**解決方法**：確認 Firecrawl 實例正在執行：
```bash
# 檢查 Firecrawl 是否可存取
curl http://localhost:3002/health

# 或重新啟動 Firecrawl
docker-compose restart firecrawl
```

### "錯誤：無效的 URL 格式"

**解決方法**：URL 必須包含協定（`http://` 或 `https://`）：
```bash
# 錯誤
uv run crawler scrape --url example.com

# 正確
uv run crawler scrape --url https://example.com
```

### 寫入輸出時權限被拒

**解決方法**：確認輸出目錄存在或你有寫入權限：
```bash
mkdir -p ./output
uv run crawler scrape --url https://example.com --output ./output/page.md
```

## 路線圖

### 階段 1（P1）- MVP ✅ 完成
- [x] 基本單頁爬取
- [x] Markdown 和 HTML 輸出
- [x] 檔案和主控台輸出
- [x] 錯誤處理和驗證
- [x] 38/38 單元測試通過

### 階段 2（P2）- 額外格式
- [ ] JSON 格式輸出
- [ ] 純文字格式輸出
- [ ] 格式特定選項

### 階段 3（P3）- 批次處理
- [ ] 從檔案爬取多個 URL
- [ ] 非同步並行爬取（50+ URLs）
- [ ] 進度報告
- [ ] 批次錯誤處理

### 階段 4（P3）- 進階功能
- [ ] 自訂檔案名稱範本
- [ ] 輸出目錄組織
- [ ] 指數退避重試邏輯

## 貢獻

### 開發工作流程（TDD）

1. **先寫測試**（RED 階段）
   ```bash
   # 在 tests/unit/test_feature.py 建立測試
   uv run pytest tests/unit/test_feature.py
   # 驗證失敗
   ```

2. **實作最少程式碼**（GREEN 階段）
   ```bash
   # 在 src/ 中加入實作
   uv run pytest tests/unit/test_feature.py
   # 驗證通過
   ```

3. **重構**，保持測試通過
   ```bash
   uv run pytest tests/unit -v
   # 所有測試應該仍然通過
   ```

4. **提交**完整週期後
   ```bash
   git add .
   git commit -m "feat: 使用 TDD 新增功能 X"
   ```

### 品質檢查清單

提交變更前：

- [ ] 所有測試通過：`uv run pytest -v`
- [ ] 覆蓋率 ≥80%：`uv run pytest --cov=src --cov-fail-under=80`
- [ ] 型別檢查通過：`uv run mypy src/ --strict`
- [ ] 程式檢查通過：`uv run ruff check src/`
- [ ] 程式碼已格式化：`uv run ruff format src/`
- [ ] 無安全性問題：`uv run bandit -r src/`

## 文件

- **規格說明**：[specs/002-python3-uv-n/spec.md](specs/002-python3-uv-n/spec.md)
- **實作計畫**：[specs/002-python3-uv-n/plan.md](specs/002-python3-uv-n/plan.md)
- **資料模型**：[specs/002-python3-uv-n/data-model.md](specs/002-python3-uv-n/data-model.md)
- **研究報告**：[specs/002-python3-uv-n/research.md](specs/002-python3-uv-n/research.md)
- **快速入門**：[specs/002-python3-uv-n/quickstart.md](specs/002-python3-uv-n/quickstart.md)

## 授權條款

[在此新增你的授權條款]

## 支援

遇到問題或疑問時：
1. 查看[疑難排解](#疑難排解)章節
2. 檢閱 `specs/002-python3-uv-n/` 中的規格文件
3. 檢查 Firecrawl 日誌：`docker logs firecrawl`
4. 驗證 `.env` 設定

---

**版本**：0.1.0
**狀態**：MVP 完成（階段 1）
**分支**：`002-python3-uv-n`
**最後更新**：2025-10-10
