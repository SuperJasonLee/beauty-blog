# daily-publish —— 每天 12:00 自动发布

每日 12:00（本地时间）由 macOS launchd 触发，自动跑完 5 阶段发布流程：
**搜索 → 配图 → 写文 → 翻译 → 发布**（无需 review）。

## 文件清单

| 文件 | 作用 |
|---|---|
| `daily-publish.sh` | 主入口：5 阶段全流程编排 |
| `com.beautyblog.dailypublish.plist` | launchd 调度配置（12:00 触发） |
| `install.sh` | 一键安装（复制 plist + load） |
| `uninstall.sh` | 一键卸载 |
| `.env.example` | 配置模板（复制为 `.env` 生效） |

## 快速开始

```bash
# 1. （可选）创建配置
cp scripts/daily-publish/.env.example scripts/daily-publish/.env

# 2. 安装调度（Mac 一次）
./scripts/daily-publish/install.sh

# 3. 测试一次（不等 12:00）
./scripts/daily-publish/daily-publish.sh
```

## 控制命令

```bash
# 暂停（不卸载调度）
touch scripts/daily-publish/.disabled

# 恢复
rm scripts/daily-publish/.disabled

# 立即触发一次
./scripts/daily-publish/daily-publish.sh

# 卸载调度
./scripts/daily-publish/uninstall.sh

# 查看最近日志
ls -lt logs/daily-publish/ | head
tail -f logs/daily-publish/$(ls -t logs/daily-publish/*.log | head -1 | xargs basename)
```

## 行为说明

1. **Kill switch**：创建 `.disabled` 文件即可暂停（无需卸载 launchd）
2. **Auto commit**：默认开启（`AUTO_COMMIT=true`）。**Auto push 默认关闭**（`AUTO_PUSH=false`），需手动 `git push` 触发部署——这是为了让你有"刹车"机会
3. **macOS 通知**：每次完成后弹原生通知，包含发布数量和日志路径
4. **失败处理**：任一阶段失败会发"Basso"警告音通知并保留详细错误在 log
5. **备份**：翻转 `draft: true` 前会备份原文件为 `.bak`

## 已知限制（v1）

- 当前 `post_generator.py` 是**硬编码模板**，未接 OpenAI API。因此每日跑出的内容相同、只换文件名日期。要真正"每日独特内容"需后续接入 LLM。
- 仅调度了**垂类新闻 pipeline**（`npm run crawl:eye-news`）。如需调度其他类型（小红书趋势/精品指南），需新建 pipeline 脚本。
- 翻译步骤的术语校对被跳过（依用户要求"无需审核翻译"）。

## 相关文档

- [docs/post-publishing-workflow.md §11](../../docs/post-publishing-workflow.md) —— 总体 SOP
- [scripts/crawl-eye-surgery-news/](../crawl-eye-surgery-news/) —— pipeline 实现
