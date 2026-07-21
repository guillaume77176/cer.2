# -*- coding: utf-8 -*-
# Copyright 2024-2025 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import pandas as pd
import os
import s3fs
from datetime import datetime
from zoneinfo import ZoneInfo
import time



t1 = "Q8MRM0DQYIOI05OIBAO5"
t2 = "MMjEfjh0UPj50VHnzAAMkkrul9VG6YEG4WAs48Bi"
t3 = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJROE1STTBEUVlJT0kwNU9JQkFPNSIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sImF1ZCI6WyJtaW5pby1kYXRhbm9kZSIsIm9ueXhpYSIsImFjY291bnQiXSwiYXV0aF90aW1lIjoxNzg0NDEzMjgzLCJhenAiOiJvbnl4aWEiLCJjbmYiOnsiamt0IjoiYjFoengtSjRKOUxJbjRuLTJ0WFlWUGxFeUZtWEFZTkdndEZIRHZMaDNLNCJ9LCJlbWFpbCI6Imd1aWxsYXVtZS5yb3VzdGFuQGVuc2FlLmZyIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImV4cCI6MTc4NTAxODA4OCwiZmFtaWx5X25hbWUiOiJSb3VzdGFuIiwiZ2l2ZW5fbmFtZSI6Ikd1aWxsYXVtZSIsImdyb3VwcyI6WyJVU0VSX09OWVhJQSJdLCJpYXQiOjE3ODQ0MTMyODgsImlzcyI6Imh0dHBzOi8vYXV0aC5sYWIuc3NwY2xvdWQuZnIvYXV0aC9yZWFsbXMvc3NwY2xvdWQiLCJqdGkiOiJvbnJ0cnQ6ZTM2MTBkNDktMDhiOC0yNGZjLTNlZTUtZmQxMzE0YmMzYTg1IiwibG9jYWxlIjoiZnIiLCJuYW1lIjoiR3VpbGxhdW1lIFJvdXN0YW4iLCJwb2xpY3kiOiJzdHNvbmx5IiwicHJlZmVycmVkX3VzZXJuYW1lIjoiZ3VpbGxhdW1lMTc2IiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLXNzcGNsb3VkIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtc3NwY2xvdWQiXSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBncm91cHMgZW1haWwiLCJzaWQiOiJpWUVRcEFSeDVISDVnN0tIcktuWm5VSzYiLCJzdWIiOiI5Mjc4NzJjYi03NjgyLTRkNDAtYjliNy04M2IyYjk3YWRmMjgiLCJ0eXAiOiJEUG9QIn0.XDvECBTiNqnLFN1TjUjrxupmqc1CsXdJw1Ay9OkCOImmBgeOxn1PyGRnEzYujcZjHpzzkiJoG_5uyddRJ0nu-g"

