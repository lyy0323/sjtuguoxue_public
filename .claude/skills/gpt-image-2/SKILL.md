---
name: gpt-image-2
description: |
  使用 GPT-image-2 模型生成图像。支持文生图（text-to-image）和图生图（image-to-image）。
  当用户要求用 GPT-image-2 / gpt-image / OpenAI 图像模型生图，或明确说"用 GPT 画"、
  "GPT 生图"、"gpt image"时触发。也适用于需要高质量文字渲染的图像生成场景。
  不适用于：Excalidraw 手绘风格图、飞书画板绘制。
---

# GPT-image-2

## Procedure

1. 确定生成模式：
  - 用户只给了文字描述 → **文生图**
  - 用户提供了参考图片 URL 或本地图片路径 → **图生图**
2. 确定尺寸参数：
  - 用户指定了比例/尺寸 → 使用用户指定的值（如 "1:1"、"16:9"、"2:3"）
  - 用户未指定 → 默认 "1:1"
3. 调用生成脚本：

```bash
python3 ~/.claude/skills/gpt-image-2/scripts/generate.py \
  --mode <text2img|img2img> \
  --prompt "<用户描述>" \
  --size "<比例>" \
  --output "<输出路径>" \
  [--images "<图片URL1>" "<图片URL2>" ...]
```

输出路径默认放在当前 workspace 下，文件名用 `gpt-image-2-<timestamp>.png`。

1. 脚本返回 JSON：`{"success": true, "urls": [...], "local_path": "..."}` 或 `{"success": false, "error": "..."}`
2. 成功后用 `<media src="<local_path>" type="image" />` 展示给用户。

## Output contract

- 生成的图片下载到本地 workspace
- 以 `<media>` 标签发送给用户
- 同时告知原始 CDN URL（方便用户分享）

## Failure handling

- API 返回非 200 → 报告具体错误码和信息给用户
- 网络超时（120s）→ 提示用户稍后重试
- API key 无效 → 提示用户更新 `~/.claude/skills/gpt-image-2/config.json`（可使用国学社中转站 `sjtuguoxue-relay` 的同一个 Key）

## Examples

**文生图**：

```
用户：用 gpt image 画一只在月球上跳舞的猫
→ python3 ~/.claude/skills/gpt-image-2/scripts/generate.py --mode text2img --prompt "A cat dancing on the moon, whimsical illustration style" --size "1:1" --output ./gpt-image-2-1717200000.png
```

**图生图**：

```
用户：基于这张图扩展背景（附图片URL）
→ python3 ~/.claude/skills/gpt-image-2/scripts/generate.py --mode img2img --prompt "expand the background naturally" --size "16:9" --images "https://example.com/ref.png" --output ./gpt-image-2-1717200000.png
```

提示：可以用文生图的cdn链接作为图生图的images参数，但注意有效期（一般在1day左右）。如果用户需要上传参考图片，引导其去[https://img.scdn.io/](https://img.scdn.io/) 免费图床上传图片，并拿到cdn url