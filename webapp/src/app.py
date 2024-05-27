from __future__ import annotations
from sqlalchemy import create_engine, Column, Integer, desc, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import requests
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, render_template, jsonify, session, request
from flask_sqlalchemy import SQLAlchemy

import math
import json
from datetime import datetime
from sqlalchemy import DateTime, Date
import os
import psycopg2
from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph
from typing import Protocol
import requests
import logging
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import create_engine, Integer, Column, String, and_, or_, func, inspect, event, ForeignKey
from sqlalchemy.orm import Session, relationship, foreign, remote, backref, joinedload, contains_eager

from typing import List

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.orm import contains_eager
from typing import List


from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import select
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)  # , template_folder='../html')
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://igwtxlzgwupcpt:202664d18050f7c8d5cb75ecde7f06d1992f83b97764a25a633fceb57e69e474@ec2-3-95-121-6.compute-1.amazonaws.com:5432/d83dkh62g54cqm'
app.secret_key = 'secretkey123.'
db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])


class hash_data_db(db.Model):
    __tablename__ = "hash_data_db"
    id = db.Column(db.Integer, primary_key=True)
    api_filename = db.Column(db.String(255))
    full_path = db.Column(db.String(255))
    hash_md5 = db.Column(db.String(32))
    hash_sha1 = db.Column(db.String(40))
    hash_sha256 = db.Column(db.String(64))


class super_pokemon_db(db.Model):
    __tablename__ = "super_pokemon_db"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    pokemon_id = db.Column(db.Integer)
    name = db.Column(db.String(200))
    released = db.Column(db.Boolean, default=False)
    type1 = db.Column(db.String(200))
    type2 = db.Column(db.String(200))
    form = db.Column(db.String(200))
    generation = db.Column(db.Integer)
    shiny = db.Column(db.Boolean, default=False)


class base_stats_db(db.Model):
    __tablename__ = 'base_stats_db'
    id = db.Column(db.Integer, primary_key=True)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('super_pokemon_db.id'), nullable=False)
    temp_name = db.Column(db.String(255))
    base_attack = db.Column(db.Integer)
    base_defense = db.Column(db.Integer)
    base_stamina = db.Column(db.Integer)
    form = db.Column(db.String(255))


def fetch_super_pokemon_db(db):
    response_pokemon_types = requests.get("https://pogoapi.net/api/v1/pokemon_types.json")
    response_released = requests.get('https://pogoapi.net/api/v1/released_pokemon.json')
    response_names = requests.get('https://pogoapi.net/api/v1/pokemon_names.json')
    response_generations = requests.get('https://pogoapi.net/api/v1/pokemon_generations.json')
    response_shiny = requests.get('https://pogoapi.net/api/v1/shiny_pokemon.json')
    #response_alolan = requests.get('https://pogoapi.net/api/v1/alolan_pokemon.json')
    #response_galarian = requests.get('https://pogoapi.net/api/v1/galarian_pokemon.json')
    #response_hisuian = requests.get('https://pogoapi.net/api/v1/hisuian_pokemon.json')
    if (response_pokemon_types.status_code == 200 and response_released.status_code == 200
            and response_names.status_code == 200 and response_generations.status_code == 200
            and response_shiny.status_code == 200): #and response_alolan.status_code == 200
            #and response_galarian.status_code == 200): # and response_hisuian.status_code == 200):
        response_types_data = response_pokemon_types.json()
        response_released_data = response_released.json()
        response_names_data = response_names.json()
        response_generations_data = response_generations.json()
        response_shiny_data = response_shiny.json()
        #response_alolan_data = response_alolan.json()
        #response_galarian_data = response_galarian.json()
        #response_hisuian_data = response_hisuian.json()

        for pokemon_info in response_types_data:
            pokemon_types = pokemon_info['type']
            existing_record = super_pokemon_db.query.filter_by(
                id=super_pokemon_db.id,
                pokemon_id=pokemon_info['pokemon_id'],
                form=pokemon_info['form'],
                name=pokemon_info['pokemon_name']
            ).first()

            if not existing_record:
                pokemon_name = pokemon_info['pokemon_name']
                pokemon_form = pokemon_info['form']
                if (pokemon_form != 'Normal'):
                    #addition = None
                    if (pokemon_form == 'Alola'):
                        #print("Alola")
                        addition = ' (Alolan)'
                        pokemon_name = pokemon_info['pokemon_name'] + addition

                    elif (pokemon_form == 'Galarian'):
                        #print("Galarian")
                        addition = ' (Galarian)'
                        pokemon_name = pokemon_info['pokemon_name'] + addition

                    elif (pokemon_form == 'Hisuian'):
                        #print("Hisui")
                        addition = ' (Hisuian)'
                        pokemon_name = pokemon_info['pokemon_name'] + addition

                    elif (pokemon_form == 'Paldea'):
                        #print("Paldea")
                        addition = ' (Paldean)'
                        pokemon_name = pokemon_info['pokemon_name'] + addition

                new_pokemon = super_pokemon_db(
                    pokemon_id=pokemon_info['pokemon_id'],
                    form=pokemon_info['form'],
                    name=pokemon_name
                    )
                if len(pokemon_types) >= 1:
                    new_pokemon.type1 = pokemon_types[0]
                if len(pokemon_types) >= 2:
                    new_pokemon.type2 = pokemon_types[1]

                db.session.add(new_pokemon)

            db.session.commit()
        #print("Types info populated successfully")

        for pokemon, pokemon_info in response_released_data.items():
            existing_records = super_pokemon_db.query.filter_by(pokemon_id=pokemon_info['id']).all()
            for existing_record in existing_records:
                existing_record.released = True
            db.session.commit()
        #print("Released info populated successfully")

        for pokemon, pokemon_info in response_names_data.items():
            existing_records = super_pokemon_db.query.filter_by(pokemon_id=pokemon_info['id']).all()

            if not existing_records:
                new_pokemon = super_pokemon_db(
                    pokemon_id=pokemon_info['id'],
                    name=pokemon_info['name']
                )
                db.session.add(new_pokemon)
            db.session.commit()
        #print("Names info populated successfully")

        for generation, generation_pokemon in response_generations_data.items():
            for pokemon_info in generation_pokemon:
                existing_records = super_pokemon_db.query.filter_by(pokemon_id=pokemon_info['id']).all()
                for existing_record in existing_records:
                    existing_record.generation = pokemon_info['generation_number']
                db.session.commit()
        #print("Generations info populated successfully")

        for shiny, shiny_pokemon in response_shiny_data.items():
            existing_records = super_pokemon_db.query.filter_by(pokemon_id=shiny_pokemon['id']).all()
            for existing_record in existing_records:
                existing_record.shiny = True
            db.session.commit()
        #print("Shiny info populated successfully")
        #print("SUPER POKEMON TABLE POPULATED SUCCESSFULLY")

    else:
        print("Failed to fetch Pokemon data from the API1")