st.set_page_config(
    page_title="Alexmex MoneyMaker - L'app de gestion financière du quotidien de Alex",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

"""
# :material/query_stats: Alexmex MoneyMaker - L'app de gestion financière du quotidien de Alex | 
"""

""  

st.text("Ajoute chaque dépense de manière simple, consulte tes dépenses en cours du mois, planifie tes dépenses à l'avance et reste dans tes comptes, et bien plus !")
cols = st.columns([1, 3])

#####################################################################
##########    Tableau principal des dépenses en cours    ############
#####################################################################

#Import des données
saved_table = pd.read_csv("https://minio.lab.sspcloud.fr/guillaume176/alex/tabledep.csv")
entry = pd.read_csv("https://minio.lab.sspcloud.fr/guillaume176/alex/entry.csv")
message = pd.read_csv("https://minio.lab.sspcloud.fr/guillaume176/alex/message.csv")

#Gestion de la date
date = datetime.now(ZoneInfo("Europe/Paris"))
date_fr = date.strftime("%d/%m/%Y %H:%M")
st.write(f"Date et Heure :  {date_fr} | Message du jour : '{message.iloc[-1]["Message"]}'")

# Ajout des dépenses fixes le 1er du mois et remise à zéro
day = date_fr[0:2]
last_day = saved_table.iloc[-1]["Date/Heure"][8:10]
ref = saved_table.iloc[-1]["ref"]

if day == "01" and last_day !=  "01":
    new_ref = ref + 1
    fixe = {
        "Date/Heure" : [date_fr for i in range(10)],
        "Montant" : [1150.00, 118.00, 245.86, 36.98, 100.77, 18.45, 7.99, 2.75, 2.99, 11.99],
        "Categorie": (["Loyer", "Electricité", "Crédit auto", "Internet",
         "Assurance voiture (ty)", "Garantie voiture", 
         "Netflix", "Maif-vie","Collier-chat", "Téléphone (ty)"]),
         "ref" : [new_ref for i in range(10)]
        }
    fixe_df = pd.DataFrame(fixe)
    saved_table = pd.concat([saved_table, fixe_df], ignore_index=True)

#Variables pour métriques
rev = entry["Montant"].sum()
solde = rev - saved_table['Montant'].sum()
economies = 0


#Metriques mensuels
st.text("RECAPITULATIF MENSUEL  : ")
c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("🛒 Transactions enregistrées (mois)", len(saved_table)-1)
c2.metric("🔁 Total en cours (mois)", f"{saved_table['Montant'].sum():.2f} €")
c3.metric("⚖️ Solde compte Alex", f"{solde:.2f} €", delta=solde)
c4.metric("🤔 Economies réalisées / mois dernier ?", f"{economies}", delta = economies)
c5.metric("💰 Revenu totaux (mois)", f"{rev:.2f} €")

st.divider()

# Ajouter une dépense
st.subheader("➕ Ajouter une dépense")

choix = st.selectbox(
    "Catégorie",
    ["Courses", "Restaurant", "Transport", "Autre facture", "Loisirs", "Autre..."]
)

if choix == "Autre...":
    categorie = st.text_input(
        "Tapez le nom de votre dépense",
        max_chars=100
    )
elif choix == "Loisirs":
    categorie = st.text_input(
        "Précisez la nature du loisir",
        max_chars=100
    )
else:
    categorie = choix


with st.form("form_depense"):
    col1, col2 = st.columns(2)

    with col1:
        montant = st.number_input(
            "💶 Montant",
            min_value=0.0,
            step=0.01,
            format="%.2f"
        )

    ajouter_depense = st.form_submit_button("Ajouter la dépense")

if ajouter_depense:
    nouvelle_depense = pd.DataFrame([{
        "Date/Heure": datetime.now(ZoneInfo("Europe/Paris")).strftime("%d/%m/%Y %H:%M"),
        "Montant": montant,
        "Catégorie": categorie,
        "ref" : ref
    }])

    saved_table = pd.concat(
        [saved_table, nouvelle_depense],
        ignore_index=True
    )


    os.environ["AWS_ACCESS_KEY_ID"] = t1
    os.environ["AWS_SECRET_ACCESS_KEY"] = t2
    os.environ["AWS_SESSION_TOKEN"] = t3
    os.environ["AWS_DEFAULT_REGION"] = 'us-east-1'
    fs = s3fs.S3FileSystem(
        client_kwargs={'endpoint_url': 'https://'+'minio.lab.sspcloud.fr'},
        key = os.environ["AWS_ACCESS_KEY_ID"], 
        secret = os.environ["AWS_SECRET_ACCESS_KEY"], 
        token = os.environ["AWS_SESSION_TOKEN"])


    #Stockage sur S3
    MY_BUCKET = "guillaume176"

    FILE_PATH_OUT_S3 = f"{MY_BUCKET}/alex/tabledep.csv"

    with fs.open(FILE_PATH_OUT_S3,"wb") as file_out:
        saved_table.to_csv(file_out, index=False)

    st.rerun()
    st.success("✅ Dépense ajoutée")





# Ajouter une rentré d'argent
st.subheader("➕ Ajouter une rentré d'argent")

with st.form("form_argent"):
    col1, col2 = st.columns(2)

    with col1:
        montant = st.number_input(
            "💶 Montant",
            min_value=0.0,
            step=0.50,
            format="%.2f"
        )

    with col2:
        categorie = st.selectbox(
            "🔠 Catégorie",
            [
                "Salaire Alex",
                "Jeux",
                "Extra 😉"
            ]
        )

    ajouter_argent = st.form_submit_button("Ajouter le revenu")

if ajouter_argent:
    nouvelle_rentre = pd.DataFrame([{
        "Date/Heure": datetime.now(ZoneInfo("Europe/Paris")).strftime("%d/%m/%Y %H:%M"),
        "Montant": montant,
        "Catégorie": categorie,
        "ref" : ref
    }])

    entry = pd.concat(
        [entry, nouvelle_rentre],
        ignore_index=True
    )


    os.environ["AWS_ACCESS_KEY_ID"] = t1
    os.environ["AWS_SECRET_ACCESS_KEY"] = t2
    os.environ["AWS_SESSION_TOKEN"] = t3
    os.environ["AWS_DEFAULT_REGION"] = 'us-east-1'
    fs = s3fs.S3FileSystem(
        client_kwargs={'endpoint_url': 'https://'+'minio.lab.sspcloud.fr'},
        key = os.environ["AWS_ACCESS_KEY_ID"], 
        secret = os.environ["AWS_SECRET_ACCESS_KEY"], 
        token = os.environ["AWS_SESSION_TOKEN"])
    



    #Stockage sur S3
    MY_BUCKET = "guillaume176"

    FILE_PATH_OUT_S3 = f"{MY_BUCKET}/alex/entry.csv"

    with fs.open(FILE_PATH_OUT_S3,"wb") as file_out:
        entry.to_csv(file_out, index=False)

    st.success("✅ Revenu ajouté ")

    st.rerun()
    


# Détail des dépenses
st.text("Détail des dépenses du mois")

st.dataframe(
    saved_table.iloc[1:,].iloc[::-1][["Date/Heure", "Montant", "Catégorie"]],
    use_container_width=True,
    hide_index=True,
    column_config={
        "Date/Heure": st.column_config.TextColumn("📅 Date"),

        "Montant": st.column_config.NumberColumn(
            "💶 Montant",
            format="%.2f €"
        ),

        "Catégorie": st.column_config.TextColumn("🏷️ Catégorie")
    }
)



# Détail des revenus
st.text("Détail des revenus du mois")

st.dataframe(
    entry.iloc[1:,].iloc[::-1][["Date/Heure", "Montant", "Catégorie"]],
    use_container_width=True,
    hide_index=True,
    column_config={
        "Date/Heure": st.column_config.TextColumn("📅 Date"),

        "Montant": st.column_config.NumberColumn(
            "💶 Montant",
            format="%.2f €"
        ),

        "Catégorie": st.column_config.TextColumn("🏷️ Catégorie")
    }
)


#Messages (suggestions etc)


with st.form("form_mess"):
    mess = st.text_input("📝 Message du jour !")

    ajouter_message = st.form_submit_button("Afficher le message")

if ajouter_message:
    nouveau_mess = pd.DataFrame([{
        "Date/Heure": datetime.now(ZoneInfo("Europe/Paris")).strftime("%d/%m/%Y %H:%M"),
        "Message": mess
    }])

    message = pd.concat(
        [message, nouveau_mess],
        ignore_index=True
    )

    os.environ["AWS_ACCESS_KEY_ID"] = t1
    os.environ["AWS_SECRET_ACCESS_KEY"] = t2
    os.environ["AWS_SESSION_TOKEN"] = t3
    os.environ["AWS_DEFAULT_REGION"] = 'us-east-1'
    fs = s3fs.S3FileSystem(
        client_kwargs={'endpoint_url': 'https://'+'minio.lab.sspcloud.fr'},
        key = os.environ["AWS_ACCESS_KEY_ID"], 
        secret = os.environ["AWS_SECRET_ACCESS_KEY"], 
        token = os.environ["AWS_SESSION_TOKEN"])
    



    #Stockage sur S3
    MY_BUCKET = "guillaume176"

    FILE_PATH_OUT_S3 = f"{MY_BUCKET}/alex/message.csv"

    with fs.open(FILE_PATH_OUT_S3,"wb") as file_out:
        message.to_csv(file_out, index=False)

    st.rerun()

    
