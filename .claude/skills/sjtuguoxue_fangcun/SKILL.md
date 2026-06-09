---
name: sjtuguoxue_fangcun
version: 1.0.0
description: |
  方寸：国学社诗词创作画布，实时格律校验、韵部查询、词语联想、典故检索。
  提供在线使用、API 调用、CLI 和本地开发四种方式。
  当用户提到方寸、格律检测、诗词校验、韵部查询、典故检索、
  write.sjtuguoxue.space、checker.sjtuguoxue.space、fangcun 时触发。
---

# 方寸 · 诗词创作画布

古典诗词创作工具。实时格律校验、韵部查询、词语联想、典故检索，一页完成查韵选词填字出图。

## 核心功能

- **格律校验** — 五/七言律诗绝句 + 2500+ 词牌，实时标注平仄错误与韵脚问题
- **韵部查询** — 平水韵 / 词林正韵 / 中华通韵，按词频排序，邻韵关联
- **字典联想** — 词首、词末、对仗、同位语查询，80 万首古诗词语料
- **典故检索** — 1.3 万条典故，按匹配度排序
- **导入诗词** — 搜索并导入历代诗词（80 万首），自动匹配格律
- **导出图片** — 33 款主题诗词卡片，2x 高清输出

## 入口

| 方式 | 地址 | 说明 |
|------|------|------|
| 在线使用 | https://write.sjtuguoxue.space | 网页端创作画布 |
| 格律检测服务 | https://checker.sjtuguoxue.space | 独立格律检测 API |
| API 文档 | https://write.sjtuguoxue.space/docs | 全部接口文档 |
| Android APK | [GitHub Releases](https://github.com/lyy0323/fangcun/releases/latest) | 离线词库 + 线上格律检测 |
| 源码仓库 | https://github.com/lyy0323/fangcun | 本地开发，提 PR 贡献 |

## API 速查

### 格律检测（无需认证）

```bash
curl -X POST https://write.sjtuguoxue.space/api/validate_meter \
  -H "Content-Type: application/json" \
  -d '{"poem_text":"床前明月光，疑是地上霜。举头望明月，低头思故乡。","genre":"Shi"}'
```

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/validate_meter` | POST | 格律检测（诗/词） |
| `/api/free_rhyme` | POST | 自由韵脚检测（古体/自由诗） |
| `/api/char/batch` | POST | 批量字音查询 |
| `/api/char/lookup` | GET | 单字音韵查询 |
| `/api/rhyme/lookup` | GET | 韵部同韵字 |
| `/api/rhyme/list` | GET | 韵部列表 |
| `/api/rules/list` | GET | 格律规则列表 |

### 词库服务

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/char/definitions` | GET | 单字释义 |
| `/api/dictionary/search` | GET | 词首/词末/对语/同位语查询 |
| `/api/dictionary/allusion` | GET | 典故检索 |

## CLI

```bash
pip install -e .   # 从源码安装

fangcun validate --text "白日依山尽，黄河入海流。" --genre Shi
fangcun char --char 明月 --book Pingshuiyun
fangcun rhyme --book Pingshuiyun --category 一东
fangcun suggest --term 明月 --mode pair --with-tones
fangcun free-rhyme --text "卖炭翁，伐薪烧炭南山中。" --pretty
```

CLI 调用线上 checker 服务，零本地依赖。可通过 `FANGCUN_CHECKER_URL` / `FANGCUN_DICT_URL` 环境变量指向自建服务。

## 本地开发

```bash
git clone https://github.com/lyy0323/fangcun.git
cd fangcun

# 后端（释义 + 词库服务）
pip install -r requirements.txt
python app.py                    # Flask on :5050

# 前端
cd frontend && npm install
npm run dev                      # Vite on :3000，格律请求代理到线上 checker
```

格律检测由 checker.sjtuguoxue.space 提供，本地开发无需额外启动。开发完成后提 PR 到 lyy0323/fangcun。

## 技术栈

React 19 + TypeScript + Vite + Tailwind CSS 4 | Python Flask | Neon PostgreSQL | Vercel Serverless | Android (Chaquopy + WebView)

## License

AGPL-3.0，导出图片中的水印须保留。
