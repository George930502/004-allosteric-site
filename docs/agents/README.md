# `docs/agents/` — plugin configuration, not subagents

**Do not rename this directory.** The path is a contract. The `mattpocock-skills`
engineering plugin reads `docs/agents/issue-tracker.md` at run time, and it looks for that
exact path. A rename breaks `/triage` and `/code-review` silently, with no error to tell you
why.

## This is not `.claude/agents/`

Two directories in this repository have "agents" in the name. They hold different things.

| Directory         | Holds                                                                                                                  | Who reads it                                  |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| `docs/agents/`    | three configuration files that answer "where do issues live, what are the labels called, where do the domain docs sit" | the installed engineering skills, at run time |
| `.claude/agents/` | subagent definitions, one file per agent, each with its own tools and system prompt                                    | Claude Code, when a subagent is spawned       |

The collision comes from upstream. Neither name is ours to choose.

## The three files

| File               | Answers                                                                                                                                              |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `issue-tracker.md` | Where issues live, and the `gh` commands that reach them. Also the flag for whether external pull requests count as a request surface. It is **off** |
| `triage-labels.md` | The label vocabulary: five state labels and two category labels                                                                                      |
| `domain.md`        | How a skill must consume this repo's domain documentation. Single-context, so `CONTEXT.md` at the root and `docs/adr/` are the whole map             |

`/setup-matt-pocock-skills` writes these files. Edit them directly to change an answer.
Re-run the setup skill only to switch issue trackers or to start over.

## What is ours, and what is not

The three files are configuration for a third-party plugin, so their **shape** follows that
plugin. Their **content** is ours, and `domain.md` in particular carries repo-specific
instructions the plugin cannot infer. Do not let a re-run of the setup skill overwrite it
without reading the diff.
