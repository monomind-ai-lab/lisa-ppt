# 文档索引

[English](../README.md) | [中文](./README.md)

---

用户文档集中在 `docs/` 目录：英文文件为规范源，本目录（`docs/zh/`）是同步中文译本。AI 自身消费的工作流与技术参考位于 [`skills/lisa-ppt/`](../../skills/lisa-ppt/SKILL.md)。

## 快速上手

| 文档 | 说明 |
|---|---|
| [快速入门](./getting-started.md) | 三步做出第一份 deck，外加模板、动画、旁白、声音复刻的用法 |
| [Windows 安装指南](./windows-installation.md) | Windows 用户手把手安装教程 |
| [常见问题](./faq.md) | 模型选择、费用、排版问题排查、自定义模板——基于真实用户反馈持续更新 |

## 能力专题

| 文档 | 说明 |
|---|---|
| [音频旁白](./audio-narration.md) | 从演讲者备注到逐页旁白：服务商、声音复刻、时序、PPTX 嵌入 |
| [转场与动画](./animations.md) | 页间转场与页内元素动画的默认行为和自定义方式 |
| [模板使用指南](./templates-guide.md) | 品牌 / 风格 / 版式 / 成品模板的创建与套用 |

## 架构与原理

| 文档 | 说明 |
|---|---|
| [技术路线](./technical-design.md) | 架构、设计哲学、为什么选 SVG → DrawingML |
| [PowerPoint–SVG 能力映射](./powerpoint-svg-mapping.md) | PowerPoint 构造与管线之间逐项能力映射 |
| [模板体系架构](./templates-architecture.md) | 品牌 / 风格 / 版式 / 成品模板体系的设计 |

## 项目方向

Lisa's PPT 自身的方向见 [`PLAN.md`](../../PLAN.md)；来源记录见 [`PROVENANCE.md`](../PROVENANCE.md) 与根目录的 [`NOTICE`](../../NOTICE)。上游的两份 README 与 slide-master 的韩文 README 原样存放在 [`upstream/`](../upstream/) 作为导入记录（其中的相对链接可能失效）；上游的定位、路线图与维护者文档没有带过来。

| 文档 | 说明 |
|---|---|
| [来源记录](../PROVENANCE.md)（英文） | 导入点、每个移植文件、删除项、内置字体，以及回移修正的记录方式 |
| [PPT Master README_CN](../upstream/README_CN.ppt-master.md) | 上游 v6.1.0 的中文 README，仅供参考 |
| [slide-master README（韩文）](../upstream/README.slide-master.ko.md) | slide-master 在移植 commit 处的 README，仅供参考 |

## 贡献者规则

| 文档 | 说明 |
|---|---|
| [风格规则](../rules/README.md)（英文） | 面向提示词参考文件与 Python 脚本的贡献者风格规则 |