'''class Pokemon(db.Model):
    __tablename__ = 'Pokemon'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(200), unique=True)
    # types = db.relationship('Types_db', backref='pokemon_ref', lazy=True)
    released_pokemon = relationship("ReleasedPokemon", back_populates="pokemon")


def fetch_pokedex_db(db):  # intial function to retrieve pokemon name and id from api
    response_pokemon_names = requests.get("https://pogoapi.net/api/v1/pokemon_names.json")
    if response_pokemon_names.status_code == 200:
        pokemon_data = response_pokemon_names.json()

        # Collect existing Pokemon IDs from the database to avoid duplicates
        existing_pokemon_ids = {pokemon.id for pokemon in Pokemon.query.all()}
        new_pokemon_entries = []

        for pokemon_name, pokemon_info in pokemon_data.items():
            pokemon_id = pokemon_info['id']
            pokemon_name = pokemon_info['name']

            if pokemon_id not in existing_pokemon_ids:
                new_pokemon_entries.append({'id': pokemon_id, 'name': pokemon_name})

        if new_pokemon_entries:
            db.session.bulk_insert_mappings(Pokemon, new_pokemon_entries)
            db.session.commit()
            return "Pokemon table populated successfully"
        else:
            return "No new entries added"
    else:
        return "Failed to fetch Pokemon data from the API"
        '''

'''
class alolan_pokemon_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # pokemon_id = db.Column(db.Integer, unique=True)


def fetch_alolan(db):
    response = requests.get("https://pogoapi.net/api/v1/alolan_pokemon.json")
    if response.status_code == 200:
        response_data = response.json()
        for pokemon_id in response_data.keys():
            if pokemon_id.isdigit():
                pokemon_id = int(pokemon_id)
                if not alolan_pokemon_db.query.filter_by(id=pokemon_id).first():
                    pokemon = alolan_pokemon_db(id=pokemon_id)
                    db.session.add(pokemon)
        db.session.commit()


class baby_pokemon_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form = db.Column(db.String(100))


def fetch_baby_pokemon(db):
    response = requests.get("https://pogoapi.net/api/v1/baby_pokemon.json")
    if response.status_code == 200:
        response_data = response.json()
        for pokemon_info in response_data:  # Iterate over values since the keys are IDs
            pokemon_id = pokemon_info.get('id')
            form = pokemon_info.get('form')
            # existing_pokemon = db.session.filter_by(baby_pokemon_db, pokemon_id).first()
            if not baby_pokemon_db.query.filter_by(id=pokemon_id).first():
                pokemon = baby_pokemon_db(
                    id=pokemon_id,
                    form=form
                )
                db.session.add(pokemon)
        db.session.commit()


class badges_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class charged_moves_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class community_days_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class cp_multiplier_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class current_pokemon_moves_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class fast_moves_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class friendship_level_settings_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class galarian_pokemon_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class gobattle_league_rewards_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class gobattle_ranking_settings_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class levelup_rewards_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class mega_evolution_settings_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class mega_pokemon_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class nesting_pokemon_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class photobomb_exclusive_pokemon_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class player_xp_requirements_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class pokemon_buddy_distances_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class pokemon_candy_to_evolve_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class pokemon_encounter_data_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class pokemon_evolutions_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class pokemon_forms_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form = db.Column(db.String(255), unique=True)


# Function to populate the form data table
def fetch_form_data(db):
    response_pokemon_forms = requests.get("https://pogoapi.net/api/v1/pokemon_forms.json")
    #print("form responcse: {}".format(response_pokemon_forms.status_code))
    if response_pokemon_forms.status_code == 200:
        pokemon_forms_data = response_pokemon_forms.json()
        #print("popform: {}".format(pokemon_forms_data))
        for form_name in pokemon_forms_data:
            form1 = pokemon_forms_db(form=form_name)  # Adjust column name as per your model
            db.session.add(form1)

        db.session.commit()


class pokemon_genders_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class pokemon_generations_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class pokemon_height_weight_scale_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class pokemon_language_categories_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class pokemon_max_cp_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class pokemon_names_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class pokemon_powerup_requirements_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class pokemon_rarity_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class pokemon_stats_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class pokemon_types_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class possible_ditto_pokemon_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class pvp_charged_moves_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class pvp_exclusive_pokemon_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class pvp_fast_moves_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class raid_bosses_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class raid_exclusive_pokemon_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class raid_settings_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class research_task_exclusive_pokemon_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class shadow_pokemon_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)


def fetch_badges_db(db):
    response = requests.get('https://pogoapi.net/api/v1/badges.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = badges_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_charged_moves_db(db):
    response = requests.get('https://pogoapi.net/api/v1/charged_moves.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = charged_moves_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_community_days_db(db):
    response = requests.get('https://pogoapi.net/api/v1/community_days.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = community_days_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_cp_multiplier_db(db):
    response = requests.get('https://pogoapi.net/api/v1/cp_multiplier.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = cp_multiplier_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_current_pokemon_moves_db(db):
    response = requests.get('https://pogoapi.net/api/v1/current_pokemon_moves.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = current_pokemon_moves_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_fast_moves_db(db):
    response = requests.get('https://pogoapi.net/api/v1/fast_moves.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = fast_moves_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_friendship_level_settings_db(db):
    response = requests.get('https://pogoapi.net/api/v1/friendship_level_settings.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = friendship_level_settings_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_galarian_pokemon_db(db):
    response = requests.get('https://pogoapi.net/api/v1/galarian_pokemon.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = galarian_pokemon_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_gobattle_league_rewards_db(db):
    response = requests.get('https://pogoapi.net/api/v1/gobattle_league_rewards.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = gobattle_league_rewards_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_gobattle_ranking_settings_db(db):
    response = requests.get('https://pogoapi.net/api/v1/gobattle_ranking_settings.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = gobattle_ranking_settings_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_levelup_rewards_db(db):
    response = requests.get('https://pogoapi.net/api/v1/levelup_rewards.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = levelup_rewards_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_mega_evolution_settings_db(db):
    response = requests.get('https://pogoapi.net/api/v1/mega_evolution_settings.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = mega_evolution_settings_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_mega_pokemon_db(db):
    response = requests.get('https://pogoapi.net/api/v1/mega_pokemon.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = mega_pokemon_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_nesting_pokemon_db(db):
    response = requests.get('https://pogoapi.net/api/v1/nesting_pokemon.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = nesting_pokemon_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_photobomb_exclusive_pokemon_db(db):
    response = requests.get('https://pogoapi.net/api/v1/photobomb_exclusive_pokemon.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = photobomb_exclusive_pokemon_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_player_xp_requirements_db(db):
    response = requests.get('https://pogoapi.net/api/v1/player_xp_requirements.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = player_xp_requirements_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_pokemon_buddy_distances_db(db):
    response = requests.get('https://pogoapi.net/api/v1/pokemon_buddy_distances.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = pokemon_buddy_distances_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_pokemon_candy_to_evolve_db(db):
    response = requests.get('https://pogoapi.net/api/v1/pokemon_candy_to_evolve.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = pokemon_candy_to_evolve_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_pokemon_encounter_data_db(db):
    response = requests.get('https://pogoapi.net/api/v1/pokemon_encounter_data.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = pokemon_encounter_data_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_pokemon_evolutions_db(db):
    response = requests.get('https://pogoapi.net/api/v1/pokemon_evolutions.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = pokemon_evolutions_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_pokemon_forms_db(db):
    response = requests.get('https://pogoapi.net/api/v1/pokemon_forms.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = pokemon_forms_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_pokemon_genders_db(db):
    response = requests.get('https://pogoapi.net/api/v1/pokemon_genders.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = pokemon_genders_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()





def fetch_pokemon_height_weight_scale_db(db):
    response = requests.get('https://pogoapi.net/api/v1/pokemon_height_weight_scale.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = pokemon_height_weight_scale_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_pokemon_language_categories_db(db):
    response = requests.get('https://pogoapi.net/api/v1/pokemon_language_categories.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = pokemon_language_categories_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_pokemon_max_cp_db(db):
    response = requests.get('https://pogoapi.net/api/v1/pokemon_max_cp.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = pokemon_max_cp_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_pokemon_names_db(db):
    response = requests.get('https://pogoapi.net/api/v1/pokemon_names.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = pokemon_names_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_pokemon_powerup_requirements_db(db):
    response = requests.get('https://pogoapi.net/api/v1/pokemon_powerup_requirements.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = pokemon_powerup_requirements_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_pokemon_rarity_db(db):
    response = requests.get('https://pogoapi.net/api/v1/pokemon_rarity.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = pokemon_rarity_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_pokemon_stats_db(db):
    response = requests.get('https://pogoapi.net/api/v1/pokemon_stats.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = pokemon_stats_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_pokemon_types_db(db):
    response = requests.get('https://pogoapi.net/api/v1/pokemon_types.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = pokemon_types_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_possible_ditto_pokemon_db(db):
    response = requests.get('https://pogoapi.net/api/v1/possible_ditto_pokemon.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = possible_ditto_pokemon_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_pvp_charged_moves_db(db):
    response = requests.get('https://pogoapi.net/api/v1/pvp_charged_moves.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = pvp_charged_moves_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_pvp_exclusive_pokemon_db(db):
    response = requests.get('https://pogoapi.net/api/v1/pvp_exclusive_pokemon.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = pvp_exclusive_pokemon_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_pvp_fast_moves_db(db):
    response = requests.get('https://pogoapi.net/api/v1/pvp_fast_moves.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = pvp_fast_moves_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_raid_bosses_db(db):
    response = requests.get('https://pogoapi.net/api/v1/raid_bosses.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = raid_bosses_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_raid_exclusive_pokemon_db(db):
    response = requests.get('https://pogoapi.net/api/v1/raid_exclusive_pokemon.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = raid_exclusive_pokemon_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_raid_settings_db(db):
    response = requests.get('https://pogoapi.net/api/v1/raid_settings.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = raid_settings_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()





def fetch_research_task_exclusive_pokemon_db(db):
    response = requests.get('https://pogoapi.net/api/v1/research_task_exclusive_pokemon.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = research_task_exclusive_pokemon_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


def fetch_shadow_pokemon_db(db):
    response = requests.get('https://pogoapi.net/api/v1/shadow_pokemon.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:
            pokemon = shadow_pokemon_db(
                id=response_info['id'],
            )
            db.session.add(pokemon)
        db.session.commit()


class shiny_pokemon_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    found_egg = db.Column(db.Boolean)
    found_evolution = db.Column(db.Boolean)
    found_photobomb = db.Column(db.Boolean)
    found_raid = db.Column(db.Boolean)
    found_research = db.Column(db.Boolean)
    found_wild = db.Column(db.Boolean)
    alolan_shiny = db.Column(db.Boolean)


def fetch_shiny_pokemon_db(db):
    response = requests.get('https://pogoapi.net/api/v1/shiny_pokemon.json')
    if response.status_code == 200:
        response_data = response.json()
        for pokemon_id, pokemon_info in response_data.items():
            pokemon = db.session.get(Pokemon, pokemon_id)
            if pokemon is None:
                pokemon = Pokemon(
                    id=pokemon_id,
                    name=pokemon_info.get('name'),
                    found_egg=pokemon_info.get('found_egg', False),
                    found_evolution=pokemon_info.get('found_evolution', False),
                    found_photobomb=pokemon_info.get('found_photobomb', False),
                    found_raid=pokemon_info.get('found_raid', False),
                    found_research=pokemon_info.get('found_research', False),
                    found_wild=pokemon_info.get('found_wild', False),
                    alolan_shiny=pokemon_info.get('alolan_shiny', False)
                )
                db.session.add(pokemon)
        db.session.commit()


class time_limited_shiny_pokemon_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form = db.Column(db.String(100))


def fetch_time_limited_shiny_pokemon_db(db):
    response = requests.get('https://pogoapi.net/api/v1/time_limited_shiny_pokemon.json')
    if response.status_code == 200:
        response_data = response.json()
        for response_info in response_data:  # Iterate over values since the keys are IDs
            pokemon_id = response_info.get('id')
            form = response_info.get('form')
            if not time_limited_shiny_pokemon_db.query.filter_by(id=pokemon_id).first():
                pokemon = time_limited_shiny_pokemon_db(
                    id=pokemon_id,
                    form=form
                )
                db.session.add(pokemon)
        db.session.commit()


class type_effectiveness_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attacking_type = db.Column(db.String(100))
    defending_type = db.Column(db.String(100))
    effectiveness = db.Column(db.Integer)


def fetch_type_effectiveness_db(db):
    response = requests.get('https://pogoapi.net/api/v1/type_effectiveness.json')
    if response.status_code == 200:
        response_data = response.json()
        for attacking_type, defending_types in response_data.items():
            for defending_type, effectiveness in defending_types.items():
                existing_record = type_effectiveness_db.query.filter_by(
                    attacking_type=attacking_type,
                    defending_type=defending_type
                ).first()
                if not existing_record:
                    # Create new record
                    type_effectiveness = type_effectiveness_db(
                        attacking_type=attacking_type,
                        defending_type=defending_type,
                        effectiveness=effectiveness
                    )
                    db.session.add(type_effectiveness)
        db.session.commit()


class weather_boosts_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weather_condition = db.Column(db.String(100))
    boosted_types = db.Column(db.ARRAY(db.String))


def fetch_weather_boosts_db(db):
    response = requests.get('https://pogoapi.net/api/v1/weather_boosts.json')
    if response.status_code == 200:
        response_data = response.json()
        for weather_condition, boosted_types in response_data.items():
            weather_boost = weather_boosts_db(
                weather_condition=weather_condition,
                boosted_types=boosted_types
            )
            db.session.add(weather_boost)
        db.session.commit()
'''


