# Steering rules — LeanScene (starter)

> Drop this into your project as `CLAUDE.md` (or merge it into an existing one).
> It steers an AI agent working in a large Unreal Engine 5 scene to use
> token-efficient queries instead of dumping the whole scene. Tune the task names
> to match your project.

## Prime rule
Never pull the whole scene when a narrow query answers the question. Large
outliner / actor list / asset registry dumps blow up the context window and
degrade accuracy. Prefer the lean LeanScene tools below — each returns a fixed,
minimal payload and reports its own per-call token saving.

## Never do these (the firehose)
- Do **not** dump the full outliner or read the entire actor list to find or
  count actors.
- Do **not** fetch a full, verbose actor description when you only need an
  actor's key fields.
- Do **not** dump the full asset registry to find a handful of offending assets.
- Do **not** take a screenshot or run a vision check to confirm something a cheap
  deterministic check can confirm.

## Use the lean tool for the task
| When you need to… | Use | Instead of |
|---|---|---|
| find / inspect actors near a point | `get_actors_in_radius` | the full actor list / outliner |
| understand the level's structure | `summarize_level` | dumping the outliner |
| read one actor's key fields | `get_actor_brief` | the verbose native "describe actor" |
| find assets with unlinked materials | `get_unlinked_materials` | scanning the whole asset registry |
| find assets missing LODs | `get_assets_missing_lods` | scanning the whole asset registry |

## Verify before vision
Before any screenshot or vision check, confirm placement with the cheap
deterministic checks — they cost a few tokens and are exact:
- `verify_bounds` — is an actor's bounding box what you expect?
- `verify_overlap` — do two actors overlap?
- `verify_transform` — is an actor at the expected location?

Only fall back to a vision check if a `verify_*` tool cannot answer the question.

## Note
This guidance biases tool selection through tool descriptions and these rules
only. It does not modify or remove the engine's native tools — you may still see
native tools in the list; the rule is simply to prefer the lean ones above.
