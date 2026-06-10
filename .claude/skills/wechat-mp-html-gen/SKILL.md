---
name: wechat-mp-html-gen
description: |
  生成微信公众号兼容的 HTML 排版。将 Markdown、纯文本、结构化数据或业务内容转为
  公众号可用的内联样式 HTML，支持多种预设主题和自定义样式。当用户需要生成公众号
  文章排版、公众号 HTML、微信排版、WeChat MP HTML 时触发。
  即使用户只说"帮我排版一篇公众号文章"或"转成公众号格式"也应该触发。
---

# WeChat MP HTML Generator

将任意内容转换为微信公众号兼容的 HTML，所有样式均为内联写法。

## Input Modes

本 skill 支持多种输入方式，不局限于 Markdown：

| Mode | When to use | How |
|------|-------------|-----|
| **Markdown 文件** | 用户提供 .md 文件 | 脚本 `--format markdown` |
| **纯文本** | 用户粘贴普通文本、业务内容 | 脚本 `--format text` 或 `auto` |
| **JSON 结构化** | 用户提供结构化数据（标题+段落+列表等） | 脚本 `--format json` |
| **HTML 注入样式** | 用户已有 HTML，需要加内联样式 | 脚本 `--format html` |
| **直接撰写** | 用户描述需求，Claude 直接构造 HTML | 不调脚本，Claude 直接写 HTML |

**「直接撰写」是最常用的模式** — 用户描述业务内容（产品介绍、活动通知、技术分享等），
Claude 根据主题样式表直接构造公众号 HTML。只有当输入已经是成型的 Markdown/文本文件时
才需要调用脚本。

## Workflow

### Path A: 脚本转换（输入已是文件/文本）

1. 用户提供文件或文本内容
2. 写入临时文件（如果是文本而非文件路径）
3. 调用转换脚本：
   ```bash
   python3 <skill_dir>/scripts/md2mp.py --input <file> --theme <theme> --format <auto|markdown|text|json|html> --output /tmp/wechat-mp-<timestamp>.html
   ```
4. 读取输出文件，展示给用户

### Path B: 直接撰写（用户描述需求）

1. 确认主题（用户指定或默认 `elegant`）
2. 获取主题样式表：
   ```bash
   python3 <skill_dir>/scripts/md2mp.py --export-theme <theme>
   ```
3. 参照样式表中每个标签的 `style` 值，直接构造 HTML
4. 输出格式：`<section>` 包裹的 HTML 片段，所有样式内联
5. 写入文件 + 在对话中展示源码

### Path C: JSON 结构化输入

用户提供或 Claude 构造如下 JSON，再调脚本转换：

```json
{
  "title": "文章标题",
  "sections": [
    {"type": "heading", "level": 2, "text": "章节标题"},
    {"type": "paragraph", "text": "正文内容..."},
    {"type": "quote", "text": "引用文字"},
    {"type": "list", "ordered": false, "items": ["项目一", "项目二"]},
    {"type": "image", "src": "url", "alt": "描述", "caption": "图片说明"},
    {"type": "table", "headers": ["列A","列B"], "rows": [["1","2"]]},
    {"type": "divider"},
    {"type": "html", "content": "<p style='...'>自定义HTML</p>"}
  ]
}
```

## Script Reference

```bash
# 自动检测格式并转换
python3 <skill_dir>/scripts/md2mp.py -i content.md -t elegant -o /tmp/out.html

# 指定纯文本格式
python3 <skill_dir>/scripts/md2mp.py -i article.txt -f text -t warm -o /tmp/out.html

# 从 stdin 读入
echo "内容" | python3 <skill_dir>/scripts/md2mp.py -t tech -o /tmp/out.html

# 为已有 HTML 注入内联样式
python3 <skill_dir>/scripts/md2mp.py -i raw.html -f html -t elegant -o /tmp/out.html

# 导出主题样式 JSON（用于直接撰写时参考）
python3 <skill_dir>/scripts/md2mp.py --export-theme elegant

# 列出所有主题
python3 <skill_dir>/scripts/md2mp.py --list-themes
```

## Supported Tags & Constraints

微信公众号对 HTML 过滤严格：

- **`<style>` 标签会被移除** — 所有样式必须写成 `style="..."` 内联属性
- **不支持 `<script>`**
- **不支持 `class` / `id`** — 只能用 `style`
- **图片必须已上传到微信素材库** — 外链图片无法显示
- **`<div>` 内不能直接放裸文字** — 文字必须用 `<p>` 或 `<span>` 包裹，否则复制到编辑器后样式（尤其居中、对齐）会丢失

