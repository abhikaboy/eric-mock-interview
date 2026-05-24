from pokedex import Pokedex, Pokemon, PokemonType, Stats

pokedex = Pokedex()
pokedex.add(
    Pokemon(
        number=6,
        name="Charizard",
        types=[PokemonType.FIRE, PokemonType.FLYING],
        stats=Stats(hp=78, attack=84, defense=78),
    )
)

results = pokedex.find_by_name("char")
print([pokemon.get_display_name() for pokemon in results["items"]])
