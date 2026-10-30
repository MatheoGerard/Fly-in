*This project has been created as part of the 42 curriculum by mgerard.*

# Fly-In

## Description

**Fly-In** is a drone routing simulation with a graphical interface.

A fleet of drones starts in a single **start hub** and must reach a single **end hub** through a network of zones (hubs) linked by connections. The goal is to move **all** drones to the end in as few simulation turns as possible, while respecting the constraints of the map:

- every hub has a maximum number of drones that can be in it at the same time (`max_drones`);
- every connection has a maximum number of drones that can use it in the same turn (`max_link_capacity`);
- every zone has a type that changes how it can be crossed (`normal`, `priority`, `restricted`, `blocked`).

The project is split in two parts:

1. **A parser and a path planner** that read a map file, validate it and compute, for every drone, the exact sequence of hubs it follows turn after turn.
2. **A pygame visualizer** that displays the map and plays the computed solution (automatically or turn by turn), with menus, one theme per difficulty level, music and smooth drone animations.

### Features

- Strict map parser with explicit error messages (invalid metadata, duplicated connections, unknown zone type, several start/end hubs, ...).
- Multi-drone planner that handles hub capacity, link capacity, restricted zones, priority zones and blocked zones.
- 10 ready-to-use maps in 4 difficulty levels (easy, medium, hard, challenger).
- Interactive visualizer: menus, themed backgrounds, colored hubs, turn counter, hover information, play / pause / step-by-step modes, fullscreen.
- Turn-by-turn textual output of the solution.

## Instructions

### Requirements

