# Universal Review · 通用严审

One reusable Agent Skill for rigorous review of any task or deliverable. It checks the overall work first, then wording, numbers and natural expression, and rechecks the final corrected version.

一个统一入口，适用于工程、软件、知识库、报告、数据分析、计划、设计、翻译、短文本及其他任务。目标是在明确范围内逐项查清事实与证据，减少遗漏，不承诺任何模型或任务绝对零错误。

## 安装

使用 [Skills CLI](https://github.com/vercel-labs/skills) 从本仓库全局安装：

```sh
npx skills add yunming-yan/universal-review-skill --skill universal-review --global --yes
```

仅指定某个Agent时，可添加其实际支持的名称，例如：

```sh
npx skills add yunming-yan/universal-review-skill --skill universal-review --global --agent codex --yes
```

`--global`是当前用户级安装，供各项目使用。具体发现目录和可用工具由Agent运行环境决定；Skill本身不提供文件访问或Subagent能力。

## 使用

```text
使用 $universal-review 对当前任务进行完整独立终审，在已有授权范围内修正问题，最后复审全部修正及其影响。
```

也可以限定实际范围：

```text
使用 $universal-review 审查这份报告的文字、数字和事实，保留原意，去掉空泛修饰，提供自然可读的修改稿。
```

只审查、不修改成品时，请直接说明。已有授权的常规修正自动闭环；Skill不会自行授予发布、付款、删除或关闭应用等权限。

## 审查精度与流程

1. 核真实目标、有效要求、全部适用对象与依赖，完整读源并区分当前版本、历史证据和未知。
2. 检查事实、逻辑、结构、实际实现/调用链、流程、版本、权限和适用验证。
3. 再核文字、数字和表达自然度，保护主体、状态、引用、限定词、单位、口径和机器字面量。预算不能润色成报价，预计不能润色成已验证。
4. 在授权内作最小必要修正，保留原件和失败，完成实际受影响对象的同步与验证。
5. 最后一次修改后，独立复审完整修正并集和依赖，包括最后的文字润色；最终结论对应同一实际版本。

整体项目或完整独审采用 **33个真实独立审查职责**，涵盖专项、异人交叉和全局反查；并发由协调者按依赖及平台能力安排。指定稿件、局部对象或已分配专项按其明确范围完整审查，不把局部结果冒称全项目通过。没有代码的任务不被强加代码或某种架构检查。

真实独立能力、源材料或验证工具不足时，继续完成可核部分并明确限制，不模拟身份或伪造PASS。历史版本留档；活动规则、入口和交付版本保持明确。

## 管理

```sh
# 查看当前用户全局Skill
npx skills list --global

# 仅更新本Skill，继续使用已登记的GitHub来源
npx skills update universal-review --global --yes

# 卸载本Skill
npx skills remove universal-review --global --yes
```

命令接口核对版本：Skills CLI 1.7.0。不要用不带名称的批量更新/卸载命令替代只管理本Skill的操作。

## 包结构与验证

`skills/universal-review/SKILL.md`是唯一入口；`references/`提供流程、33职责、任务分支、证据规则和文字数字方法。所有引用随技能一起安装，不依赖特定用户目录、私有知识库或其他Skill。

合成行为场景与评分依据见 [evals](evals/README.md)。语法校验、行为测试和人工独立审查回答不同问题；测试结果不能被解释为所有任务的无遗漏保证。

本仓库不包含生产知识库、私人审计资料或真实业务数据。所有评估样例均为合成数据。

## License

[MIT](LICENSE)
