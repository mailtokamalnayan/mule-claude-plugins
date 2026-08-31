# mule-claude-plugins

Claude Code plugins for the mule-ui design team.

## Install

In Claude Code, run:

```
/plugin marketplace add <org>/mule-claude-plugins
/plugin install mule-explorations@mule-ui
```

Restart Claude Code. Run `/mcp` and sign in to **mobbin** and **figma** (one time). Done.

## Use

```
/mobbin-exploration-team order summary card
/mobbin-exploration-team ~/Desktop/current-design.png
/mobbin-exploration-team https://www.figma.com/design/...?node-id=... --mobile
```

Each run writes one standalone HTML page to `~/Developer/explorations/<subject>/` with three live, clickable design concepts on the mule-ui tokens. Open it in a browser.

## Update

New versions ship through this repo. To get them:

```
/plugin marketplace update mule-ui
```

## Notes

- The plugin bundles the Mobbin and Figma MCP servers. If you already have the official Figma plugin, both work; disable one if the duplicate tools bother you.
- Mobbin is required — the skill refuses to design without pattern research.
- Design tokens are a baked snapshot of the `_lib-mule-ui` Figma library (stickermule light theme). To refresh them, export variables from Figma to JSON and run `python3 plugins/mule-explorations/skills/mobbin-exploration-team/build-tokens.py <export.json>`, then commit and bump the plugin version.