def fetch_hashes(db):
    response = requests.get('https://pogoapi.net/api/v1/api_hashes.json')
    ##print("fetch hashes response.status_code = {}".format(response.status_code))
    if response.status_code == 200:
        hash_data = response.json()
        for filename in sorted(hash_data):
            data = hash_data[filename]
            #Todo: Check to see if this is where I compare endpoint vs current database/endpoint.
            existing_hash_entry = hash_data_db.query.filter_by(
                #api_filename=filename,
                full_path=data['full_path'],
                #hash_md5=data['hash_md5'],
                #hash_sha1=data['hash_sha1'],
                #hash_sha256=data['hash_sha256']
            ).all()

            if not existing_hash_entry:
                new_hash_entry = hash_data_db(
                    api_filename=filename,
                    full_path=data['full_path'],
                    hash_md5=data['hash_md5'],
                    hash_sha1=data['hash_sha1'],
                    hash_sha256=data['hash_sha256']
                )
                db.session.add(new_hash_entry)
                db.session.commit()
        ##print('Hash data fetched and stored successfully')
    else:
        return 'Failed to fetch hash data from the remote API', 500






def fetch_base_stats_db(db):
    response_pokemon_base_stats = requests.get("https://pogoapi.net/api/v1/pokemon_stats.json")
    if response_pokemon_base_stats.status_code == 200:
        pokemon_base_stats_data = response_pokemon_base_stats.json()
        for pokemon_base_stats_info in pokemon_base_stats_data:
            pokemon_name = pokemon_base_stats_info['pokemon_name']
            pokemon_id = pokemon_base_stats_info['pokemon_id']
            form = pokemon_base_stats_info['form']
            pokemon_base_attack = pokemon_base_stats_info['base_attack']
            pokemon_base_defense = pokemon_base_stats_info['base_defense']
            pokemon_base_stamina = pokemon_base_stats_info['base_stamina']
            existing_pokemon = super_pokemon_db.query.filter_by(
                id=base_stats_db.id,
                pokemon_id=pokemon_id,
                #name=pokemon_name,
                form=form
            ).first()
            if not existing_pokemon:
                new_base_stats_entry = base_stats_db(
                    form=form,
                    pokemon_id=pokemon_id,
                    temp_name=pokemon_name,
                    base_attack=pokemon_base_attack,
                    base_defense=pokemon_base_defense,
                    base_stamina=pokemon_base_stamina
                )
                db.session.add(new_base_stats_entry)
        db.session.commit()
        ##print("Base Stats table populated successfully")
    else:
        return "Failed to fetch Pokemon base stats data from the API2"


