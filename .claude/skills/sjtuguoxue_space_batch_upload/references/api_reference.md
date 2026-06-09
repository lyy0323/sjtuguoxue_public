# 南洋吟游 · 作品上传 API

Base URL: `https://sjtuguoxue.space`

## 认证

所有 API 请求需要在请求头中携带 API Key：

```
Authorization: Bearer sk-nyyy-xxxxxxxxxxxx
```

API Key 可在登录后访问 [个人中心](/profile/) 查看。

---

## POST /api/submit/

提交一首作品到审核队列。提交后作品状态为 `pending`，需管理员审核通过后发布。

### 请求

```
POST /api/submit/
Content-Type: application/json
Authorization: Bearer sk-nyyy-xxxxxxxxxxxx
```

### 请求体

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `author` | string | 是 | 作者笔名（如 `"林雨夜"`）或数字编号（如 `"10"`） |
| `title` | string | 是 | 作品标题 |
| `content` | string | 是 | 正文。诗两句一行，词一阕一段，用 `\n` 分行 |
| `date` | string | 是 | 创作日期，尽可能精确：`YYYY.M.D`（如 `"2026.5.5"`）、`YYYY.M`（如 `"2026.5"`）、`YYYY`（如 `"2026"`） |
| `type` | string | 否 | `"诗"` / `"词"` / `"现代韵文"`。省略则根据标题自动推断 |
| `genre` | string | 否 | 体裁（如 `"七律"` / `"浣溪沙"`）。省略则自动检测 |
| `legacy_id` | string \| null | 否 | 作品编号。省略或 `"auto"` = 自动计算；`null` = 不分配编号；传入具体值 = 使用该编号 |
| `preface` | string | 否 | 序 |
| `footnote` | string | 否 | 脚注 |
| `tags` | array\<string\> | 否 | 标签列表。`#` 前缀可省略，如 `["次韵", "清明"]` |
| `relations` | array\<object\> | 否 | 关联作品列表。每项包含 `id`（UUID 或旧编号）和 `type`（关系类型） |

关系类型（`relations[].type`）：
- `"story"` — 本事/故事
- `"reply"` — 酬答/次韵
- `"sequence"` — 组诗/序列
- `"quote"` — 引用/集句

### 示例请求

**最简提交（仅必填字段）：**

```json
{
  "author": "林雨夜",
  "title": "无题",
  "content": "平平仄仄平平仄，仄仄平平仄仄平。\n仄仄平平平仄仄，平平仄仄仄平平。",
  "date": "2026.5.5"
}
```

**完整提交：**

```json
{
  "author": "林雨夜",
  "title": "次韵某某春日诗",
  "content": "春风拂面过江城，柳色如烟万缕生。\n莫道年华无觅处，枝头新绿已盈盈。",
  "date": "2026.3.15",
  "type": "诗",
  "genre": "七绝",
  "legacy_id": "auto",
  "preface": "读友人诗有感而作",
  "footnote": "江城：指武汉。",
  "tags": ["次韵", "春"],
  "relations": [
    {"id": "a1b2c3d4", "type": "reply"}
  ]
}
```

**强制不分配编号：**

```json
{
  "author": "林雨夜",
  "title": "试作",
  "content": "...",
  "date": "2026.5.5",
  "legacy_id": null
}
```

### curl 示例

```bash
curl -X POST https://sjtuguoxue.space/api/submit/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-nyyy-xxxxxxxxxxxx" \
  -d '{
    "author": "林雨夜",
    "title": "无题",
    "content": "平平仄仄平平仄，仄仄平平仄仄平。\n仄仄平平平仄仄，平平仄仄仄平平。",
    "date": "2026.5.5"
  }'
```

### 成功响应

```json
{
  "ok": true,
  "uuid": "a1b2c3d4",
  "legacy_id": "10101",
  "title": "无题",
  "author": "林雨夜",
  "type": "诗",
  "genre": "七绝"
}
```

### 错误响应

```json
{"ok": false, "error": "无效的 API Key"}          // 401
{"ok": false, "error": "权限不足"}                  // 403 (guest)
{"ok": false, "error": "只能以绑定的笔名提交"}      // 403 (非admin提交他人作品)
{"ok": false, "error": "缺少必填字段：author, title, content, date"}  // 400
{"ok": false, "error": "未找到作者：xxx"}            // 400
```

### 自动推断规则

| 字段 | 推断逻辑 |
|------|---------|
| `type` | 标题包含词牌名（浣溪沙、水调歌头等）或中圆点（`·`）→ `"词"`，否则 → `"诗"` |
| `genre` | 仅对诗自动检测：按正文纯字数判断（56字=七律，28字=七绝，40字=五律，20字=五绝，其他=古体诗） |
| `legacy_id` | 调用内部编号生成器，按 `作者ID×10000 + 体裁位×1000 + 序号` 规则分配。部分作者（林雨夜、韶逆等）使用自定义编号规则，不自动分配 |

### 权限

- **admin**：可以任意作者身份提交
- **author**：只能以绑定的笔名提交
- **guest**：无权提交

---

## POST /api/recommend_id/

单独调用编号推荐，不提交作品。

### 请求体

```json
{
  "author": "尤共",
  "title": "春日",
  "content": "...",
  "type": "诗"
}
```

`author` 接受作者名（如 `"尤共"`）或数字编号（如 `"21"`）。

### 成功响应

```json
{
  "success": true,
  "id": "214012",
  "msg": "检测为体裁【七绝】，推荐编号：214012"
}
```

### 失败响应

```json
{"success": false, "msg": "提示：作者【林雨夜】请按照自定义规则手动编号。", "id": ""}
```