### 可用标签速查

| 类别 | 标签 |
|------|------|
| 文本 | `<p>`, `<br>`, `<strong>`, `<em>`, `<u>`, `<s>`, `<span>` |
| 标题 | `<h1>` ~ `<h6>` |
| 列表 | `<ul>`, `<ol>`, `<li>` |
| 链接/图片 | `<a>`, `<img>` |
| 表格 | `<table>`, `<tr>`, `<td>`, `<th>` |
| 块级 | `<div>`, `<section>` |
| 其他 | `<blockquote>`, `<pre>`, `<code>`, `<hr>` |

### 安全 CSS 属性

```
color, background-color, background, font-size, font-weight, font-style, font-family
line-height, letter-spacing, text-align, text-decoration, text-indent
margin, margin-top/right/bottom/left, padding, padding-top/right/bottom/left
border, border-radius, border-bottom, border-left, border-top, border-right
display, width, max-width, min-width, box-sizing
overflow, word-break, white-space
linear-gradient (in background)
```

## Themes

| Theme | Style | Colors |
|-------|-------|--------|
| `elegant` | 优雅简约，衬线标题 + 无衬线正文 | 淡蓝 #4a90d9 |
| `tech` | 科技感，深色代码块 | 蓝紫 #667eea |
| `warm` | 温暖柔和，圆角卡片 | 暖橙 #e8a735 |
| `minimal` | 极简黑白，大留白 | 纯黑白 |
| `dark` | 深色背景浅色文字 | 暗蓝 #58a6ff |

## Direct Composition Patterns

Claude 直接撰写 HTML 时的常用模板片段：

### 带标题装饰的章节
```html
<h2 style="font-size:20px;font-weight:bold;color:#16213e;margin:25px 0 15px;padding-left:12px;border-left:4px solid #4a90d9;">章节标题</h2>
```

### 高亮文字
```html
<span style="color:#4a90d9;font-weight:bold;">高亮内容</span>
```

### 注意/提示框
```html
<div style="background:#fff3cd;border-left:4px solid #ffc107;padding:12px 15px;margin:15px 0;border-radius:0 4px 4px 0;font-size:14px;color:#856404;">
  <strong style="font-weight:bold;">注意：</strong>提示内容
</div>
```

### 图片 + 说明
```html
<img src="..." alt="..." style="max-width:100%;border-radius:4px;margin:15px auto;display:block;">
<p style="font-size:12px;color:#999;text-align:center;margin:8px 0 15px;">图片说明文字</p>
```

### 脚注/来源
```html
<p style="font-size:13px;color:#888;margin:5px 0;line-height:1.6;padding-left:15px;">
  来源：xxx
</p>
```

## Output Contract

- HTML 片段以 `<section>` 包裹，不含 `<html>/<head>/<body>`
- 所有样式内联，无 `class`/`id`/`<style>` 标签
- 输出文件路径告知用户，同时在对话中以代码块展示 HTML 源码
- 提示用户复制后粘贴到公众号编辑器的"代码编辑"模式

### 编辑器元数据（非 HTML 字段）

以下字段无法通过 HTML 复制，需要在公众号编辑器内手动填写。生成 HTML 时一并输出供用户审阅：

| 字段 | 要求 | 说明 |
|------|------|------|
| **标题** | 必填 | 简洁有力，建议 15-25 字 |
| **作者** | 选填 | 可留空 |
| **摘要** | 必填，≤120 字 | 需博眼球，出现在分享卡片和消息列表 |
| **封面图** | 必填，2.35:1 + 1:1 | 见下方封面图生成流程 |

### 封面图生成流程

公众号封面需要两张图：**2.35:1**（大图卡片）和 **1:1**（小图/列表），建议等高拼接为一张提供给用户。

**当有图片生成工具可用时（gpt-image-2 等）：**
1. 先根据文章主题生成 **21:9 横向图**
2. 以该图为参考，I2I（图生图）改为 **1:1** 正方形构图
3. 将两张图**横向等高拼接**为一张图，发给用户
4. 用户在编辑器中分别裁剪上传

