from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import ceil


class PokemonType(str, Enum):
    NORMAL = "Normal"
    FIRE = "Fire"
    WATER = "Water"
    GRASS = "Grass"
    ELECTRIC = "Electric"
    FLYING = "Flying"
    DRAGON = "Dragon"


@dataclass(frozen=True)
class Stats:
    hp: int
    attack: int
    defense: int

    def __add__(self, other: "Stats") -> "Stats":
        return Stats(
            hp=self.hp + other.hp,
            attack=self.attack + other.attack,
            defense=self.defense + other.defense,
        )


@dataclass(frozen=True)
class Ability:
    name: str


@dataclass(frozen=True)
class Form:
    name: str
    type_override: list[PokemonType] | None = None
    stat_bonus: Stats | None = None
    extra_abilities: list[Ability] = field(default_factory=list)


@dataclass
class Pokemon:
    number: int
    name: str
    types: list[PokemonType]
    stats: Stats
    abilities: list[Ability] = field(default_factory=list)
    traits: list[str] = field(default_factory=list)
    form: Form | None = None

    def get_display_name(self) -> str:
        parts = []
        if self.traits:
            parts.extend(self.traits)
        if self.form:
            parts.append(self.form.name)
        parts.append(self.name)
        return " ".join(parts)

    def get_effective_types(self) -> list[PokemonType]:
        if self.form and self.form.type_override:
            return self.form.type_override
        return self.types

    def get_effective_stats(self) -> Stats:
        if self.form and self.form.stat_bonus:
            return self.stats + self.form.stat_bonus
        return self.stats

    def has_trait(self, trait: str) -> bool:
        return trait in self.traits

    def get_effective_abilities(self) -> list[Ability]:
        if self.form and self.form.extra_abilities:
            return [*self.abilities, *self.form.extra_abilities]
        return self.abilities


class Pokedex:
    def __init__(self) -> None:
        self._pokemon: list[Pokemon] = []

    def add(self, pokemon: Pokemon) -> None:
        self._pokemon.append(pokemon)

    def find_by_name(self, name: str, page: int = 1, page_size: int = 10) -> dict:
        filtered = [p for p in self._pokemon if name.lower() in p.name.lower()]
        return self._paginate(filtered, page=page, page_size=page_size)

    def filter_by_type(
        self,
        pokemon_type: PokemonType,
        page: int = 1,
        page_size: int = 10,
    ) -> dict:
        filtered = [p for p in self._pokemon if pokemon_type in p.get_effective_types()]
        return self._paginate(filtered, page=page, page_size=page_size)

    def list_all(self, page: int = 1, page_size: int = 10) -> dict:
        return self._paginate(self._pokemon, page=page, page_size=page_size)

    def find_common_pokemon(self, other_pokedex: "Pokedex") -> list[Pokemon]:
        raise NotImplementedError("Implement in assessment part E")

    def find_unique_pokemon(self, other_pokedex: "Pokedex") -> list[Pokemon]:
        raise NotImplementedError("Implement in assessment part E")

    def merge(self, other_pokedex: "Pokedex") -> "Pokedex":
        raise NotImplementedError("Implement in assessment part E")

    def diff(self, other_pokedex: "Pokedex") -> dict:
        raise NotImplementedError("Implement in assessment part F")

    @staticmethod
    def _paginate(items: list[Pokemon], page: int, page_size: int) -> dict:
        if page < 1:
            raise ValueError("page must be >= 1")
        if page_size < 1:
            raise ValueError("page_size must be >= 1")

        total_items = len(items)
        total_pages = ceil(total_items / page_size) if total_items else 0
        start = (page - 1) * page_size
        end = start + page_size

        return {
            "items": items[start:end],
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
        }