- Python **3.12**
- [uv](https://docs.astral.sh/uv/) (dependency manager)
- A graphical environment and an audio output (the game opens a window and plays music with `pygame.mixer`)
- Dependencies (installed automatically by `uv`): `pygame >= 2.6.1`, `pydantic >= 2.13.5`, `parse >= 1.22.2`

### Installation

```bash
make install     # runs `uv sync`
```

### Execution

Run everything **from the root of the repository** (maps, textures and sounds are loaded with relative paths):

```bash
make run         # plays an animated ASCII banner, then runs `uv run python -m src`
```

Other useful rules:

```bash
make debug       # runs the program under pdb
make lint        # flake8 + mypy (strict flags)
make clean       # removes __pycache__, .pyc, .mypy_cache and .pytest_cache
```

> `make lint` needs `flake8` and `mypy`. If they are not installed in your environment: `uv add --dev flake8 mypy`.

### Controls

| Screen | Key | Action |
| --- | --- | --- |
| Menus | `Up` / `Down` | Change the selection (PLAY / QUIT, difficulty, map) |
| Menus | `Enter` | Validate |
| Menus and map | `Esc` | Go back one screen |
| Any screen | `Space` | Toggle fullscreen |
| Map | `P` | Start / stop the automatic simulation (1 turn every 0.5 s) |
| Map (not playing) | `Up` | Play the next turn manually |
| Map | mouse over a hub | Show `name current_drones/max_drones` |

### Project structure

```
.
├── Makefile
├── banner.txt              # ASCII art displayed by `make run`
├── pyproject.toml / uv.lock
├── maps/                   # easy / medium / hard / challenger map files
├── sound/                  # one music track per difficulty + menu music
├── textures/               # menus, backgrounds, buttons, drone sprite
└── src/
    ├── __main__.py         # entry point and main loop
    └── fly_in/
        ├── maps_parser.py  # reads and validates map files
        ├── hub.py          # Hub model (zone type, capacity, cost, position)
        ├── connexion.py    # Connexion model (link + link capacity)
        ├── map_class.py    # Map: hubs, links, drones, start / end validation
        ├── simulation_init.py  # parser -> Map
        ├── drone.py        # Drone: path planning + movement + animation
        ├── display.py      # all the drawing code (Visualization)
        ├── play_mode.py    # automatic turn timer
        ├── input.py        # keyboard and mouse handling
        ├── main_menu.py    # menu buttons and selections
        ├── game_state.py   # which screen is active
        └── sound_player.py # music selection
```

## Map format (input)

A map is a text file. Lines starting with `#` are comments.

```
nb_drones: <int>                                  # must be the first line

start_hub: <name> <x> <y> [metadata]
hub:       <name> <x> <y> [metadata]
end_hub:   <name> <x> <y> [metadata]

connection: <name_a>-<name_b> [max_link_capacity=<int>]
```

Hub metadata (all optional, separated by spaces, between brackets):

| Key | Default | Meaning |
| --- | --- | --- |
| `zone` | `normal` | `normal` (1 turn), `priority` (1 turn, preferred), `restricted` (2 turns), `blocked` (cannot be entered) |
| `color` | `none` | Display color of the hub (any pygame color name, or `none` / `rainbow`) |
| `max_drones` | `1` | Maximum number of drones in the hub at the same time |

Other rules: hub names cannot contain `-`, a connection cannot be declared twice, there must be exactly one start and one end hub, and `max_link_capacity` defaults to `1`. The start and end hubs can hold every drone.

## Algorithm and implementation strategy

### Problem modeling

The map is an undirected graph: hubs are vertices, connections are edges. Moving to a zone costs a number of **turns**:

| Zone | Cost (`Hub.define_cost`) | Duration in turns |
| --- | --- | --- |
| `normal` | `1.0` | 1 |
| `restricted` | `2.0` | 2 |
| `priority` | `0.999999` | 1 (`max(1, int(cost))`) |
| `blocked` | `inf` | never entered |

The `priority` cost is intentionally *slightly lower* than a normal zone. Durations are rounded to whole turns, but the planner also uses priority zones as a **tie-breaker** (see below).

Because drones must wait for each other (capacities), the problem is not a simple shortest path: the position of a drone depends on **time**. The planner therefore searches in a **time-expanded graph**, where a state is a pair `(turn, hub)`.

### Planning drone by drone (prioritized planning)

`Drone.dijsktra` plans one drone at a time, and all drones share one **reservation table** (`occupancy`):

- `occupancy[(turn, hub)]` = number of drones in `hub` at `turn`;
- `occupancy[(turn, hub_a, hub_b)]` = number of drones that start using the link at `turn`.

For each drone, in order:

1. **Search.** A Dijkstra search runs on states `(turn, hub)`. From a state, a drone can either **wait** one turn in the same hub, or **move** to a neighbor (taking 1 or 2 turns depending on the zone). Blocked zones are skipped.
2. **Capacity checks.** A transition is allowed only if the destination hub is not full at the arrival turn (`occupancy < max_drone`, ignored for start and end) and if the link is not full (`occupancy < max_link_capacity`).
3. **Priority queue order.** States are popped from a heap ordered by `(turn, -priority_score)`: the earliest turn first, and among equal turns the path that crossed the most `priority` zones. The first time the end hub is popped, the earliest possible arrival has been found.
4. **Reconstruction.** The path is rebuilt from `came_from` and converted into a **timeline** (`true_way`): one entry per turn, either a hub name or `a-b` while the drone is on the way through a restricted link.
5. **Reservation.** The hubs and links used by this drone are added to `occupancy`, so the next drones automatically avoid them or wait.

Drones are identical and start together, so the first drone gets the best route and the following ones naturally spread over alternative routes or wait at the start when everything is saturated.

### Why this approach?

- **Correct by construction**: the reservation table guarantees that no capacity is ever exceeded, including the "wait" moves.
- **Simple and fast**: one search per drone over at most `max_turn × hubs` states (`max_turn = 500`). The hardest provided map is solved in about 0.1 s.
- **Handles all zone types** with a single model (waiting, 2-turn moves, blocked and priority zones).
- **Deterministic**, which makes the output easy to test and compare.

### Limits

- Planning drone by drone is a *greedy* heuristic: the result depends on the order of the drones and is not guaranteed to be globally optimal (more advanced approaches exist, see Resources).
- If no path exists within `max_turn`, the program prints `No path available` and the drone does not move.

### Results on the provided maps

| Map | Drones | Turns |
| --- | --- | --- |
| easy / 01_linear_path | 2 | 4 |
| easy / 02_simple_fork | 4 | 4 |
| easy / 03_basic_capacity | 4 | 4 |
| medium / 01_dead_end_trap | 5 | 8 |
| medium / 02_circular_loop | 6 | 10 |
| medium / 03_priority_puzzle | 5 | 6 |
| hard / 01_maze_nightmare | 8 | 13 |
| hard / 02_capacity_hell | 12 | 16 |
| hard / 03_ultimate_challenge | 15 | 26 |
| challenger / 01_the_impossible_dream | 25 | 43 |

## Visual representation

The visualizer is built with pygame (1920×1080 window, 60 FPS). It makes the simulation easy to follow and to debug:

- **Menus and themes.** A main menu, a difficulty selection and a map selection lead to the simulation. Each difficulty has its own music, and each map has its own background, so the player always knows where they are.
- **Automatic scaling.** Hub coordinates are scaled to the window using the bounding box of the map (with a one-cell margin), so any map fits the screen. The `y` axis points up, like on a regular graph.
- **Colored hubs and visible links.** Hubs use the `color` given in the map file, which makes zone roles (bottleneck, priority path, ...) readable at a glance. Connections are drawn as white lines.
- **Smooth drone animation.** Drones glide from one hub to the next instead of teleporting. The display position (`render_position`) is moved toward the logical position with a frame-rate independent exponential smoothing (`ANIMATION_SPEED`), so the animation also works with fast manual stepping.
- **Restricted zones.** A drone crossing a restricted link is drawn halfway on the link during its first turn, then arrives at the hub on the second turn.
- **No hidden drones.** When several drones share the same hub, they are laid out on a small grid around it instead of being drawn on top of each other.
- **Turn counter.** `turn/total` is displayed in the top-left corner.
- **Hover information.** Moving the mouse over a hub displays its name and its occupancy (`current/max`).
- **Two playback modes.** `P` plays the simulation automatically (one turn every 0.5 s, `TURN_DURATION` in `play_mode.py`); when paused, `Up` advances turn by turn to inspect a situation in detail.
- **Fullscreen** with `Space`.

## Example

### Input: `maps/easy/03_basic_capacity.txt`

```
# Easy Level 3: Basic capacity management
nb_drones: 4

start_hub: start 0 0 [color=green]
hub: bottleneck 1 0 [color=orange max_drones=2]
hub: wide_area 2 0 [color=blue max_drones=3]
end_hub: goal 3 0 [color=red]

connection: start-bottleneck [max_link_capacity=4]
connection: bottleneck-wide_area [max_link_capacity=4]
connection: wide_area-goal [max_link_capacity=4]
```

### Expected output

The solution is appended to `text.txt` in the current directory when the map is loaded. There is one line per turn, and each token is `D<drone>-<destination>`. A drone that does not move in a turn is not listed.

```
D0-bottleneck D1-bottleneck
D0-wide_area D1-wide_area D2-bottleneck D3-bottleneck
D0-goal D1-goal D2-wide_area D3-wide_area
D2-goal D3-goal
Total : 4 tours
```

`bottleneck` only holds 2 drones, so D2 and D3 wait at the start for one turn: 4 turns are the minimum for this map.

### Example with a restricted and a priority zone: `maps/medium/03_priority_puzzle.txt`

```
D0-fast_junction D2-start-slow_path1
D0-fast_path D1-fast_junction D2-slow_path1 D4-start-slow_path1
D0-merge_point D1-fast_path D2-slow_path2 D3-fast_junction D4-slow_path1
D0-goal D1-merge_point D2-merge_point D3-fast_path D4-slow_path2
D1-goal D2-goal D3-merge_point D4-merge_point
D3-goal D4-goal
Total : 6 tours
```

A token with two hub names, like `D2-start-slow_path1`, means that the drone is **in transit on the link** `start-slow_path1`: that is how a restricted zone (2 turns) shows up in the output. The priority path (`fast_junction`, `fast_path`) is used by D0, D1 and D3, while D2 and D4 take the longer restricted path because the fast one is saturated.

## Resources

### References

- [Dijkstra's algorithm: Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Introduction to A\*: Red Blob Games](https://www.redblobgames.com/pathfinding/a-star/introduction.html), graph search and priority queues explained visually
- D. Silver, *Cooperative Pathfinding*, AIIDE 2005: reservation tables and time-expanded search for several agents (the idea behind the planner)
- R. Stern et al., *Multi-Agent Pathfinding: Definitions, Variants, and Benchmarks*, SoCS 2019: overview of multi-agent path finding and of optimal approaches
- [Python `heapq` documentation](https://docs.python.org/3/library/heapq.html)
- [pygame documentation](https://www.pygame.org/docs/)
- [pydantic documentation](https://docs.pydantic.dev/)
- [`parse` on PyPI](https://pypi.org/project/parse/)
- [uv documentation](https://docs.astral.sh/uv/)
- https://en.wikipedia.org/wiki/Graph_theory

### Use of AI

AI (Claude, by Anthropic) was used as an assistant for the following tasks:

- **Makefile**: the animated rainbow ASCII banner displayed by `make run`.
- **Documentation**: drafting of this README, based on the source code.

All AI-generated content was reviewed and tested before being kept.
