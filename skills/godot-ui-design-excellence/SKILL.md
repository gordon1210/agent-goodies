---
name: godot-ui-design-excellence
description: >-
  Design, implement, critique, and polish distinctive game UI in Godot: visual art
  direction, HUDs, menus, inventories, strategy dashboards, typography, materials,
  motion, controller navigation, accessibility, and in-engine visual validation.
  Use for premium or AAA-quality interface requests, Expedition 33 / Frostpunk 2
  references, UI redesigns, and interfaces that work but look generic. Not for
  website design, general gameplay implementation, or engine migration.
---

# Godot UI Design Excellence

Produce a coherent, playable interface with an authored visual identity. "AAA" is
an ambition for craft, not an aesthetic preset or a quality guarantee. Preserve
the project's identity; never substitute a generic dashboard, fantasy skin, or
unrequested redesign.

## Start with the right amount of context

Inspect the current screen, project instructions, engine version, renderer, target
devices, existing UI scenes/themes, and available tools. Read
[discovery](references/discovery.md) for new work; skip repeated discovery for a
small established task. Ask about genuinely unresolved design requirements rather
than inventing the user's game. Do not ask questions already answered by the repo.

Read **only the relevant rows below**. Usually load 2–4 modules for the current
stage, not the entire library. Source and example files are optional lookups.
Finish a stage, persist decisions, then load the next stage's references. For a
small fix, choose the narrow repair route without restarting art direction.

| Task / symptom | Read |
|---|---|
| New visual identity, references, "make it modern" | [Reference analysis](references/reference-analysis.md), [art direction](references/art-direction.md) |
| Generic layout, weak hierarchy | [Composition](references/composition.md), [critique and repair](references/critique-and-repair.md) |
| Fonts, numbers, readability | [Typography](references/typography.md), [Godot text](references/godot-text.md) |
| Colors, texture, ornaments, icons | [Color and materials](references/color-materials.md), [iconography](references/iconography.md) |
| State language and reusable components | [Component states](references/component-states.md), [Godot themes](references/godot-themes.md) |
| Information architecture and decisions | [Interaction](references/interaction-information.md) |
| Cinematic / painterly RPG | [RPG direction](references/cinematic-rpg.md), [worked RPG example](examples/ashen-atlas.md) |
| Dense management / strategy | [Strategy direction](references/strategy-management.md), [worked strategy example](examples/meridian-station.md) |
| Expressive or tactical identity | [Other visual directions](references/other-directions.md) |
| Inventory, equipment, build comparison | [Inventory and buildcraft](references/inventory-buildcraft.md) |
| Maps, research trees, spatial navigation | [Maps and trees](references/maps-trees.md) |
| Tooltips, alerts, notifications | [Tooltips and notifications](references/tooltips-notifications.md) |
| Settings, confirmation, dialogue | [Settings and dialogue](references/settings-dialogue.md) |
| Motion / transitions / sound | [Motion design](references/motion-design.md), [audio feedback](references/audio-feedback.md) |
| Art production / generated assets | [Asset production](references/asset-production.md) |
| Layout, scaling, safe areas | [Godot layout](references/godot-layout.md) |
| Input leak, focus, modal, device switching | [Godot input](references/godot-input.md) |
| Interrupted animations, layout fighting tweens | [Godot animation](references/godot-animation.md) |
| Shader, blur, masks, custom drawing | [Godot rendering](references/godot-rendering.md) |
| Portraits, 3D previews, world-space UI | [Godot spatial UI](references/godot-spatial-ui.md) |
| Data binding, loading, large lists, performance | [Godot data and performance](references/godot-data-performance.md) |
| Accessibility or localization acceptance | [Accessibility](references/accessibility.md), [Godot text](references/godot-text.md) |
| Verify or review a delivered screen | [Visual validation](references/visual-validation.md), [critique and repair](references/critique-and-repair.md) |
| Permissions, tools, external references | [Evidence and safety](references/evidence-safety.md) |
| Primary sources / changing APIs | [Source register](references/sources.md) |

## Production loop

1. **Frame the decision.** Who is acting, what must they notice, what can they do,
   and what is the cost of a mistake? Capture constraints in the
   [design brief](assets/design-brief.md), proportionate to the request.
2. **Observe references.** Inspect actual screenshots and, for motion claims,
   recordings. Distinguish shipped screens, concepts, and original proposals.
   Extract a visual grammar, not a bag of decorative motifs.
3. **Choose a direction.** Define composition, typography, shape/material roles,
   information hierarchy, and motion character. Explore meaningfully different
   options only when direction is open. Respect explicit delegation of choices.
4. **Build one representative screen.** Use real or labeled fixture data, real
   background variation, and normal/focused/disabled/error states. Use the
   [screen contract](assets/screen-contract.md). Do not scale out an unproven skin.
5. **Implement natively.** Use semantic Controls and reusable scenes, Themes and
   variants, authored assets, and bounded decorative effects. Detect the installed
   Godot version before using version-sensitive APIs; never upgrade it implicitly.
6. **Inspect and revise.** Run the real scene, capture it at target sizes, exercise
   input and animation interruptions, then correct the most consequential visual
   or interaction failure. Use the [visual review](assets/visual-review.md).
7. **Generalize after acceptance.** Extract components and tokens from the accepted
   screen, apply to sibling screens, and record exceptions. Hand off evidence and
   remaining limits with the [handoff](assets/handoff.md).

## Non-negotiable distinctions

- Functional correctness, visual fidelity, usability, and accessibility are
  separate acceptance axes. A polished screenshot cannot compensate for a trapped
  user; a passing build cannot prove visual quality.
- "Modern" does not require glass, neon, huge cards, tiny text, or springy buttons.
  Use texture and motion for a stated purpose, not to conceal weak hierarchy.
- Keep functional text and interaction native. Do not ship a flattened generated
  screenshot as an interface. Inspect actual alpha, scale, and asset provenance.
- Focus, hover, selection, equipped, locked, disabled, and busy are not synonyms.
  Decorative transitions must not silently delay input or commit an action.
- No blanket ban on manual coordinates, continuous updates, or linear motion.
  Choose the appropriate coordinate space, update cadence, and semantic behavior.
- No invented runtime tests, fabricated screenshots, invisible tool capabilities,
  or claims of accessibility certification. Label unavailable checks explicitly.

Persist decisions and evidence in the project rather than repeating long reference
text in chat. For delegation, send the relevant module names, screen contract,
asset paths, and acceptance checks—not the whole skill. For installation, tools,
validation scripts, and evaluation cases, see [README](README.md).