@app.route('/get_datalist_forms', methods=['POST'])
def get_datalist_forms():
    ##print("test")
    if request.method == 'POST':
        input_name = request.json.get('input_name')
        input_type1 = request.json.get('input_type1')
        input_type2 = request.json.get('input_type2')

        released_pokemon_ids = [released_pokemon.pokemon_id for released_pokemon in
                                super_pokemon_db.query.distinct(super_pokemon_db.pokemon_id).order_by(
                                    super_pokemon_db.pokemon_id).all()]
        pokemon_list = super_pokemon_db.query.filter(super_pokemon_db.id.in_(released_pokemon_ids)).order_by(
            super_pokemon_db.name).all()
        ##print(released_pokemon_ids)
        ##print(pokemon_list)

        released_pokemon_ids2 = [pokemon.pokemon_id for pokemon in
                                 super_pokemon_db.query.filter(super_pokemon_db.released).all()]
        ##print(released_pokemon_ids2)
        pokemon_names = [pokemon.name for pokemon in
                         super_pokemon_db.query.filter(super_pokemon_db.pokemon_id.in_(released_pokemon_ids))
                         .order_by(super_pokemon_db.name)
                         .all()]
        ##print(pokemon_names)

        # Pre-query released Pokémon
        released_pokemon_ids = [released_pokemon.id for released_pokemon in
                                super_pokemon_db.query.order_by(super_pokemon_db.released).all()]
        pokemon_list = super_pokemon_db.query.filter(super_pokemon_db.id.in_(released_pokemon_ids)).order_by(
            super_pokemon_db.name).all()

        ##print("1: {}, Type1: {}, Type2: {}".format(input_name, input_type1, input_type2))

        # 1/0/0
        if input_name and (not input_type1 or input_type1 == "Type 1") and (not input_type2 or input_type2 == "Type 2"):
            if input_name.isdigit():
                ##print("2-Pokemon")
                pokemon = super_pokemon_db.query.filter_by(id=int(input_name)).first()
            else:
                pokemon = super_pokemon_db.query.filter_by(name=input_name).distinct(super_pokemon_db.name).first()
                ##print("3test-Pokemon: {}".format(pokemon))

            if pokemon:
                ##print("3.5-Pokemon: {}".format(pokemon))
                serialized_no_types = {
                    'pokemons': [{'pokemon': pokemon.name}],
                }
                ##print("4-Serialized forms are: {}".format(serialized_no_types))
                return jsonify(serialized_no_types)
            else:
                ##print("5-Pokemon")
                return jsonify()

        # 0/0/0
        elif not input_name and (input_type1 == "Type 1") and (input_type2 == "Type 2"):
            pokemon = super_pokemon_db.query.with_entities(super_pokemon_db.name).distinct().order_by(super_pokemon_db.name).all()
            reset_menus = {
                'pokemon': [{'name': pokemon.name} for pokemon in pokemon],
            }
            ##print("6-Reset menu is: {}".format(reset_menus))
            return jsonify(reset_menus)

        # 0/1/1
        elif not input_name and (input_type1 and input_type1 != "Type 1") and (input_type2 and input_type2 != "Type 2"):
            ##print("Both selected: {}, Type2: {}".format(input_type1, input_type2))
            # pokemon_ids_type1 = [entry.pokemon_id for entry in Types_db.query.with_entities(Types_db.pokemon_id).filter(or_(Types_db.type1 == input_type1, Types_db.type2 == input_type1)).distinct().order_by().all()]
            # pokemon_ids_type2 = [entry.pokemon_id for entry in Types_db.query.with_entities(Types_db.pokemon_id).filter(or_(Types_db.type1 == input_type2, Types_db.type2 == input_type2)).distinct().order_by.all()]


            ##print("2: Type1: {}, Type2: {}".format(input_type1, input_type2))
            pokemon_type_ids = [entry.pokemon_id for entry in
                    super_pokemon_db.query.with_entities(super_pokemon_db.pokemon_id).filter(and_(and_(
                                        (or_(super_pokemon_db.type1 == input_type2,
                                            super_pokemon_db.type2 == input_type2)),
                                        (or_(
                                            super_pokemon_db.type1 == input_type1,
                                            super_pokemon_db.type2 == input_type1))
                                            )), super_pokemon_db.released)
                                    .distinct(super_pokemon_db.pokemon_id).order_by(super_pokemon_db.pokemon_id).all()]
            pokemon_names = [pokemon.name for pokemon in
                                 super_pokemon_db.query.filter(super_pokemon_db.pokemon_id.in_(pokemon_type_ids))
                                 .distinct(super_pokemon_db.name).order_by(super_pokemon_db.name)
                                 .all()]
            serialized_pokemon = [{'pokemon': name} for name in pokemon_names]
            ##print("Else no name & type1 & type2")
            return jsonify(serialized_pokemon)






        elif not input_name and ((input_type1 == "Type 1") or (input_type2 == "Type 2")):
            if input_type2 != "Type 2":
                ##print("2: Type1: {}, Type2: {}".format(input_type1, input_type2))
                pokemon_type_ids = [entry.pokemon_id for entry in
                                    super_pokemon_db.query.with_entities(super_pokemon_db.pokemon_id).filter((
                                        or_(super_pokemon_db.type1 == input_type2,
                                            super_pokemon_db.type2 == input_type2)), super_pokemon_db.released)
                                    .distinct(super_pokemon_db.pokemon_id).order_by(super_pokemon_db.pokemon_id).all()]
                pokemon_names = [pokemon.name for pokemon in
                                 super_pokemon_db.query.filter(super_pokemon_db.pokemon_id.in_(pokemon_type_ids))
                                 .distinct(super_pokemon_db.name).order_by(super_pokemon_db.name)
                                 .all()]
                serialized_pokemon = [{'pokemon': name} for name in pokemon_names]
                return jsonify(serialized_pokemon)

            elif input_type1 != "Type 1":
                ##print("3: Type1: {}, Type2: {}".format(input_type1, input_type2))
                pokemon_type_ids = [entry.pokemon_id for entry in
                                    super_pokemon_db.query.with_entities(super_pokemon_db.pokemon_id).filter((
                                        or_(super_pokemon_db.type1 == input_type1,
                                            super_pokemon_db.type2 == input_type1)), super_pokemon_db.released)
                                    .distinct(super_pokemon_db.pokemon_id).order_by(super_pokemon_db.pokemon_id).all()]
                ##print("Type1: {}".format(pokemon_type_ids))
                #released_pokemons = [pokemon.pokemon_id for pokemon in
                #                     super_pokemon_db.query.filter(super_pokemon_db.pokemon_id.in_(pokemon_type_ids),
                #                                               super_pokemon_db.released is True).all()]
                ###print("Type2: {}".format(released_pokemons))
                pokemon_names = [pokemon.name for pokemon in
                                 super_pokemon_db.query.filter(super_pokemon_db.pokemon_id.in_(pokemon_type_ids))
                                 .distinct(super_pokemon_db.name).order_by(super_pokemon_db.name)
                                 .all()]
                ##print("Type3: {}".format(pokemon_names))

                serialized_pokemon = [{'pokemon': name} for name in pokemon_names]
                ###print(serialized_pokemon)
                return jsonify(serialized_pokemon)
            else:
                ##print("Else no name & type1 or type2")
                return ""


        else:
            ##print("8-Pokemon")
            # return jsonify([])
            return ''
    return render_template('Pokemon_Details.html')


