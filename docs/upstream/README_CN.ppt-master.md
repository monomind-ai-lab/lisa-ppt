> **Lisa's PPT 存档说明。** 这是 PPT Master v6.1.0 的 README_CN，仅供参考与 W2 取材。本副本已删除：两个赞助章节与全部推广链接、以及自更新方式（Lisa's PPT 已移除上游的更新脚本——它会从上游仓库重新拉取）。`docs/assets/` 下的截图链接不再有效（该目录未导入）。其余内容原样保留。

# PPT Master — AI 生成原生 PowerPoint，支持任意文档输入

[![Version](https://img.shields.io/github/v/release/hugohe3/ppt-master?label=version&color=blue)](https://github.com/hugohe3/ppt-master/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/hugohe3/ppt-master.svg)](https://github.com/hugohe3/ppt-master/stargazers)
[![AtomGit stars](https://atomgit.com/hugohe3/ppt-master/star/badge.svg)](https://atomgit.com/hugohe3/ppt-master)
[![The Agentic Leaderboard](https://www.theagenticleaderboard.com/badges/ppt-master.svg)](https://www.theagenticleaderboard.com/agent/?q=ppt-master)

<p align="center">
  <a href="https://trendshift.io/repositories/25760?utm_source=repository-badge&amp;utm_medium=badge&amp;utm_campaign=badge-repository-25760" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/repositories/25760" alt="hugohe3%2Fppt-master | Trendshift" width="250" height="55"/></a>
</p>

[English](./README.md) | 中文

## 产品定位

**可编辑如今只是及格线——真正要紧的是你能拿到多少 PowerPoint。** PPT Master 交付的是 PowerPoint 的原生对象模型本身，而且有深度：带调节手柄的原生形状与连接符、按需的数据驱动图表与表格、完整的文本 / 图片 / 填充 / 效果，点开任意元素都作为原生 PowerPoint 对象继续编辑；走模板 / 结构化路线时，它还能为你产出带真正母版与版式（`p:sldMaster` / `p:sldLayout` 继承）的 deck。

而且这份深度是**一个前进方向，不是一张固定清单。** PPT Master 的北极星是持续向 PowerPoint 本身靠拢：不断开发、集成更多 PowerPoint 原生能力，一个版本接一个版本，缩小「AI 能替你生成的」和「你在 PowerPoint 里手工能做出的」之间的差距。[PowerPoint ↔ SVG 映射指南](./docs/zh/powerpoint-svg-mapping.md) 逐条、诚实地记录了这份能力今天覆盖到哪——SmartArt 是刻意的排除，不是缺口。

形态上，它是一套在有 Agent 能力的 AI 工具里运行的工作流（一个 "skill"）：你在对话框里说"用这份 PDF 做一份 PPT"，它就按流程在你本机生成、导出原生可编辑的 `.pptx`。你不写任何代码，只做三件事——装 Python、装一个 AI 工具、把材料放进来。

从源材料生成新 deck 是主管线，但不是唯一路线：PPT Master 还能从你的参考资料中提炼可复用的品牌 / 风格 / 版式 / 成品模板，把新内容填进你已有的 `.pptx` 并保留其设计，或为成品 deck 追加原生转场、动画和旁白——每条路线都有明确的保留契约。

在这份原生深度之上，这个形态还带来三个承诺：

- **成本透明可控** — 工具免费开源，唯一成本是你自己的 AI 模型用量，不在此之外增加任何订阅费用
- **数据不出本地** — 除与 AI 模型的对话外，全流程在你的电脑上完成
- **不锁定平台** — 任何具备 agent 能力的 AI IDE 均可驱动；Claude、GPT、Gemini、Kimi 等模型均可使用

为什么选它、以及它不适合的场景 → [为什么选 PPT Master](./docs/zh/why-ppt-master.md)；这些承诺背后的长期能力边界 → [项目定位与能力边界](./docs/zh/project-positioning.md)。

> [!IMPORTANT]
> ### 这是一个工具，不是一个许愿池
> `harness + model = agent`——PPT Master 只负责工作流，产出上限由模型决定。推荐 **Kimi K3（或 Claude）大上下文窗口（~100 万 token）+ AI 生图（`gpt-image-2` 或 Google `gemini-3.1-flash-image`）**；其他模型能跑通流程，但有质量差距。
>
> 也别指望一把就拿到完美成品。它的价值是帮你把大部分枯燥的活儿干掉，剩下的打磨交给你——做原生可编辑的 PPT，本就是为了让你接着改，而不是甩给你一张改不动的图。模型越便宜，要补的人工就越多；效果不理想，先升级模型，再对照[快速入门](./docs/zh/getting-started.md)和[示例工程](https://hugohe3.github.io/ppt-master-examples/)检查用法。

---

## 关于作者

我是何雨果（Hugo He），投融资领域从业者（注册会计师 · 资产评估师 · 咨询工程师（投资）），工作中经常审阅和修改 PPT。我希望 AI 生成的幻灯片仍然能在 PowerPoint 里继续编辑，而不是被压成一张张图片——所以做了这个。

未来，使用 Python 和 AI agent 的能力会越来越重要，这个项目也想展示：仅凭这两样，你能走多远。零基础上手有一段学习曲线，但走完这段，你就接上了未来——做 PPT 只是个借口，我真正想推广的是 Python 和 agent。

---

## 你可能也感兴趣

### <a href="https://github.com/microsoft/ResearchStudio">ResearchStudio-<img src="https://raw.githubusercontent.com/ai-nuts/Storage/main/ResearchStudio/ResearchStudio-Reel/docs/figures/reel-wordmark.png" alt="Reel" height="16"></a>

> 微软开源项目，我最近也参与其中——从**论文**到**演讲视频**、**海报**与**博客**，自动化科研传播的**最后一公里**。
>
> 📦 **仓库：**[microsoft/ResearchStudio](https://github.com/microsoft/ResearchStudio) · 📄 **论文：**[arXiv:2607.04438](https://arxiv.org/abs/2607.04438)

<table align="center">
<tr>
<td align="center" valign="middle" width="53%">
  <a href="https://aka.ms/ResearchStudio">
    <img src="https://raw.githubusercontent.com/ai-nuts/Storage/main/ResearchStudio/ResearchStudio-Reel/docs/figures/reel_demo.gif" width="100%"
    alt="ResearchStudio-Reel 演示" />
  </a>
</td>
<td align="center" valign="middle" width="47%">
  <a href="https://aka.ms/ResearchStudio">
    <img src="https://raw.githubusercontent.com/ai-nuts/Storage/main/ResearchStudio/ResearchStudio-Reel/docs/examples/latent_diffusion_landscape/poster.png" width="100%" alt="ResearchStudio-Reel 生成的海报" />
  </a>
</td>
</tr>
</table>

<details>
<summary><strong>BibTeX</strong> —— 如果你在研究中使用了 ResearchStudio-Reel</summary>

```bibtex
@article{xiao2026researchstudioreel,
  title   = {ResearchStudio-Reel: Automate the Last Mile of Research from Paper to Poster, Video, and Blog},
  author  = {Lingao Xiao and Yalun Dai and Yangyu Huang and Qihao Zhao and Wenshan Wu and Hugo He and Ruishuo Chen and Jin Jiang and Qianli Ma and Jiahuan Zhang and Xin Zhang and Ying Xin and Yang Ou and Yan Xia and Scarlett Li and Longbo Huang and Zhipeng Zhang and Yang He and Yap Kim Hui and Yan Lu},
  journal = {arXiv preprint arXiv:2607.04438},
  year    = {2026},
  url     = {https://arxiv.org/abs/2607.04438}
}
```

</details>

---

## 快速开始

### 1. 前置条件

**只需安装 [Python](https://www.python.org/downloads/) 3.10+。** 其余依赖在第 3 步下载好项目后，用一行 `pip install -r requirements.txt` 装齐。

<details>
<summary><strong>Windows</strong> — 请看专门的<a href="./docs/zh/windows-installation.md">手把手安装指南</a> ⚠️</summary>

Windows 需要一些额外步骤（PATH 设置、执行策略等）。我们为 Windows 用户写了一份**手把手安装指南**：

**📖 [Windows 安装指南](./docs/zh/windows-installation.md)** — 从零到跑通第一份 PPT，10 分钟搞定。

简要流程：从 [python.org](https://www.python.org/downloads/) 下载 Python → **安装时勾选 "Add to PATH"** → 完成，依赖安装见第 3 步。
</details>

<details>
<summary><strong>macOS / Linux</strong> — 安装即用</summary>

```bash
# macOS
brew install python

# Ubuntu / Debian
sudo apt install python3 python3-pip
```
</details>

<details>
<summary><strong>边缘场景备用方案</strong> — 99% 的用户用不到</summary>

**Pandoc** — 只在需要转小众格式时才装：`.doc`、`.odt`、`.rtf`、`.tex`、`.rst`、`.org`、`.typ`。`.docx`、`.html`、`.epub`、`.ipynb` 已由 Python 原生处理，不需要 pandoc。

```bash
# macOS
brew install pandoc

# Ubuntu / Debian
sudo apt install pandoc
```
</details>

### 2. 选择一个 Agent

PPT Master 在**任何具备 agent 能力**（可读写文件、执行命令、持续多轮对话）的工具里都能跑。

没用过这类工具也不用担心：它们在本项目里只扮演一个角色——一个能读写文件的 AI 聊天窗口。从下表任选一款装好即可，全程只用它的聊天面板，不需要写任何代码。

> **作者最推荐：[Claude Code](https://claude.ai/code)** ——本项目开发与测试最充分的环境，CLI 与 VS Code / JetBrains 扩展均可。

| 类型 | 代表工具 | 说明 |
|---|---|---|
| **IDE 内置 agent** | • VS Code 架构（含 [VS Code](https://code.visualstudio.com/) 本体及分支与衍生）：[Cursor](https://cursor.sh/)、Trae、Codebuddy IDE、[Windsurf](https://codeium.com/windsurf) 等<br>• 其他架构：[Zed](https://zed.dev/) 等 | 编辑器原生集成 agent |
| **IDE 插件 / 扩展** | [Claude Code](https://claude.ai/code)（VS Code / JetBrains 扩展）、[GitHub Copilot](https://github.com/features/copilot)、[Cline](https://cline.bot/)、通义灵码 等 | 装在 VS Code / JetBrains 等宿主里使用 |
| **CLI agent** | [Claude Code](https://claude.ai/code) CLI、[Codex CLI](https://github.com/openai/codex)、Gemini CLI 等 | 终端里运行，适合脚本化 / 远程 / 服务器场景 |



**🔀 手上有多个渠道？** 拿到多家的 API Key 后，[cc-switch](https://github.com/farion1231/cc-switch)（跨平台桌面应用）可以一键切换 Claude Code、Codex、Gemini CLI 等工具的 API 供应商，免去手动改配置。

### 3. 配置项目

**方式 A — Git clone**（推荐；需先安装 [Git](https://git-scm.com/downloads)）：首选这种方式，因为 clone 可以随时拉取最新版本。

```bash
# GitHub
git clone https://github.com/hugohe3/ppt-master.git
# AtomGit（中国大陆地区网速更快）
git clone https://atomgit.com/hugohe3/ppt-master.git
cd ppt-master
```

然后安装依赖：

```bash
pip install -r requirements.txt
```

**方式 B — 下载 ZIP**（无需安装 Git，适合快速体验）：
[GitHub](https://github.com/hugohe3/ppt-master) → **Code → Download ZIP** · [AtomGit](https://atomgit.com/hugohe3/ppt-master) → **克隆/下载 → 下载ZIP**（中国大陆地区访问 GitHub 下载不便时用这个，网速更快）；解压后同样用 `pip install -r requirements.txt` 装依赖。ZIP 没有 Git 历史，不能自动 `git pull`（更新见下）。

如果完整仓库下载失败、或嫌体积太大，可以改到 [Releases](https://github.com/hugohe3/ppt-master/releases) 页面下载纯技能包 `ppt-master-skill-*.zip`（约 56 MB，功能完整，但不含内置示例 deck）。

#### 日常更新

**Git clone 安装：**

```bash
git pull
pip install -r requirements.txt
```

脚本会拉取最新版；如果 `requirements.txt` 有变化，会自动同步 Python 依赖。

**下载 ZIP 安装：**

ZIP 目录没有 Git 历史，不能自动 `git pull`。更新时请重新下载最新版 ZIP，解压到新目录，然后把旧目录里的 `.env` 和 `projects/` 复制过去，再执行：

```bash
pip install -r requirements.txt
```

> **方式 C — Skill marketplace**：仓库已添加 `.claude-plugin/marketplace.json` 元数据，可通过 [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces) 生态一行安装：
>
> ```bash
> # 跨 agent CLI（Claude Code、Cursor、Codex 等）
> npx skills add hugohe3/ppt-master
>
> # 或在 Claude Code 内
> /plugin marketplace add hugohe3/ppt-master
> /plugin install ppt-master@ppt-master
> ```
>
> 上述两种安装方式都只会拉取 skill 文件本身（不含完整仓库），后处理脚本仍需在安装目录跑 `pip install -r requirements.txt`。

### 4. 开始创作

**先在 Agent 里打开项目文件夹：** 目标是让 AI 工作在上一步解压 / 克隆出来的 `ppt-master` 目录里——IDE 类工具通过菜单 **文件 → 打开文件夹**（File → Open Folder）打开它，AI 聊天面板通常在侧边栏；CLI 类工具先 `cd ppt-master` 再启动。之后的一切都在聊天里完成。

**提供原始材料（推荐）：** 将 PDF、DOCX、图片等文件放入 `projects/` 目录下，在 AI 聊天面板中告诉它使用哪些文件。获取路径的最快方式：在文件管理器或 IDE 侧边栏中右键文件 → **复制路径**（Copy Path / Copy Relative Path），直接粘贴进聊天框。

```
你：请用 projects/q3-report/sources/report.pdf 这份文件生成一份 PPT
```

**直接输入内容：** 也可以把文字内容直接粘贴进聊天窗口，AI 会根据这些内容生成 PPT。

```
你：请根据以下内容制作成 PPT：[粘贴你的文字内容...]
```

默认流程下（除非显式要求快速生成），AI 会先确认设计规范：

```
AI：好的，先确认设计规范：
   [模板] B) 自由设计
   [格式] PPT 16:9
   [页数] 8-10 页
   ...
```

AI 全程处理——内容分析、视觉设计、SVG 生成、PPTX 导出。

**快速生成（跳过来回确认）：** 显式说明即可，AI 直接进入创作与导出。

```
你：用 projects/q3-report/sources/report.pdf 快速生成一份 5 页 PPT，不用跟我确认
```

你明确提的照做，你没提的由 AI 直接定，不再回来问你。它仍会转换来源、补齐事实、应用共享视觉基线，并按需使用图片 / 图标 / 原生形状 / 图表 / 表格 / PowerPoint 原生行内或块级公式——省掉的是交互与持久规划，不是 PPT 能力。它是不可续接的一次性生成，也不会产生 `svg_final/` 预览。完整说明 → [快速模式](./docs/zh/getting-started.md#快速模式)。

> **输出说明：** SVG 管线统一由项目转换器读取 `svg_output/`，生成可直接编辑的原生 DrawingML `.pptx`，保存至 `exports/<name>_<timestamp>.pptx`。默认 Generate 流程会运行 `finalize_svg.py` 并生成自包含预览 `svg_final/`；PowerPoint 手工“转换为形状”不在支持范围。用户可显式启用[快速生成](./skills/ppt-master/workflows/profiles/quick-generate.md)：它跳过 Strategist、确认、`design_spec.md`、`spec_lock.md` 与 `finalize_svg.py`——你明确提出的要求照做，你没提的由 Agent 在一次有效上下文中直接决定；仍按需转换来源、研究事实缺口、应用共享 mode / visual style / 美学规范、准备图片 / 图标，并把公式直接创作为原生行内或块级 marker，同时考虑原生形状与数据可视化，随后按规范手写 SVG，通过无锁的 Quick 最终质量检查，再导出最终 PPTX。它不写替代计划，上下文丢失后不能续接。公式 marker 会把 LaTeX payload 编译为 PowerPoint 2010+ 可编辑 OMML；块级 group 与行内 `<tspan>` run 都保留普通 SVG 预览，导出时将其替换。Keynote、WPS、LibreOffice 等非 PowerPoint 客户端的公式显示与编辑能力不在支持合同内。原生图表 / 表格替换、讲稿、动效、旁白和诊断等普通导出能力仍可按需使用；讲稿、自定义对象动画和旁白默认关闭，Agent 可在用户要求或 deck 确有需要时启用。Quick 使用默认输出路径时仍会生成普通 postflight 报告，并把 `svg_output/` 镜像到 `backup/<timestamp>/svg_output/`；显式指定输出路径时沿用普通流程不创建备份的行为。图表和表格默认导出为 SVG 派生、可逐形状编辑的 DrawingML 对象，优先保证 PowerPoint / Keynote / WPS 间的视觉一致性；可加 `--native-charts-and-tables`，把符合合同的组替换为带数据源和对象专属编辑能力的 PowerPoint 原生 Chart/Table 对象，跨软件渲染可能略有差异，保存为 `exports/<name>_<timestamp>_native_charts_tables.pptx`。这两种图表/表格导出变体都可编辑，区别在于 PowerPoint 对象模型，而不是“能否编辑”。

> **已有一份想复用的 `.pptx`？** 把 deck 连同素材给 AI，说「套模板」即可——Edit Native PPTX 会保留原设计，逐字节保留未改页面，只编辑选中页面，支持选页/重排，并可添加讲稿或旁白。详见 [常见问题](./docs/zh/faq.md) 与 [工作流](./skills/ppt-master/workflows/edit-native-pptx.md)。

> **遇到问题？** AI 迷失上下文时，让它先读 `skills/ppt-master/SKILL.md`；其他问题查看 **[常见问题](./docs/zh/faq.md)** — 涵盖模型选择、排版问题、导出异常等，基于真实用户反馈持续更新。

### 5. 图片获取（可选）

非用户自带图片有两条路径，可在同一份 deck 里按图混用：

**A) AI 生图** — Agent host 提供原生生图工具时可直接使用；也可通过 `image_gen.py` 配置 `IMAGE_BACKEND` 和供应商 `*_API_KEY`。host-native 生图不需要另配供应商生图 API Key，直接要求 Agent 使用自身生图工具即可。`python3 skills/ppt-master/scripts/image_gen.py --list-backends` 查看供应商后端清单。`gpt-image-2` 目前综合质量最佳。

**B) 网络图片搜索** — `image_search.py`。**零配置**可用；建议配置 `PEXELS_API_KEY` / `PIXABAY_API_KEY`（都免费申请）以获得稳定的高质量结果：

- 不配置时只使用 Openverse / Wikimedia Commons，适合作为兜底，但容易出现构图随意、清晰度不稳定的图片
- 配置后默认搜索链会追加 Pexels / Pixabay，现代商业摄影、人物、办公、生活方式和插画类图片质量明显更稳定
- 许可自动处理：默认把 CC0、公有领域、Pexels / Pixabay 免署名许可、CC BY、CC BY-SA 一起纳入候选；选中需署名的图片时，Executor 会在该幻灯片自动添加小字署名。只有明确不能出现署名时，才使用 `--strict-no-attribution` 限制为免署名图片
- 对视觉要求高的封面、产品图、人物图和品牌场景，优先级建议：用户自带高清素材 / AI 生图 > 配置 Pexels / Pixabay 的网络搜索 > 零配置网络搜索

上面提到的 API Key 统一通过 `.env` 配置。clone 安装可以用 `cp .env.example .env`；skill marketplace 安装建议使用持久的用户级配置：

```bash
mkdir -p ~/.ppt-master
cp /path/to/installed/ppt-master/.env.example ~/.ppt-master/.env
```

PPT Master 会优先读取当前进程环境变量，然后按顺序读取第一个存在的 `.env`：当前工作目录、skill 安装目录（如 `~/.agents/skills/ppt-master/.env`）、clone 仓库根目录、`~/.ppt-master/.env`。

> 完整说明：[`image-generator.md`](./skills/ppt-master/references/image-generator.md)（AI）·[`image-searcher.md`](./skills/ppt-master/references/image-searcher.md)（网络）。

---

## 文档导航

| | 文档 | 说明 |
|---|------|------|
| 📘 | [快速入门](./docs/zh/getting-started.md) | 三步做出第一份 deck，外加模板、实时预览、动画、旁白、声音复刻的用法（**新用户从这里开始**） |
| 🆚 | [为什么选 PPT Master](./docs/zh/why-ppt-master.md) | 为什么选它、以及它不适合的场景 |
| 🧭 | [项目定位与能力边界](./docs/zh/project-positioning.md) | 长期定位、产品承诺与能力边界 |
| 🪟 | [Windows 安装指南](./docs/zh/windows-installation.md) | Windows 用户手把手安装教程 |
| 📖 | [SKILL.md](./skills/ppt-master/SKILL.md) | 核心流程与规则 |
| 📐 | [画布格式](./skills/ppt-master/references/canvas-formats.md) | PPT 16:9、小红书、朋友圈等 10+ 种格式 |
| 🛠️ | [脚本与工具](./skills/ppt-master/scripts/README.md) | 所有脚本和命令 |
| 💼 | [示例](https://hugohe3.github.io/ppt-master-examples/) | 所有示例项目 |
| 🏗️ | [技术路线](./docs/zh/technical-design.md) | 架构、设计哲学、为什么选 SVG |
| ❓ | [常见问题](./docs/zh/faq.md) | 模型选择、费用、排版问题排查、自定义模板 |

<sub>完整文档索引 → [`docs/zh/`](./docs/zh/README.md)</sub>

---

## 贡献

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 开源协议

[MIT](LICENSE)

## 致谢

[SVG Repo](https://www.svgrepo.com/) · [Tabler Icons](https://github.com/tabler/tabler-icons) · [Simple Icons](https://github.com/simple-icons/simple-icons) · [Phosphor Icons](https://github.com/phosphor-icons/core) · [Robin Williams](https://en.wikipedia.org/wiki/Robin_Williams_(author))（CRAP 设计原则）

固定版本、许可证、署名、兼容层与商标边界详见[第三方图标说明](./skills/ppt-master/templates/icons/THIRD_PARTY_NOTICES.md)。

## 相关工具

[cc-switch](https://github.com/farion1231/cc-switch) —— 一键切换 Claude Code / Codex / Gemini CLI 等工具的 API 供应商。

## 联系与合作

欢迎合作交流、将 PPT Master 集成到你的工作流，或者单纯提问：

- 💬 **提问与分享** — [GitHub Discussions](https://github.com/hugohe3/ppt-master/discussions)
- 🐛 **Bug 反馈与功能建议** — [GitHub Issues](https://github.com/hugohe3/ppt-master/issues)

---

