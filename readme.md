# Pokémon Pokédex OOP Exercise

## Overview

You are building a simplified Pokédex system.

The goal of this exercise is to evaluate:

- object-oriented design
- inheritance vs. composition tradeoffs
- API design
- data modeling
- clean, extensible code
- reasoning about identity and equality

You may use AI tools during the exercise, but you should be prepared to explain and justify your design decisions.

This is intentionally open-ended. Focus on writing code that is clean, maintainable, and easy to extend.

---

# Part A — Basic Pokémon Model

Implement a `Pokemon` class.

Each Pokémon should contain:

- Pokédex number
- name
- one or more types
- stats:
  - HP
  - Attack
  - Defense

Required methods:

```python
pokemon.get_display_name()
pokemon.get_effective_types()
pokemon.get_effective_stats()
```

For Part A, these methods may simply return the base values.

---

# Part B — Pokédex Storage, Search, and Pagination

Implement a `Pokedex` class.

Required methods:

```python
pokedex.add(pokemon)

pokedex.find_by_name(
    name,
    page=1,
    page_size=10,
)

pokedex.filter_by_type(
    pokemon_type,
    page=1,
    page_size=10,
)

pokedex.list_all(
    page=1,
    page_size=10,
)
```

---

## Pagination Requirements

All query methods should support pagination.

- `page` is 1-indexed
- `page_size` must be positive
- Pagination should be deterministic
- Query methods should return metadata along with results

Suggested return shape:

```python
{
    "items": [...],
    "page": 1,
    "page_size": 10,
    "total_items": 37,
    "total_pages": 4
}
```

---

## Search Requirements

- Name lookup should be case-insensitive.
- Name lookup may return multiple results.
- Filtering by type should return all matching Pokémon.
- Your solution should work efficiently as the Pokédex grows.

---

# Part C — Forms

Add support for Pokémon forms.

Examples:

- Mega Charizard X
- Alolan Vulpix
- Gigantamax Pikachu

A form may modify:

- display name
- types
- stats
- abilities

Example:

```python
mega_x = Form(
    name="Mega X",
    type_override=[PokemonType.FIRE, PokemonType.DRAGON],
    stat_bonus=Stats(hp=0, attack=46, defense=33),
)
```

Required behavior:

```python
pokemon.get_display_name()
pokemon.get_effective_types()
pokemon.get_effective_stats()
```

should account for the active form.

---

# Part D — Traits and Abilities

Add support for traits and abilities.

Traits are simple labels such as:

- Shiny
- Legendary
- Starter

Abilities are named metadata or behaviors such as:

- Blaze
- Levitate
- Static

Required methods:

```python
pokemon.has_trait("Shiny")
pokemon.get_effective_abilities()
```

Traits should be able to stack with forms.

Example:

```text
Shiny Mega X Charizard
```

---

# Part E — Merge and Compare Pokédexes

You are given another `Pokedex`.

Implement:

```python
pokedex.find_common_pokemon(other_pokedex)
pokedex.find_unique_pokemon(other_pokedex)
pokedex.merge(other_pokedex)
```

---

## `find_common_pokemon(other_pokedex)`

Returns Pokémon that exist in both Pokédexes.

Two Pokémon are considered the same if they have the same:

```python
(number, display_name)
```

---

## `find_unique_pokemon(other_pokedex)`

Returns Pokémon that exist in the current Pokédex but not in `other_pokedex`.

---

## `merge(other_pokedex)`

Returns a new `Pokedex` containing Pokémon from both Pokédexes.

Duplicate Pokémon should only appear once.

Do not mutate either original Pokédex.

---

# Part F — Pokédex Diff

Implement:

```python
pokedex.diff(other_pokedex)
```

This method should return all differences between two Pokédexes.

---

## Identity Rules

For Part F, two Pokémon represent the same base Pokémon if they have the same:

```python
(number, name)
```

Do NOT use display name for identity in Part F.

This means:

```text
Charizard
Shiny Charizard
Mega X Charizard
```

should be treated as the same Pokémon with different attributes.

---

## Required Output

Return a dictionary with:

```python
{
    "added": [],
    "removed": [],
    "changed": [],
    "unchanged": []
}
```

Where:

- `added` = Pokémon only in `other_pokedex`
- `removed` = Pokémon only in the current Pokédex
- `changed` = Pokémon present in both, but with different data
- `unchanged` = Pokémon present in both with identical data

---

## Changed Pokémon Format

Each changed Pokémon should include:

```python
{
    "before": old_pokemon,
    "after": new_pokemon,
    "changes": {
        "stats.attack": (55, 60),
        "traits": ([], ["Shiny"]),
        "form.name": (None, "Mega X")
    }
}
```

---

## Fields to Compare

Compare:

- types
- stats
- abilities
- traits
- form

For `form`, compare:

- form name
- type override
- stat bonus
- extra abilities

Comparison rules:

- type order should not matter
- trait order should not matter
- ability order should not matter
- ability comparison may use ability names only
- output should be deterministic

---

# Example Usage

```python
charizard = Pokemon(
    number=6,
    name="Charizard",
    types=[PokemonType.FIRE, PokemonType.FLYING],
    stats=Stats(hp=78, attack=84, defense=78),
)

mega_x = Form(
    name="Mega X",
    type_override=[PokemonType.FIRE, PokemonType.DRAGON],
    stat_bonus=Stats(hp=0, attack=46, defense=33),
)

charizard.form = mega_x
charizard.traits.append("Shiny")

print(charizard.get_display_name())
```

Expected:

```text
Shiny Mega X Charizard
```

---

# Notes

You do NOT need to perfectly model Pokémon game mechanics.

Prefer:

- clean abstractions
- readable code
- maintainable APIs
- thoughtful tradeoffs

over overengineering.