@app.route('/get_types', methods=['POST'])
def get_types():
    if request.method == 'POST':
        input_type1 = request.json.get('input_type1')
        input_type2 = request.json.get('input_type2')
        ##print("1: Type1: {}, Type2: {}".format(input_type1, input_type2))

        if (input_type1 == "Type 1") or (input_type2 == "Type 2"):
            if input_type2 != "Type 2":
                ##print("2: Type1: {}, Type2: {}".format(input_type1, input_type2))


                pokemon_ids = [entry.pokemon_id for entry in
                               super_pokemon_db.query.distinct(super_pokemon_db.pokemon_id).order_by(
                                   super_pokemon_db.pokemon_id).filter(
                                   or_(super_pokemon_db.type1 == input_type2, super_pokemon_db.type2 == input_type2))]
                ##print("test1: {}".format(pokemon_ids))

                pokemon_names = [entry2.name for entry2 in
                                 super_pokemon_db.query.distinct(super_pokemon_db.name).order_by(super_pokemon_db.name).filter(
                                     super_pokemon_db.id.in_(pokemon_ids))]
                ##print("test2: {}".format(pokemon_names))

                serialized_pokemon = {'pokemons': [{'pokemon': name} for name in pokemon_names]}
                ##print("test3: {}".format(serialized_pokemon))

            elif input_type1 != "Type 1":
                ##print("3: Type1: {}, Type2: {}".format(input_type1, input_type2))

                pokemon_ids = [entry.pokemon_id for entry in
                               super_pokemon_db.query.distinct(super_pokemon_db.pokemon_id).order_by(
                                   super_pokemon_db.pokemon_id).filter(
                                   or_(super_pokemon_db.type1 == input_type1, super_pokemon_db.type2 == input_type1))]
                ##print("test4: {}".format(pokemon_ids))

                pokemon_names = [entry2.name for entry2 in
                                 super_pokemon_db.query.distinct(super_pokemon_db.name).order_by(super_pokemon_db.name).filter(
                                     super_pokemon_db.id.in_(pokemon_ids))]
                ##print("test5: {}".format(pokemon_names))

                serialized_pokemon = {'pokemons': [{'pokemon': name} for name in pokemon_names]}
                ##print("test6: {}".format(serialized_pokemon))

                return jsonify(serialized_pokemon)
            else:
                ##print("Else type1 type2")
                return ""

        else:
            ##print("4: Type1: {}, Type2: {}".format(input_type1, input_type2))
            pokemon_type1 = super_pokemon_db.query.filter_by(id=input_type1).first()
            pokemon_type2 = super_pokemon_db.query.filter_by(id=input_type2).first()
            pokemon_with_types12 = (pokemon_type1, pokemon_type2)
            return jsonify(pokemon_with_types12)


