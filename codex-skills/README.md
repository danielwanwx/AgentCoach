# Codex Skills

This directory contains reusable Codex skills published from this repository.

## Senior SDE Interview Script

Path: `codex-skills/senior-sde-interview-script`

This skill converts technical interview excerpts, especially system design and API design notes, into concise senior SDE candidate speaking scripts. It produces bilingual Chinese and English output by default:

- one-sentence summaries in Chinese and English
- a Chinese speakable interview answer
- an English speakable interview answer
- 30-second versions in both languages
- optional bilingual follow-up prep when the topic has useful senior-level tradeoffs

## Install

Copy the skill folder into your local Codex skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/danielwanwx/AgentCoach.git /tmp/agentcoach-skills
cp -R /tmp/agentcoach-skills/codex-skills/senior-sde-interview-script ~/.codex/skills/
```

Then start a new Codex session and invoke it with:

```text
Use $senior-sde-interview-script to turn this technical excerpt into bilingual senior SDE interview scripts.
```

## 中文说明

这个目录用于分享可复用的 Codex skills。

`senior-sde-interview-script` 会把技术面试材料转换成 senior SDE candidate 可以直接讲的中英文面试底稿。默认输出包括：

- 中文和英文一句话总结
- 中文可直接讲版本
- 英文可直接讲版本
- 中英文 30 秒短版
- 必要时补充中英文追问准备
