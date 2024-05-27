# Pokémon Go Pokédex

---
### CSCA 5028 Final Project - Applications of Software Architecture for Big Data


## Table of Contents

---


## Requirements Elicitation

---
- ### What problem is the product aimed at solving?
    And easy way to access nearly all available in-game information such as Pokémon identification, individual statistics for battling, evolutionary lines, etc.
- ### Who is the product geared towards (targeted audience)?
    Pokémon Go users.
- ### How is my product unique?
    The uniqueness of this product comes from its goal of singling out a Pokémon Go-specific online Pokédex where users can go to reference an up-to-date culmination of all available data on each Pokémon within the game.

---

This program creates a postgresql database via Heroku.. It pulls from a Pokemon Go api that fills the database with the pokemon information needed in the webpages.

This is a screenshot of the home page where you can select the pokemon you want to search.
![homepage.png](images%2Fhomepage.png)

It can sort through the selected types and will present you with all available options that meet the criteria. You can start with either Type 1 or Type 2 and leave the other blank and it will still work the same.
![Type1.png](images%2FType1.png)

This also applies to when both Types are selected.
![Type1Type2.png](images%2FType1Type2.png)

Then if you start to type, it will automatically filter it even further to what is types.
![TypeFilter.png](images%2FTypeFilter.png)

Finally, once you select a pokemon and press Find Pokemon, it will direct you to the pokemon's page where it will display its information that is available and relevant to the Pokemon Go app.
You can progress forward to the next pokemon, or to the previous in regards to their assigned Pokedex Number. You can also return to the home page. 

The program calculates the Combat Power (CP) based on the Attack, Defense, and HP stats to give the maximum CP at levels 40 and 50 for a Pokemon with Max Individual Values (IV) which are 15/15/15.

It then also displays the Attack, Defense, and HP stats which are set by the game. And the table shows how strong the Pokemon's three stats are compared to the highest respective stat currently available in the game, in which it finds dynamically each time the page is reloaded in case a new pokemon was added that has an even higher stat.
![PokemonPage.png](images%2FPokemonPage.png)