@app.route('/get_pokemon', methods=['GET', 'POST'])
def get_pokemon():
    if request.method == 'POST':
        #input_name = request.form.get('input_name')
        input_name = request.form.get('input_name') or request.form.get('input_name_prev')
        original_input_type1 = request.form.get('input_type1')
        original_input_type2 = request.form.get('input_type2')
        ##print("input_name {}".format(input_name))
        ##print("input_type2 {}".format(original_input_type2))
        pokemon = None
        if input_name == "" or input_name is None:
            pokemon_id = super_pokemon_db.query.order_by(super_pokemon_db.pokemon_id).all()
            pokemon_list = super_pokemon_db.query.order_by(super_pokemon_db.name).all()
            pokemon_form_list = super_pokemon_db.query.with_entities(super_pokemon_db.form).distinct().order_by(
                super_pokemon_db.form).all()
            return render_template('PokeMainPage.html',
                                   pokemon_id=pokemon_id,
                                   pokemon_list=pokemon_list,
                                   pokemon_form_list=pokemon_form_list
                                   )
        if input_name:
            if input_name.isdigit():
                ##print("test")

                new_pokemon = super_pokemon_db.query.filter_by(pokemon_id=int(input_name)).all()
                ##print("pokemons: {}".format(new_pokemon))
                new_name = new_pokemon[0].name
                ##print("new_name: {}".format(new_name))

                pokemons = [p for p in new_pokemon if p.form == "Normal" and p.pokemon_id == int(input_name)]
                input_type1 = new_pokemon[0].type1
                ##print("1<10: {}".format(pokemons))
                # new_name = pokemons[0].name
            else:
                new_pokemon = super_pokemon_db.query.filter_by(name=input_name).first()
                ##print(new_pokemon)
                #TODO: this is where I left off 10:20pm wednesday night

                if not new_pokemon:
                    return "Pokemon with name {} not found.".format(input_name)
                ##print("Pokemon new_name: {}".format(new_pokemon.name))
                new_name = new_pokemon.name
                ##print("new_name: {}".format(new_name))
                input_type1 = new_pokemon.type1
                ##print("input_type1: {}   input_type2: {}".format(input_type1, original_input_type2))





            #if original_input_type2 is None:
            #    input_type2 = None
            #    subquery = (db.session.query(func.max(super_pokemon_db.id))
            #                    .filter(and_(super_pokemon_db.name == new_name,
            #                                 (or_(super_pokemon_db.type1 == input_type1, super_pokemon_db.type2 == input_type1))))
            #                    .group_by(super_pokemon_db.form).subquery())
            #    ##print("Type 2 is null or not provided")
            #else:
            #    input_type2 = new_pokemon.type2
            #    ##print("Type 2:{}".format(original_input_type2))

            #    subquery = (db.session.query(func.max(super_pokemon_db.id)).filter(and_(super_pokemon_db.name == new_name,
            #                                                                            (or_(or_(or_(super_pokemon_db.type1 == input_type1, super_pokemon_db.type2 == input_type1),
            #                                                                                     (or_(super_pokemon_db.type1 == input_type2, super_pokemon_db.type2 == input_type2))))))
            #                                                                       ).group_by(super_pokemon_db.form).subquery())

            #if (((original_input_type1 != input_type1)
            #            and (original_input_type1 != input_type2))
            #                or ((original_input_type2 != input_type1) and (original_input_type2 != input_type2))):
            #    return "No match for this combination."




            ###print("Subquery: {}".format(subquery))
            pokemon_id = super_pokemon_db.query.filter_by(name=new_name,form='Normal',released=True).order_by(super_pokemon_db.pokemon_id).distinct().first()
            if not pokemon_id:
                ##print("not pokemon_id")
                pokemon_id = super_pokemon_db.query.filter_by(name=new_name,released=True).order_by(super_pokemon_db.id.asc()).distinct().first()

            pokemon = pokemon_id
            #pokemon = super_pokemon_db.query.filter_by(id=pokemon_id).first()
            ##print("pokemon: {}".format(pokemon))
            if not pokemon:
                return "Pokemon not found: {}".format(pokemon)

            ##print("pokemon2: {}".format(pokemon))
            base_stats = base_stats_db.query.filter_by(id=pokemon.id).first()
            ##print("base stats: {}".format(base_stats)) 
            #base_stats = base_stats_db.query.filter_by(pokemon_id=pokemon.id).first()


            highest_atk = base_stats_db.query.filter_by(id=base_stats_db.id).order_by(desc(base_stats_db.base_attack)).first()
            ###print("highest_atk: {}".format(highest_atk))
            lowest_atk = base_stats_db.query.filter_by(id=base_stats_db.id).order_by(asc(base_stats_db.base_attack)).first()
            highest_def = base_stats_db.query.filter_by(id=base_stats_db.id).order_by(desc(base_stats_db.base_defense)).first()
            lowest_def = base_stats_db.query.filter_by(id=base_stats_db.id).order_by(asc(base_stats_db.base_defense)).first()
            highest_sta = base_stats_db.query.filter_by(id=base_stats_db.id).order_by(desc(base_stats_db.base_stamina)).first()
            lowest_sta = base_stats_db.query.filter_by(id=base_stats_db.id).order_by(asc(base_stats_db.base_stamina)).first()
            atk_perc = (base_stats.base_attack)/(highest_atk.base_attack)*100
            def_perc = (base_stats.base_defense)/(highest_def.base_defense)*100
            sta_perc = (base_stats.base_stamina)/(highest_sta.base_stamina)*100
            ##print("base stats: {}".format(base_stats))
            ##print("atk perc: {}".format(atk_perc))
            atk_color = None
            def_color = None
            sta_color = None
            if 0 <= atk_perc < 10:
                atk_color = "percent_color_1"
            elif 10 <= atk_perc < 20:
                atk_color = "percent_color_2"
            elif 20 <= atk_perc < 35:
                atk_color = "percent_color_3"
            elif 35 <= atk_perc < 50:
                atk_color = "percent_color_4"
            elif 50 <= atk_perc < 75:
                atk_color = "percent_color_5"
            elif 75 <= atk_perc <= 100:
                atk_color = "percent_color_6"

            if 0 <= def_perc < 10:
                def_color = "percent_color_1"
            elif 10 <= def_perc < 20:
                def_color = "percent_color_2"
            elif 20 <= def_perc < 35:
                def_color = "percent_color_3"
            elif 35 <= def_perc < 50:
                def_color = "percent_color_4"
            elif 50 <= def_perc < 75:
                def_color = "percent_color_5"
            elif 75 <= def_perc <= 100:
                def_color = "percent_color_6"

            if 0 <= sta_perc < 10:
                sta_color = "percent_color_1"
            elif 10 <= sta_perc < 20:
                sta_color = "percent_color_2"
            elif 20 <= sta_perc < 35:
                sta_color = "percent_color_3"
            elif 35 <= sta_perc < 50:
                sta_color = "percent_color_4"
            elif 50 <= sta_perc < 75:
                sta_color = "percent_color_5"
            elif 75 <= sta_perc <= 100:
                sta_color = "percent_color_6"

            CPM40 = 0.790300011634826
            CPM50 = 0.840300023555755
            #Max_CP40 = (((base_stats.base_attack + 15) * ((base_stats.base_defense + 15) ** 0.5) * ((base_stats.base_stamina + 15) ** 0.5) * ((7903001 / 10) ** 2)) / 10)
            Max_CP40 = ((base_stats.base_attack + 15) * ((base_stats.base_defense + 15) ** 0.5) * ((base_stats.base_stamina + 15) ** 0.5) * (0.7903001 ** 2))
            Max_CP50 = max(10, int(((base_stats.base_attack + 15) / 10) ** 0.5 * ((base_stats.base_defense + 15) / 10) ** 0.5 * ((base_stats.base_stamina + 15) / 10) ** 0.5 * 0.667934002 ** 2))
            #Max_CP50 = ((base_stats.base_attack + 15) * ((base_stats.base_defense + 15) ** 0.5) * ((base_stats.base_stamina + 15) ** 0.5) * (0.667934002 ** 2))
            Max_CP40 = round(((base_stats.base_attack + 15) * math.sqrt(base_stats.base_defense + 15) * math.sqrt(base_stats.base_stamina + 15) * (CPM40 ** 2)) / 10)
            Max_CP50 = round(((base_stats.base_attack + 15) * math.sqrt(base_stats.base_defense + 15) * math.sqrt(base_stats.base_stamina + 15) * (CPM50 ** 2)) / 10)
            #Max_CP50 = ((base_stats.base_attack + 15) * math.sqrt(base_stats.base_defense + 15) * math.sqrt(base_stats.base_stamina + 15) * (0.667934002 ** 2))
            #Max_CP50 = 0
            ##print("Max_CP40: {}".format(Max_CP40))
            ##print("Max_CP50: {}".format(Max_CP50))
            #if not types:
            #    return "No data found for this Pokemon form"

            return render_template('Pokemon_Details.html',
                                           pokemon=pokemon,
                                           types=pokemon,
                                           base_stats=base_stats,
                                           highest_atk=highest_atk,
                                           lowest_atk=lowest_atk,
                                           highest_def=highest_def,
                                           lowest_def=lowest_def,
                                           highest_sta=highest_sta,
                                           lowest_sta=lowest_sta,
                                           atk_perc=atk_perc,
                                           def_perc=def_perc,
                                           sta_perc=sta_perc,
                                           atk_color=atk_color,
                                           def_color=def_color,
                                           sta_color=sta_color,
                                           Max_CP40=Max_CP40,
                                           Max_CP50=Max_CP50
                                           )

        return render_template('Pokemon_Details.html')


