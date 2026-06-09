---
name: sjtuguoxue_space_web_api
version: 1.0.0
description: |
  南洋吟游（sjtuguoxue.space）公共 API。无需认证，可查询最新诗作、历史上的今天、经典推荐、搜索诗词。
  当用户提到南洋吟游、sjtuguoxue.space、查诗、搜诗、最新诗作、历史上的今天、经典推荐、
  随机推荐一首诗、搜索诗词时触发。
---

# 南洋吟游 · 公共 API

Base URL: `https://sjtuguoxue.space`

所有接口无需认证，直接 GET 请求即可。

## 接口一览

| 接口 | 说明 | 用途 |
|------|------|------|
| `GET /api/new_poem` | 最新诗作 | 获取平台最新发布的作品 |
| `GET /api/today_history` | 历史上的今天 | 获取往年今日发布的作品 |
| `GET /api/classic_recommend` | 经典推荐 | 基于关联度的作品推荐 |
| `GET /api/search/{keyword}` | 搜索诗词 | 按关键词全文搜索作品 |
| `GET /api/poem/{id}` | 获取单首作品 | 按 UUID 获取作品完整信息 |

## GET /api/new_poem

返回最新发布的一首诗作。

### 响应示例

```json
{
  "author": "祁水",
  "title": "浣溪沙",
  "sentence": "余生一万六千场。",
  "content": "春色无声去大荒。海天云气绿茫茫。余生一万六千场。\n恨欲空时看昨日，人流尽处作家乡。怀中箫剑已俱忘。",
  "date": "2026.6.1",
  "id": "b62c5719",
  "color": "#bb99dd"
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `author` | string | 作者笔名 |
| `title` | string | 作品标题 |
| `sentence` | string | 摘句（代表性的一句） |
| `content` | string | 完整正文，`\n` 分行 |
| `date` | string | 创作日期，`YYYY.M.D` 格式 |
| `id` | string | 作品 UUID（短） |
| `color` | string | 作品主题色（HEX） |

## GET /api/today_history

返回历史上的今天（同月同日）发布的一首作品，附当天总数。

### 响应示例

```json
{
  "author": "广寒居士",
  "title": "临江仙·咏荷花兼赠刘同学毕业二首（其一）",
  "sentence": "清啼侵晓新雨后，依依风举荷裙。",
  "date": "2025.6.9",
  "year": 2025,
  "total": 11,
  "id": "0abce72f",
  "color": "#bbffee"
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `author` | string | 作者笔名 |
| `title` | string | 作品标题 |
| `sentence` | string | 摘句 |
| `date` | string | 原始创作日期 |
| `year` | number | 创作年份 |
| `total` | number | 历史上的今天共有多少首作品 |
| `id` | string | 作品 UUID（短） |
| `color` | string | 作品主题色（HEX） |

## GET /api/classic_recommend

基于作品关联度的经典推荐，每次返回一首。

### 响应示例

```json
{
  "author": "张力夫",
  "title": "齐天乐 咏梅",
  "dynasty": "当代",
  "sentence": "露滋冰蕊铅华净。",
  "score": 0.8571,
  "source_author": "抱木",
  "source_id": "1b8d2343",
  "source_title": "倾杯吟（其十二）",
  "ok": true
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `author` | string | 推荐作品的作者 |
| `title` | string | 推荐作品标题 |
| `dynasty` | string | 作者年代（如 "当代"） |
| `sentence` | string | 摘句 |
| `score` | number | 关联度评分（0-1） |
| `source_author` | string | 推荐来源作者（基于这首诗的关联） |
| `source_id` | string | 来源作品 UUID |
| `source_title` | string | 来源作品标题 |
| `ok` | boolean | 请求是否成功 |

## GET /api/search/{keyword}

全文搜索诗词。底层逻辑是将每首诗的 id + title + author + content + date 拼成一个大字符串做子串匹配，硬限 30 条，无分页。

### 请求方式

两种等价写法：

```
GET /api/search/梅花              # 路径形式
GET /api/search/?q=梅花           # query 参数形式
```

### 参数

| 参数 | 位置 | 说明 |
|------|------|------|
| `{keyword}` | URL path | 搜索关键词（路径形式，与 `q` 等价） |
| `q` | query string | 搜索关键词（空格分隔 = AND） |
| `include_pending` | query string | 设为 `"true"` 时搜索审核中的稿件 |
| `exclude` | query string | 排除某个 poem ID |

### 搜索技巧

- **搜作者**：直接搜作者名即可，如 `/api/search/祁水`
- **搜作者+日期**：`/api/search/?q=林雨夜 2025`，空格为 AND 语义，可用于手动翻页
- **多词搜索**：`/api/search/?q=梅花 春`，同时包含"梅花"和"春"

### 响应示例

```json
{
  "results": [
    {
      "id": "e4f4fc7e",
      "poem_id": "e4f4fc7e",
      "snippet": "...一树梅花落绣床，三冬被里裹鸳鸯。甘饴蜜语风...",
      "text": "闺中作 - 林雨夜"
    },
    {
      "id": "7cfd776f",
      "poem_id": "7cfd776f",
      "snippet": "...。\n镜里驭回天栈绝，梅花曾落满南山。...",
      "text": "拆忠延《长相思》韵，得七绝一首和之 - 毛哥"
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `results` | array | 搜索结果列表 |
| `results[].id` | string | 作品 UUID（与 `poem_id` 相同） |
| `results[].poem_id` | string | 作品 UUID |
| `results[].snippet` | string | 关键词上下文片段 |
| `results[].text` | string | 格式为 `"标题 - 作者"`，需自行拆分 |

### 注意

- 硬限 30 条，无分页；结果较多时可通过追加作者/日期缩小范围
- `id` 和 `poem_id` 冗余（值相同）
- `text` 字段将标题和作者合并为 `"标题 - 作者"` 格式

---

## GET /api/poem/{id}

按 UUID 获取单首作品的完整信息。返回值为数组（非对象）。

### 请求

```
GET /api/poem/e4f4fc7e
```

### 响应示例

```json
["诗", "闺中作", "林雨夜", "2023.1.3", "一树梅花落绣床，三冬被里裹鸳鸯。\n甘饴蜜语风先醉，白雪澄心露未霜。\n紧拥冰肌酥入骨，微沾玉齿触回肠。\n从今永卧君怀抱，既暖何需衣与裳！", ["#流灯袅水"]]
```

### 字段说明（按数组下标）

| 下标 | 说明 |
|------|------|
| `[0]` | 类型（诗/词/现代韵文） |
| `[1]` | 标题 |
| `[2]` | 作者笔名 |
| `[3]` | 创作日期，`YYYY.M.D` 格式 |
| `[4]` | 完整正文，`\n` 分行 |
| `[5]` | 标签数组（带 `#` 前缀） |

---

## 调用示例

```bash
# 最新诗作
curl -s https://sjtuguoxue.space/api/new_poem | python3 -m json.tool

# 历史上的今天
curl -s https://sjtuguoxue.space/api/today_history | python3 -m json.tool

# 经典推荐
curl -s https://sjtuguoxue.space/api/classic_recommend | python3 -m json.tool

# 搜索诗词
curl -s 'https://sjtuguoxue.space/api/search/梅花' | python3 -m json.tool

# 获取单首作品
curl -s https://sjtuguoxue.space/api/poem/e4f4fc7e | python3 -m json.tool
```
