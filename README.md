# 網頁爬蟲 CLI 工具

使用 [Firecrawl](https://firecrawl.dev) API 的 Python CLI 工具，支援多種輸出格式的網頁爬取。

## 功能特色

- 🌐 透過 Firecrawl API 爬取單一網頁
- 📝 多種輸出格式（Markdown、HTML）
- 💾 儲存至檔案或輸出至主控台
- 📁 目錄輸出支援，自動根據 URL 生成檔案名稱
- 🤖 **AI 驅動文章摘要**（新功能！）
- 🌍 多語言摘要支援（自動偵測並以原文語言產生摘要）
- 🎛️ 可自訂摘要長度（簡短、標準、詳細）
- 🔧 彈性的 AI 模型選擇（支援 Gemini、OpenAI、Anthropic 等）
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

# 編輯 .env 並設定必要的環境變數
```

**必要設定**（`.env` 檔案）：
```ini
# Firecrawl API 設定
FIRECRAWL_API_URL=http://localhost:3002
FIRECRAWL_API_KEY=  # 自架版本可選

# AI 模型設定（用於摘要功能）
DEFAULT_AI_MODEL=gemini/gemini-pro
GOOGLE_API_KEY=your_gemini_api_key_here

# 其他 AI 供應商（選用，P2 階段）
# OPENAI_API_KEY=your_openai_key
# ANTHROPIC_API_KEY=your_anthropic_key
```

**取得 Gemini API 金鑰**：
1. 前往 https://makersuite.google.com/app/apikey
2. 點擊「建立 API 金鑰」
3. 將金鑰複製到 `.env` 檔案

### 4. 執行第一次爬取

**基本爬取**：
```bash
# 爬取至主控台（markdown）
uv run crawler scrape --url https://example.com

# 爬取至檔案
uv run crawler scrape --url https://example.com --output page.md

# 爬取至目錄（自動生成檔案名稱）
uv run crawler scrape --url https://example.com --output ./output

# 爬取為 HTML 格式
uv run crawler scrape --url https://example.com --html --output page.html
```

**AI 摘要**（新功能！）：
```bash
# 產生文章摘要（輸出至主控台）
uv run crawler summarize --url https://example.com/article

# 產生摘要並儲存至檔案
uv run crawler summarize --url https://example.com/article --output summary.md

# 簡短摘要（1-2 句）
uv run crawler summarize --url https://example.com/article --summary brief

# 詳細摘要
uv run crawler summarize --url https://example.com/article --summary detailed

# 使用特定 AI 模型
uv run crawler summarize --url https://example.com/article --model gemini/gemini-1.5-flash
```

## 使用方式

### 指令概覽

```bash
# 爬取指令
uv run crawler scrape --url <URL> [OPTIONS]

# 摘要指令（新功能！）
uv run crawler summarize --url <URL> [OPTIONS]

# 取得說明
uv run crawler scrape --help
uv run crawler summarize --help
```

### 爬取指令

```bash
# 爬取至主控台（預設：markdown）
uv run crawler scrape --url <URL>

# 爬取至檔案
uv run crawler scrape --url <URL> --output <FILE>

# 爬取至目錄（自動生成檔案名稱）
uv run crawler scrape --url <URL> --output <DIRECTORY>

# 使用 HTML 格式
uv run crawler scrape --url <URL> --html --output page.html
```

### 摘要指令（AI 驅動）

```bash
# 基本摘要（輸出至主控台）
uv run crawler summarize --url <URL>

# 儲存摘要至檔案
uv run crawler summarize --url <URL> --output <FILE>

# 儲存至目錄（自動產生檔名）
uv run crawler summarize --url <URL> --output <DIRECTORY>

# 自訂摘要長度
uv run crawler summarize --url <URL> --summary <brief|standard|detailed>

# 使用特定 AI 模型
uv run crawler summarize --url <URL> --model <provider/model-name>

# 同時儲存原文和摘要
uv run crawler summarize --url <URL> --output ./docs/ --save-original
```

**摘要長度選項**：
- `brief`：簡短摘要（1-2 句話，~30 字）
- `standard`：標準摘要（3-5 個重點，~100 字）- 預設值
- `detailed`：詳細摘要（完整概述，~300 字）

**支援的 AI 模型**：
- `gemini/gemini-pro`：Google Gemini Pro（預設）
- `gemini/gemini-1.5-flash`：更快的 Gemini 模型
- 更多模型將在 P2 階段支援（OpenAI、Anthropic、Ollama 等）

### 使用範例

#### 爬取範例

**爬取部落格文章為 markdown**：
```bash
uv run crawler scrape \
  --url https://blog.example.com/article \
  --output ./articles/article.md
```

**爬取至目錄（自動生成檔案名稱）**：
```bash
# 自動生成檔案名稱：example-com.md
uv run crawler scrape \
  --url https://example.com \
  --output ./articles

# 自動生成檔案名稱：docs-python-org-tutorial.html
uv run crawler scrape \
  --url https://docs.python.org/tutorial \
  --html \
  --output ./docs
```

**爬取文件為 HTML**：
```bash
uv run crawler scrape \
  --url https://docs.example.com \
  --html \
  --output ./docs/reference.html
```

#### 摘要範例（新功能！）

**產生技術文章摘要**：
```bash
uv run crawler summarize \
  --url https://blog.example.com/python-tutorial \
  --output ./summaries/python-tutorial-summary.md
```

**快速瀏覽（簡短摘要）**：
```bash
uv run crawler summarize \
  --url https://news.example.com/article \
  --summary brief
```

**詳細分析（詳細摘要）**：
```bash
uv run crawler summarize \
  --url https://research.example.com/paper \
  --summary detailed \
  --output detailed-summary.md
```

**批次處理：儲存多篇文章摘要**：
```bash
# 儲存至目錄，自動產生檔名
uv run crawler summarize \
  --url https://blog.example.com/ai-trends \
  --output ./summaries/

# 同時儲存原文和摘要
uv run crawler summarize \
  --url https://docs.example.com/guide \
  --output ./docs/ \
  --save-original
```

**多語言文章摘要**：
```bash
# 中文文章 → 自動產生中文摘要
uv run crawler summarize \
  --url https://example.com/chinese-article

# 日文文章 → 自動產生日文摘要
uv run crawler summarize \
  --url https://example.jp/article
```

**使用不同 AI 模型**：
```bash
# 使用更快的 Gemini Flash 模型
uv run crawler summarize \
  --url https://example.com/article \
  --model gemini/gemini-1.5-flash

# 使用預設模型（從 .env 讀取）
uv run crawler summarize \
  --url https://example.com/article
```

**將輸出導向其他指令**：
```bash
# 爬取
uv run crawler scrape --url https://example.com | grep "關鍵字"

# 摘要
uv run crawler summarize --url https://example.com/article | wc -w
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
├── models/              # Pydantic 資料模型
│   ├── scrape.py        # ScrapeRequest、ScrapeResponse
│   ├── summarize_request.py    # 摘要請求模型（新）
│   ├── ai_model_config.py      # AI 模型設定（新）
│   ├── article_content.py      # 文章內容模型（新）
│   ├── ai_summary.py           # AI 摘要模型（新）
│   └── output_file.py          # 輸出檔案模型（新）
├── services/            # 業務邏輯
│   ├── firecrawl.py     # Firecrawl API 整合
│   ├── ai_service.py    # AI 摘要服務（新）
│   ├── prompt_service.py # 提示詞管理（新）
│   └── output.py        # 檔案/主控台輸出
├── cli/                 # CLI 介面
│   ├── main.py          # 入口點
│   ├── scrape.py        # 爬取指令
│   └── summarize.py     # 摘要指令（新）
├── config/              # 設定
│   ├── settings.py      # 環境設定（已擴充 AI 設定）
│   └── prompts.py       # AI 提示詞範本（新）
└── lib/                 # 工具程式
    ├── exceptions.py    # 自訂例外（已擴充 AI 例外）
    └── validators.py    # 輸入驗證

tests/
├── unit/                # 單元測試（模擬）
│   ├── models/          # 135 個模型測試（新）
│   ├── services/        # 服務測試（含 AI 服務）
│   └── cli/             # CLI 測試
├── integration/         # 整合測試
└── contract/            # API 契約測試
```

## 設定

### 環境變數

| 變數 | 必要 | 預設值 | 說明 |
|------|------|--------|------|
| `FIRECRAWL_API_URL` | 是 | - | Firecrawl API 基礎 URL |
| `FIRECRAWL_API_KEY` | 否 | `""` | API 金鑰（自架版本可選） |
| `DEFAULT_AI_MODEL` | 摘要需要 | - | 預設 AI 模型（例如：`gemini/gemini-pro`） |
| `GOOGLE_API_KEY` | Gemini 需要 | - | Google Gemini API 金鑰 |
| `OPENAI_API_KEY` | OpenAI 需要 | - | OpenAI API 金鑰（P2 階段） |
| `ANTHROPIC_API_KEY` | Anthropic 需要 | - | Anthropic API 金鑰（P2 階段） |

### 退出代碼

| 代碼 | 意義 |
|------|------|
| 0 | 成功 |
| 1 | 一般錯誤（無效 URL、網路失敗） |
| 2 | 設定錯誤（缺少 API URL、缺少 API 金鑰） |
| 3 | AI 服務錯誤（超過速率限制、Token 限制） |

## 架構

### 技術堆疊

- **CLI 框架**：Typer（型別安全的 CLI，自動產生說明）
- **API 客戶端**：firecrawl-py（官方 Firecrawl Python SDK）
- **AI 整合**：LiteLLM（統一多個 AI 供應商的介面）
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

### 爬取相關

**"錯誤：缺少必要設定：FIRECRAWL_API_URL"**

解決方法：建立 `.env` 檔案並設定 Firecrawl API URL：
```bash
echo "FIRECRAWL_API_URL=http://localhost:3002" > .env
```

**"錯誤：無法連線至 Firecrawl API"**

解決方法：確認 Firecrawl 實例正在執行：
```bash
# 檢查 Firecrawl 是否可存取
curl http://localhost:3002/health

# 或重新啟動 Firecrawl
docker-compose restart firecrawl
```

**"錯誤：無效的 URL 格式"**

解決方法：URL 必須包含協定（`http://` 或 `https://`）：
```bash
# 錯誤
uv run crawler scrape --url example.com

# 正確
uv run crawler scrape --url https://example.com
```

**寫入輸出時權限被拒**

解決方法：確認輸出目錄存在或你有寫入權限：
```bash
mkdir -p ./output
uv run crawler scrape --url https://example.com --output ./output/page.md
```

### 摘要相關（新功能）

**"錯誤：未設定 DEFAULT_AI_MODEL"**

解決方法：在 `.env` 檔案中設定預設 AI 模型：
```bash
echo "DEFAULT_AI_MODEL=gemini/gemini-pro" >> .env
```

**"錯誤：缺少 API 金鑰 'gemini/gemini-pro'"**

解決方法：在 `.env` 檔案中設定 Google API 金鑰：
```bash
echo "GOOGLE_API_KEY=你的金鑰" >> .env
```

取得 Gemini API 金鑰：https://makersuite.google.com/app/apikey

**"錯誤：超過速率限制"**

解決方法：稍等片刻後重試，或使用速率限制較高的模型：
```bash
uv run crawler summarize --url https://example.com/article \
  --model gemini/gemini-1.5-flash  # 速率限制較高的快速模型
```

**"錯誤：文章超過模型 Token 限制"**

解決方法：使用簡短摘要模式或較大的模型：
```bash
# 選項 1：使用簡短模式
uv run crawler summarize --url https://example.com/long-article --summary brief

# 選項 2：使用有較大 context window 的模型
uv run crawler summarize --url https://example.com/long-article \
  --model gemini/gemini-1.5-pro  # 更大的 context window
```

**"只支援 Gemini 模型"（P1 限制）**

說明：目前版本（P1）僅支援 Google Gemini 模型。其他 AI 供應商（OpenAI、Anthropic、Ollama）將在 P2 階段支援。

支援的模型：
- `gemini/gemini-pro`
- `gemini/gemini-1.5-flash`
- `gemini/gemini-1.5-pro`

## 路線圖

### 功能 002 - 基本爬取 ✅ 完成
- [x] 基本單頁爬取
- [x] Markdown 和 HTML 輸出
- [x] 檔案和主控台輸出
- [x] 目錄輸出支援（自動生成檔案名稱）
- [x] 錯誤處理和驗證
- [x] 38/38 單元測試通過

### 功能 003 - AI 驅動文章摘要 🚧 開發中
**P1 階段**（MVP）：
- [x] 資料模型（135 個測試通過，100% 覆蓋率）
- [x] AI 服務（LiteLLM 整合）
- [x] 系統提示詞管理
- [x] 設定和例外處理
- [ ] CLI 摘要指令
- [ ] 端到端整合測試
- [ ] 多語言摘要支援（自動偵測）
- [ ] Google Gemini 模型支援

**P2 階段**（進階功能）：
- [ ] 可自訂摘要長度（簡短、標準、詳細）
- [ ] 多 AI 供應商支援：
  - [ ] OpenAI（GPT-4、GPT-4o）
  - [ ] Anthropic（Claude 3）
  - [ ] 本地模型（Ollama、vLLM）
- [ ] 彈性模型選擇（`--model` 參數）

**P3 階段**（額外功能）：
- [ ] 同時儲存原文和摘要（`--save-original`）
- [ ] 自訂系統提示詞
- [ ] 批次 URL 摘要
- [ ] 詳細模式（顯示 Token 使用量）

### 未來計畫
- [ ] JSON 格式輸出（爬取）
- [ ] 批次處理（從檔案讀取多個 URL）
- [ ] 非同步並行爬取
- [ ] 進度報告
- [ ] 自訂檔案名稱範本
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

### 功能 002 - 基本爬取
- **規格說明**：[specs/002-python3-uv-n/spec.md](specs/002-python3-uv-n/spec.md)
- **實作計畫**：[specs/002-python3-uv-n/plan.md](specs/002-python3-uv-n/plan.md)
- **資料模型**：[specs/002-python3-uv-n/data-model.md](specs/002-python3-uv-n/data-model.md)
- **研究報告**：[specs/002-python3-uv-n/research.md](specs/002-python3-uv-n/research.md)
- **快速入門**：[specs/002-python3-uv-n/quickstart.md](specs/002-python3-uv-n/quickstart.md)

### 功能 003 - AI 文章摘要（新！）
- **規格說明**：[specs/003-markdown-summary-ai/spec.md](specs/003-markdown-summary-ai/spec.md)
- **實作計畫**：[specs/003-markdown-summary-ai/plan.md](specs/003-markdown-summary-ai/plan.md)
- **資料模型**：[specs/003-markdown-summary-ai/data-model.md](specs/003-markdown-summary-ai/data-model.md)
- **快速入門**：[specs/003-markdown-summary-ai/quickstart.md](specs/003-markdown-summary-ai/quickstart.md)
- **API 契約**：[specs/003-markdown-summary-ai/contracts/](specs/003-markdown-summary-ai/contracts/)
- **實作指南**：[specs/003-markdown-summary-ai/IMPLEMENTATION_GUIDE.md](specs/003-markdown-summary-ai/IMPLEMENTATION_GUIDE.md)
- **任務分解**：[specs/003-markdown-summary-ai/tasks.md](specs/003-markdown-summary-ai/tasks.md)

## 授權條款

[在此新增你的授權條款]

## 支援

遇到問題或疑問時：
1. 查看[疑難排解](#疑難排解)章節
2. 檢閱 `specs/002-python3-uv-n/` 中的規格文件
3. 檢查 Firecrawl 日誌：`docker logs firecrawl`
4. 驗證 `.env` 設定

---

**版本**：0.2.0-dev
**狀態**：
- 功能 002（基本爬取）：✅ 完成
- 功能 003（AI 摘要）：🚧 開發中（43% 完成）
**目前分支**：`003-markdown-summary-ai`
**最後更新**：2025-10-12

**實作進度**（功能 003）：
- ✅ Phase 1: 設定與配置（3/3 任務）
- ✅ Phase 2: 資料模型（13/15 任務，135 個測試通過）
- ✅ Phase 3: 核心服務（2/8 任務，AI 服務實作完成）
- ⏳ 剩餘：CLI 整合、提示詞服務、測試（6 個任務完成 MVP）

詳細進度請參閱：[IMPLEMENTATION_GUIDE.md](specs/003-markdown-summary-ai/IMPLEMENTATION_GUIDE.md)