@app.route('/get_dec_inc', methods=['GET', 'POST'])
def get_dec_inc():
    if request.method == 'GET':
        if request.method == 'GET':
            input_type1 = request.args.get('type1')
            input_type2 = request.args.get('type2')
            pk_id = request.args.get('id')


            if 'prev' in request.args or 'next' in request.args:
                # Determine which button was clicked and get the corresponding ID
                if 'prev' in request.args:
                    new_id = int(request.args.get('prev_id'))
                    button_clicked = 'Previous'

                else:
                    new_id = int(request.args.get('next_id'))
                    button_clicked = 'Next'

                ##print("GET: {}".format(new_id))
                if 1 <= new_id <= 1010:
                    new_pokemon = super_pokemon_db.query.filter_by(pokemon_id=int(new_id)).all()
                    ##print("pokemons: {}".format(new_pokemon))
                    new_name = new_pokemon[0].name #super_pokemon_db.query.filter_by(name=new_id.name).all()
                    ##print("new_name: {}".format(new_name))

                    pokemon = [p for p in new_pokemon if p.form == "Normal" or p.pokemon_id == int(new_id)]
                    new_type1 = new_pokemon[0].type1
                    ##print("1<10: {}".format(pokemon))
                    if input_type2 is None:
                        subquery = (db.session.query(func.max(super_pokemon_db.id))
                                    .filter(and_(super_pokemon_db.name == new_name,
                                                 (or_(super_pokemon_db.type1 == new_type1, super_pokemon_db.type2 == new_type1))))
                                                  .group_by(super_pokemon_db.form).subquery())
                        #print("Type 2 is null or not provided")
                    else:
                        new_type2 = new_pokemon[0].type2
                        #print("Type 2:{}".format(input_type2))

                        subquery = (db.session.query(func.max(super_pokemon_db.id)).filter(and_(super_pokemon_db.name == new_name,
                                                                                        (or_(or_(or_(super_pokemon_db.type1 == new_type1, super_pokemon_db.type2 == new_type1),
                                                                                                 (or_(super_pokemon_db.type1 == new_type2, super_pokemon_db.type2 == new_type2))))))
                                                                                   ).group_by(super_pokemon_db.form).subquery())

                    #print("Subquery: {}".format(subquery))
                    pokemon_id = db.session.query(super_pokemon_db.id).filter(
                        super_pokemon_db.id.in_(subquery)).order_by(super_pokemon_db.id.desc()).first()
                    #print("pokemon_id: {}".format(pokemon_id))
                    if not pokemon_id:
                        return "Pokemon not found"

                    # Retrieve the full details of the Pokemon using the found ID
                    pokemon = super_pokemon_db.query.filter_by(id=pokemon_id[0]).first()
                    #print("pokemon1: {}".format(pokemon))
                    # Retrieve types associated with the found Pokemon based on the form
                    types = super_pokemon_db.query.filter_by(id=pokemon.id).first()
                    #print("types: {}".format(types))
                    #print("pokemon2: {}".format(pokemon))
                    base_stats = base_stats_db.query.filter_by(id=pokemon.id).first()
                    #print("base stats: {}".format(base_stats))

                    if not types:
                        return "No data found for this Pokemon form"

                    return render_template('Pokemon_Details.html',
                                           pokemon=pokemon,
                                           types=types,
                                           base_stats=base_stats
                                           )


                else:
                    input_type1 = request.args.get('type1')
                    input_type2 = request.args.get('type2')

                    pokemon = super_pokemon_db.query.filter_by(id=int(pk_id)).first()
                    types = super_pokemon_db.query.filter_by(id=pokemon.id).first()
                    base_stats = base_stats_db.query.filter_by(id=pokemon.id).first()
                    return render_template('Pokemon_Details.html', pokemon=pokemon, types=types, base_stats=base_stats)






            #subquery = db.session.query(func.max(super_pokemon_db.id)).filter(
            #super_pokemon_db.name == input_name, super_pokemon_db.form == 'Normal').group_by(super_pokemon_db.form).subquery()

            # Get the Pokemon with the highest ID for the 'Normal' form


    return render_template('Pokemon_Details.html')

@app.route('/ajax_search', methods=['POST'])
def ajax_search():
    query = request.form.get('query')

    #print("query: {}".format(query))
    if query:
        pokemons = super_pokemon_db.query.with_entities(super_pokemon_db.released,super_pokemon_db.name).filter(super_pokemon_db.name.ilike('%{}%'.format(query))).distinct().all()
        pokemon_names = []
        # pokemon_names = [{'name': pokemon.name} for pokemon in pokemons]
        for pokemon in pokemons:
        #for pokemon_multiple in pokemons:
            #pokemon = pokemon_multiple.query.filter(super_pokemon_db.name).distinct().all()
            if pokemon.released:
                #if pokemon.form == "Normal":
                pokemon_names.append({'name': pokemon.name})
                #print("______________________")
                #print("{}".format(pokemon.name))

                #else:
                    #temp_pokemon = ({'name': pokemon.name, ' (': pokemon.form})
                    ##print(temp_pokemon)
                    #pokemon_names.append(temp_pokemon)
                    #pokemon_names.append({'name': '{} ({})'.format(pokemon.name, pokemon.form)})
                    ##print("______________________")
                    ##print("Not name: {}".format(pokemon.name))
                    ##print("Not form: {}".format(pokemon.form))
                    ##print("Not P_Names: {}".format(pokemon_names))

        return jsonify(pokemon_names)

    else:
        #print("else")
        pokemons = super_pokemon_db.query.with_entities(super_pokemon_db.released, super_pokemon_db.name).order_by(super_pokemon_db.name).distinct().all()
        pokemon_names = []
        for pokemon in pokemons:
            #for pokemon_multiple in pokemons:
            #pokemon = pokemon_multiple.query.filter(super_pokemon_db.name).distinct().all()
            if pokemon.released:
                #if pokemon.form == "Normal":
                pokemon_names.append({'name': pokemon.name})
                ##print("______________________")
                #print("{}".format(pokemon.name))
        return jsonify(pokemon_names)


        #pokemon_id = super_pokemon_db.query.order_by(super_pokemon_db.name).all()
        #pokemon_list = super_pokemon_db.query.order_by(super_pokemon_db.name).all()
        #return render_template('PokeMainPage.html',
        #                   pokemon_id=pokemon_id,
        #                   pokemon_list=pokemon_list,
        #                   )


# TODO: Finish the periodic table updating function later, check the class lectures for guidance
'''
def check_table_empty(table_name):
    #table_name = base_stats_db
    #print("temp")
    count = db.session.query(func.count()).select_from(table_name).scalar()
    #print("CountTables: {}".format(count))
    return count == 0

def check_table_exists(table_name):
    inspector = inspect(db.engine)
    ##print("Inspector: {}".format(inspector))
    ##print("Inspected: {}".format(inspector.get_table_names()))
    #print("__tablename__: {}".format(table_name))
    if table_name.__tablename__ in inspector.get_table_names():

        #print("Table '{}' exists".format(table_name.__tablename__))
        if not check_table_empty(table_name):
            #print("Table '{}' is populated.".format(table_name.__tablename__))
            return 1
        else:
            #print("Table '{}' exists but is empty.".format(table_name.__tablename__))
            return 2
    else:
        #print("Table Name: {} does not exist.".format(table_name.__tablename__))
        return 0

'''

def download_png(url, filename, id_num):

    ##print("{}   {}".format(url, filename))
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        ##print("Downloaded {} successfully.".format(filename))
    #else:
        #print("{}  {}  {}".format(id_num, filename, url))