**当无图片生成工具可用时：**
1. 根据文章内容撰写**生图提示词**（中英文各一版）
2. 注明建议尺寸（21:9 和 1:1）
3. 提示用户使用 Midjourney / DALL-E / GPT-image-2 等工具自行生成

### 协调转推流程

当文章需要推送到其他公众号（如兄弟社团账号、校级平台等），引导用户按以下步骤操作：

1. 在公众号编辑器中将文章**存为草稿**
2. 打开**秀米编辑器**，新建一个图文
3. 点击 **更多 > 导入公众号文章 > 草稿箱**，导入刚才的草稿
4. 如果发现排版有问题，点击 **设置** ， **取消勾选** “粘贴时清除格式”，点击空白灰色处，按下 **Ctrl+A** 全选、 **Del** 删除；然后在 **微信公众号编辑器** 中，按下 **Ctrl+A** 全选、确保选中 **编辑器内部** 的全部内容后按下 **Ctrl+C** 复制；回到 **秀米** ，点击空白灰色处，按下 **Ctrl+V** 粘贴。这样基本没有格式问题。
5. 检查排版无误后，点击 **另存给其他用户**
6. 选择需要协助转推的目标账号
7. 通知对方账号管理员审核发布

## 国学社公众号专用规则

### 诗词排版规范

公众号中的诗词排版与网站不同，需适配小屏幕阅读：

- **所有内容（标题、正文）一律两端对齐**（`text-align:justify`），不要居中
- **诗（律诗/绝句/古体）**：一段写到底，不分行。句间用标点自然分隔即可
- **词**：也不换行，上下阕之间用 `⦾` 记号分隔（如「……平平仄。⦾ 仄仄平平……」）
- **同一作者的组稿**：作者信息只在开头出现一次，每首诗下面不重复署名
- **文字必须用 `<p>` 或 `<span>` 包裹**，不要在 `<div>` 内直接放裸文字

示例（词）：

```html
<p style="line-height:2;font-size:15px;color:#444;font-family:'STKaiti','KaiTi',serif;text-align:justify;">
  明镜台前仔细看。双核炯炯透光寒。吸盘宛转带丝牵。⦾ 世上虫生多少事，人间药入几分安。笑他隐伏在澶漫。
</p>
```

示例（律诗）：

```html
<p style="line-height:2;font-size:15px;color:#444;font-family:'STKaiti','KaiTi',serif;text-align:justify;">
  乙酰来过种柠檬，几变身形问旧踪。成碳成氢多历历，如熵如电只空空。转轮不待微生觉，断链但和余梦同。愿许他时作苹果，重回故地草丛中。
</p>
```

### 名片

> **必须遵守**：为上海交通大学国学社公众号制作推文时，文章底部必须放置社团名片图片。
> 名片素材地址见 `sjtuguoxue_vi` skill，当前使用「国学社名片 2026」。
>
> ```html
> <!-- 文章底部必放名片 -->
> <img src="https://mmbiz.qpic.cn/sz_mmbiz_png/CA1DSgOCkZWNZ41xc6368aqnreOYPcFvl6klJl9U6sicJRV7jwfDNjv3ia9GveIgTpNBtkQiaVdkkGQoiaRoY9m6HhBo1JZP4U92oCRlcbC1ziaQ/640?wx_fmt=png"
>      style="max-width:100%;display:block;margin:20px auto 0;">
> ```

## Failure Handling

- 格式检测失败 → 回退为纯文本模式
- 主题不存在 → 使用 `elegant` 默认主题并告知
- Python 依赖 → 脚本纯 Python 实现，无外部依赖

## Examples

**Example 1: 用户粘贴业务文案**
```
用户：帮我排版一下这段公众号文案，用 warm 主题：
「夏日特惠」活动来了！6月15日至30日，全场满200减50...
→ Claude 直接撰写 HTML，使用 warm 主题样式
```

**Example 2: 用户提供 Markdown 文件**
```
用户：把 article.md 转成公众号排版
→ python3 <skill_dir>/scripts/md2mp.py -i article.md -t elegant -o /tmp/wechat-mp.html
```

**Example 3: 用户描述需求**
```
用户：写一篇关于 AI 趋势的公众号文章，tech 风格
→ Claude 撰写内容 + 直接构造 HTML
```

**Example 4: 用户有现成 HTML 要加样式**
```
用户：给这段 HTML 加上公众号兼容的样式
→ python3 <skill_dir>/scripts/md2mp.py -f html -t elegant -o /tmp/out.html
```