@app.route('/')
def index():
    pokemon_count = super_pokemon_db.query.count()
    #print("Count: {}".format(pokemon_count))

    #fetch_hashes(db)
    #fetch_super_pokemon_db(db)
    #fetch_base_stats_db(db)


    '''
    pre_url = ""
    for i in range(1,10):
        folder_name = "fromWeb_specials/normal/generation_{}".format(i)  # Naming the folder based on the iteration value
        folder_name_shiny = "fromWeb_specials/shiny/generation_{}".format(i)
        os.makedirs(folder_name, exist_ok=True)  # Create folder if it doesn't exist
        os.makedirs(folder_name_shiny, exist_ok=True)  # Create folder if it doesn't exist
        pokemon_list = super_pokemon_db.query.filter_by(generation=i).order_by(super_pokemon_db.pokemon_id).all()
        url = ""
        surl = ""

        for pokemon_var in pokemon_list:
            pokemon_name = pokemon_var.name.lower()  # Assuming the name is stored in lowercase
            pokemon_form = pokemon_var.form

            if pokemon_form == "Alola":
                pre_url = "https://img.pokemondb.net/sprites/sun-moon"
                url = pre_url + "/normal/" + pokemon_name + "-alolan.png"
                surl = pre_url + "/shiny/" + pokemon_name + "-alolan.png"
            elif pokemon_form == "Galarian":
                pre_url = "https://img.pokemondb.net/sprites/sword-shield"
                url = pre_url + "/normal/" + pokemon_name + "-galarian.png"
                surl = pre_url + "/shiny/" + pokemon_name + "-galarian.png"
            

            #elif pokemon_var.form == "Normal":
                #######if 1 <= i <= 6:
                    #######pre_url = "https://img.pokemondb.net/sprites/x-y"
                #elif i == 2:
                #    pre_url = "https://img.pokemondb.net/sprites/x-y"
                #elif i == 3:
                #    pre_url = "https://img.pokemondb.net/sprites/ruby-sapphire"
                #elif i == 4:
                #    pre_url = "https://img.pokemondb.net/sprites/diamond-pearl"
                #elif i == 5:
                #    pre_url = "https://img.pokemondb.net/sprites/black-white"
                #elif i == 6:
                #    pre_url = "https://img.pokemondb.net/sprites/x-y"
                #########elif 6 < i <= 9:
                    ##########pre_url = "https://img.pokemondb.net/sprites/go"
                #elif i == 8:
                #    pre_url = "https://img.pokemondb.net/sprites/go"
                #elif i == 9:
                #    pre_url = "https://img.pokemondb.net/sprites/go"
                #####else:
                    #########rint("BAD")

            else:
                #print("BAD2")
                pre_url = "https://img.pokemondb.net/sprites/x-y"
                url = pre_url + "/normal/" + pokemon_name + ".png"
                surl = pre_url + "/shiny/" + pokemon_name + ".png"


            #url = pre_url + "/normal/" + pokemon_name + ".png"
            ##print(url)
            pokemon_id_file = pokemon_var.pokemon_id
            filename = str(pokemon_id_file) + ".png"
            file_path = os.path.join(folder_name, filename)
            download_png(url, file_path, pokemon_id_file)



            #spokemon_name = pokemon_var.name.lower()  # Assuming the name is stored in lowercase
            #spokemon_id_file = pokemon_var.pokemon_id
            #url = "https://img.pokemondb.net/sprites/x-y/shiny/" + pokemon_name + ".png"
            #url = pre_url + "/shiny/" + pokemon_name + ".png"
            ##print(url)
            filename = str(pokemon_id_file) + "s.png"
            file_path = os.path.join(folder_name_shiny, filename)
            download_png(surl, file_path, pokemon_id_file)


    '''
    '''
    table_name = None
    for i in range(3):
        if i == 0:
            table_name = hash_data_db
        elif i == 1:
            table_name = super_pokemon_db
        elif i == 2:
            table_name = base_stats_db
        #print("Table Name: {}".format(table_name))
        result = check_table_exists(table_name)
        #print("Result: {}".format(result))
        if result == 1:
            #print("Table '{}' exists and is populated.".format(table_name))
        elif result == 2:
            #print("Table '{}' exists but is empty.".format(table_name))


        else:
            return "Table '{}' does not exist.".format(table_name)
    '''

    # fetch_raid_settings_db(db)
    # fetch_released_pokemon_db(db)
    # fetch_research_task_exclusive_pokemon_db(db)
    # fetch_shadow_pokemon_db(db)

    if pokemon_count == 10142:
        # fetch_pokemon(db)
        '''
        fetch_badges_db(db)
        fetch_charged_moves_db(db)
        fetch_community_days_db(db)
        fetch_cp_multiplier_db(db)
        fetch_current_pokemon_moves_db(db)
        fetch_fast_moves_db(db)
        fetch_friendship_level_settings_db(db)
        fetch_galarian_pokemon_db(db)
        fetch_gobattle_league_rewards_db(db)
        fetch_gobattle_ranking_settings_db(db)
        fetch_levelup_rewards_db(db)
        fetch_mega_evolution_settings_db(db)
        fetch_mega_pokemon_db(db)
        fetch_nesting_pokemon_db(db)
        fetch_photobomb_exclusive_pokemon_db(db)
        fetch_player_xp_requirements_db(db)
        fetch_pokemon_buddy_distances_db(db)
        fetch_pokemon_candy_to_evolve_db(db)
        fetch_pokemon_encounter_data_db(db)
        fetch_pokemon_evolutions_db(db)
        fetch_pokemon_forms_db(db)
        fetch_pokemon_genders_db(db)
        fetch_pokemon_generations_db(db)
        fetch_pokemon_height_weight_scale_db(db)
        fetch_pokemon_language_categories_db(db)
        fetch_pokemon_max_cp_db(db)
        fetch_pokemon_names_db(db)
        fetch_pokemon_powerup_requirements_db(db)
        fetch_pokemon_rarity_db(db)
        fetch_pokemon_stats_db(db)
        fetch_pokemon_types_db(db)
        fetch_possible_ditto_pokemon_db(db)
        fetch_pvp_charged_moves_db(db)
        fetch_pvp_exclusive_pokemon_db(db)
        fetch_pvp_fast_moves_db(db)
        fetch_raid_bosses_db(db)
        fetch_raid_exclusive_pokemon_db(db)

        fetch_raid_settings_db(db)
        fetch_released_pokemon(db)
        fetch_research_task_exclusive_pokemon_db(db)
        fetch_shadow_pokemon_db(db)

        fetch_shiny_pokemon_db(db)
        fetch_time_limited_shiny_pokemon_db(db)
        fetch_type_effectiveness_db(db)
        fetch_weather_boosts_db(db)

    # TODO: update this block if statement or move/remove it to the endpoint comparitors
    if pokemon_count != 1010:
        fetch_hashes(db)
        fetch_pokedex_db(db)
        # fetch_evolutions_db(db)
        fetch_types_db(db)
        fetch_base_stats_db(db)
        fetch_form_data(db)
        fetch_alolan(db)
'''
        #print("indexed")

    pokemon_ids = [pokemon.id for pokemon in super_pokemon_db.query.order_by(super_pokemon_db.id).all()]

    # Retrieve all released Pokemon IDs
    released_pokemon_ids = [released_pokemon.id for released_pokemon in
                            super_pokemon_db.query.order_by(super_pokemon_db.released).all()]

    # Filter Pokemon list to include only released Pokemon
    # pokemon_list = [pokemon for pokemon in pokemon_ids if pokemon in released_pokemon_ids]
    pokemon_list = super_pokemon_db.query.filter(super_pokemon_db.id.in_(released_pokemon_ids)).order_by(
        super_pokemon_db.name).all()


    #print("release_pokemon: {}".format(pokemon_list))
    # Fetch distinct Pokemon forms
    pokemon_form_list = super_pokemon_db.query.with_entities(super_pokemon_db.form).distinct().order_by(super_pokemon_db.form).all()

    return render_template('PokeMainPage.html',
                           released_pokemon_id=released_pokemon_ids,
                           pokemon_list=pokemon_list,
                           pokemon_form_list=pokemon_form_list
                           )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    #app.run()
    app.run(debug=True)
    #app.run(host="0.0.0.0", port=8000, debug=True)
