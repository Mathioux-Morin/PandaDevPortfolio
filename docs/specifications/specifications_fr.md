# Cahier des charges

## _PandaDev Portfolio_

> 🇬🇧 English version: [specifications_en.md](specifications_en.md)

| Version         | Date       | Auteurs                        | Changements      |
|-----------------|------------|--------------------------------|------------------|
| 0.1 (brouillon) | 29/10/2026 | Mathieu MORIN, Mathias GARAIOS | Première version |

---

## 1. Contexte

### 1.1 Présentation du projet

PandaDev est une équipe de développeurs. Le projet consiste à créer un site qui réunit plusieurs portfolios : chaque membre y présente son profil, ses compétences, son parcours et ses projets, et les projets réalisés ensemble sont présentés une seule fois, avec le rôle de chacun. Le site n'est pas limité à un nombre fixe de portfolios (voir [3.5 Ajout d'un portfolio](#35-ajout-dun-portfolio)).

### 1.2 Rôles dans le projet

Les membres de l'équipe sont à la fois commanditaires, développeurs et utilisateurs du site. Ils se partagent :

- la conception (cahier des charges, schéma de la base de données) ;
- le développement de l'API, du site et de la base de données ;
- la rédaction de la documentation ;
- la saisie de leur propre contenu dans l'espace privé.

### 1.3 Public visé

- Recruteurs et entreprises, en particulier pour des offres de stage, d'alternance ou d'emploi ;
- Enseignants, jurys et autres développeurs qui veulent voir des réalisations concrètes.

### 1.4 Problématique

Un CV ou un profil LinkedIn ne montre pas les projets eux-mêmes : le code, les captures, les technos utilisées, le rôle de chacun dans un travail de groupe. Les membres veulent :

- un site unique qui présente l'équipe tout en laissant à chacun son identité ;
- un contenu modifiable depuis un espace privé, sans toucher au code ni redéployer le site (seule la mise en page propre à chaque membre se fait dans le code, voir [3.5](#35-ajout-dun-portfolio)) ;
- un site bilingue, en français et en anglais.

### 1.5 Solution retenue

Trois composants, versionnés dans le même dépôt :

- **API REST (FastAPI, Python 3.15, SQLModel)** : authentification par login et mot de passe (jeton JWT), lecture publique des contenus, écriture réservée aux membres connectés, téléversement des images.
- **Site web (Nuxt 4, Nuxt UI, Bun)** : partie publique (accueil, portfolios, projets, à propos) et espace privé de saisie. Traduction avec `@nuxtjs/i18n`.
- **Base de données (PostgreSQL 18, Docker Compose)** : stocke les contenus (profils, projets, technos, médias…). Les fichiers images sont stockés hors de la base. Le schéma est décrit dans [`docs/database/`](../database/).

---

## 2. Existant

### 2.1 Déjà réalisé

| Élément          | Détail                                                                                                                                                               |
|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Authentification | Connexion par login et mot de passe (bcrypt, jeton JWT), session Nuxt chiffrée, déconnexion                                                                          |
| Espace privé     | Page « Mon espace » réservée aux membres connectés, encore vide                                                                                                      |
| Traduction       | Interface entièrement traduite en français (langue par défaut) et en anglais                                                                                         |
| Apparence        | Palette de couleurs PandaDev (Radix), mode clair / sombre, en-tête responsive                                                                                        |
| Pages publiques  | Accueil, Projets et À propos créées, sans contenu                                                                                                                    |
| Portfolios       | Une page par membre, avec la structure de sa mise en page propre (layout, en-tête, hero) et des composants communs (projets, parcours, technos, liens), encore vides |
| Base de données  | Table `users` créée ; schéma complet proposé ([schema.puml](../database/schema.puml), [dictionnaire de données](../database/data_dictionary.md))                     |

### 2.2 Reste à faire

- Créer les tables du schéma proposé et les routes de l'API correspondantes ;
- Afficher les contenus sur les pages publiques ;
- Construire les formulaires de saisie de l'espace privé ;
- Mettre en place le stockage des images ;
- Créer le pied de page du site, présent sur toutes les pages, avec le lien vers les mentions légales ;
- Choisir l'hébergeur, nécessaire à la mise en ligne et à la page « Mentions légales ».

---

## 3. Besoins fonctionnels

### 3.1 Fonctionnalités indispensables

1. Présenter le portfolio de chaque membre : profil, disponibilité, compétences, parcours et liens.
2. Présenter les projets, individuels ou de groupe, avec le rôle de chaque membre.
3. Permettre à chaque membre de modifier son contenu depuis l'espace privé, sans toucher au code.
4. Proposer tout le contenu en français et en anglais.

### 3.2 Actions des utilisateurs

Le visiteur peut :

- consulter la page d'accueil, les portfolios, les projets et la page À propos ;
- passer d'un portfolio à l'autre depuis la barre de navigation ;
- filtrer les projets par techno ou par membre ;
- changer de langue et passer du mode clair au mode sombre ;
- contacter un membre par e-mail, par téléphone ou par ses liens (LinkedIn, Discord…), s'il les a renseignés.

Le membre connecté peut :

- modifier son profil, ses coordonnées de contact, sa disponibilité et sa section « Now » ;
- gérer ses liens, son parcours et ses technos ;
- créer, modifier, publier et mettre en avant les projets dont il est membre ;
- ajouter des co-auteurs à un projet et préciser leur rôle ;
- téléverser des images (avatar, couverture, galerie).

### 3.3 Données à enregistrer

Le détail de chaque champ (type, contraintes, caractère obligatoire) est dans le [dictionnaire de données](../database/data_dictionary.md). En résumé :

| Donnée   | Contenu                                                                                                                                    |
|----------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Profil   | Nom affiché, titre, bio, ville, avatar, disponibilité, section « Now », e-mail et téléphone de contact, CV en PDF par langue (facultatifs) |
| Liens    | GitHub, Discord, YouTube, LinkedIn, tous facultatifs                                                                                       |
| Parcours | Expériences professionnelles et formations                                                                                                 |
| Technos  | Catalogue partagé (nom, catégorie, icône) ; score de 0 à 100 par membre, niveau calculé automatiquement                                    |
| Projets  | Titre, résumé, présentation, couverture, galerie, liens, dates, technos, membres et rôles, brouillon ou publié, mis en avant               |
| Médias   | Images (WebP) et PDF : dimensions, poids, texte alternatif                                                                                 |

Tous les textes affichés aux visiteurs sont saisis dans les deux langues.

### 3.4 Résultats attendus

- Un visiteur comprend en moins d'une minute qui est chaque membre, ce qu'il sait faire et s'il est disponible.
- Chaque projet de groupe indique clairement qui a fait quoi.
- Un membre met à jour son contenu en quelques minutes, sans aide et sans redéploiement.
- Un brouillon n'est jamais visible du public.

### 3.5 Ajout d'un portfolio

Le site n'est pas limité à un nombre fixe de portfolios. Le **contenu** d'un portfolio se gère depuis l'espace privé ; sa **mise en page propre** se fait dans le code.

Ajouter un membre se fait en trois étapes :

1. **Compte** : un développeur crée le compte du membre dans la base de données et choisit son slug, par exemple `jean-dupont`.
2. **Contenu** : le membre se connecte et remplit son profil, ses liens, son parcours et ses technos depuis l'espace privé. Son portfolio est alors visible à l'adresse `/portfolios/<slug>`, avec la mise en page par défaut.
3. **Mise en page propre (facultatif)** : un développeur crée, dans `web/app/` :
   - `pages/portfolios/<slug>/index.vue` : la page du membre ;
   - `layouts/<slug>.vue` : sa mise en page ;
   - `components/<slug>/` : ses composants (en-tête, hero…), qui peuvent réutiliser les composants communs de `components/portfolio/`.

   Cette page remplace automatiquement la page par défaut pour ce membre.

Les fichiers sont nommés d'après le slug, qui est unique : deux homonymes ne peuvent donc pas entrer en conflit (deux « Jean Dupont » auraient par exemple les slugs `jean-dupont` et `jean-dupont-2`).

---

## 4. Besoins non fonctionnels

| Critère          | Détail                                                                                                                                                                                                                                                                                                                   |
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Langues          | Interface et contenus en français (par défaut) et en anglais ; un contenu sans ses deux traductions est refusé                                                                                                                                                                                                           |
| Responsive       | Utilisable sur ordinateur, tablette et téléphone                                                                                                                                                                                                                                                                         |
| Accessibilité    | Texte alternatif obligatoire sur les images, contrastes de la palette Radix, navigation au clavier                                                                                                                                                                                                                       |
| Sécurité         | Mots de passe forts (voir UC-12) et hachés (bcrypt), jetons JWT, écriture réservée aux membres connectés, édition d'un projet limitée à ses membres                                                                                                                                                                      |
| Erreurs          | Page 404 et page d'erreur aux couleurs du site, traduites, avec l'en-tête et un lien de retour vers l'accueil ; aucun détail technique n'est montré au visiteur                                                                                                                                                          |
| Mentions légales | Page « Mentions légales » (éditeurs du site, hébergeur), traduite et accessible depuis le pied de page de chaque page                                                                                                                                                                                                    |
| Fichiers         | Vérification du vrai type de fichier, taille limitée, conversion en WebP, suppression des données EXIF, nom de fichier aléatoire                                                                                                                                                                                         |
| Sauvegardes      | Sauvegarde automatique quotidienne de la base de données et du dossier `uploads/`, conservée 30 jours ; une restauration est testée avant la mise en ligne                                                                                                                                                               |
| Performance      | Images optimisées (WebP), rendu côté serveur de Nuxt pour un premier affichage rapide                                                                                                                                                                                                                                    |
| Référencement    | Rendu côté serveur, URL lisibles (slugs), titre et description propres à chaque page, aperçu de partage (Open Graph) avec l'avatar du membre ou la couverture du projet, `sitemap.xml` des pages publiques (sans brouillons ni espace privé), liens entre les versions française et anglaise de chaque page (`hreflang`) |
| Maintenabilité   | Code typé, linters (ruff, ESLint), tests de l'API (pytest) et du site (Vitest avec `@nuxt/test-utils` pour les composants, Playwright pour les parcours principaux : connexion, consultation d'un portfolio, publication d'un projet), documentation tenue à jour                                                        |

---

## 5. Contraintes et limites

- **Comptes** : pas d'inscription publique. Les comptes des membres sont créés directement dans la base de données, avec leur slug. Changer un slug reste possible dans la base, mais il faut alors renommer les fichiers de la mise en page du membre, et les anciens liens ne fonctionnent plus. La suppression d'un compte se fait aussi dans la base de données.
- **Langues** : uniquement le français et l'anglais.
- **Contact** : pas de formulaire de contact, donc pas de messages à stocker ni de spam à gérer. Les visiteurs écrivent ou téléphonent directement au membre, ou passent par ses liens.
- **Liens** : limités à GitHub, Discord, YouTube et LinkedIn. En ajouter un autre demande une migration de la base.
- **Confidentialité** : aucune donnée personnelle de visiteur n'est collectée. Seules les informations que les membres choisissent de publier sont stockées, y compris leur e-mail et leur téléphone de contact, qui restent facultatifs. L'adresse IP d'un visiteur sert uniquement, en mémoire, à limiter les demandes de coordonnées et de CV ; elle n'est jamais enregistrée. Le site n'utilise que des cookies et un stockage local techniques (session de connexion, langue, mode clair / sombre et thème) : aucun bandeau de consentement n'est nécessaire.
- **Hébergement** : à définir. Le choix doit être fait avant la mise en ligne, car la page « Mentions légales » doit indiquer le nom, l'adresse et le téléphone de l'hébergeur.

---

## 6. Personas

### Le visiteur recruteur

Consulte les portfolios et les projets.

| Attribut           | Détail                                                                                             |
|--------------------|----------------------------------------------------------------------------------------------------|
| Profil             | Recruteur, chargé de RH, maître d'apprentissage ou enseignant                                      |
| Objectif principal | Évaluer rapidement les compétences et la disponibilité d'un membre                                 |
| Comportement       | Visite courte, souvent sur téléphone : regarde les projets mis en avant, puis un ou deux en détail |
| Niveau technique   | Variable : le site doit rester lisible sans connaissances techniques                               |
| Attentes           | Savoir qui a fait quoi, voir du concret (captures, code, démo), trouver un moyen de contact        |

### Le membre PandaDev

Gère son portfolio et ses projets depuis l'espace privé.

| Attribut           | Détail                                                                                                  |
|--------------------|---------------------------------------------------------------------------------------------------------|
| Profil             | Développeur, membre de l'équipe PandaDev                                                                |
| Objectif principal | Présenter ses compétences et ses projets, garder son portfolio à jour                                   |
| Comportement       | Se connecte de temps en temps pour ajouter un projet ou une techno, ou mettre à jour sa section « Now » |
| Niveau technique   | Développeur, mais la saisie doit rester rapide et ne jamais demander d'intervenir dans la base          |
| Droits             | Modifie son propre profil et les projets dont il est membre                                             |

---

## 7. Cas d'utilisation

Statut : ✅ fait, 🟡 commencé, ⬜ à faire.

| #     | Cas d'utilisation                  | Acteur           | Statut |
|-------|------------------------------------|------------------|--------|
| UC-01 | Consulter la page d'accueil        | Visiteur         | 🟡     |
| UC-02 | Parcourir les portfolios           | Visiteur         | ⬜     |
| UC-03 | Consulter le portfolio d'un membre | Visiteur         | 🟡     |
| UC-04 | Parcourir les projets              | Visiteur         | 🟡     |
| UC-05 | Consulter un projet                | Visiteur         | ⬜     |
| UC-06 | Consulter la page À propos         | Visiteur         | 🟡     |
| UC-07 | Personnaliser l'affichage          | Visiteur         | 🟡     |
| UC-08 | Rechercher sur le site             | Visiteur         | ⬜     |
| UC-09 | Consulter la frise chronologique   | Visiteur         | ⬜     |
| UC-10 | Consulter les statistiques         | Visiteur         | ⬜     |
| UC-11 | Découvrir l'easter egg             | Visiteur         | ⬜     |
| UC-12 | Se connecter et se déconnecter     | Membre           | 🟡     |
| UC-13 | Modifier son profil                | Membre           | ⬜     |
| UC-14 | Gérer ses liens sociaux            | Membre           | ⬜     |
| UC-15 | Gérer son parcours                 | Membre           | ⬜     |
| UC-16 | Gérer ses technos                  | Membre           | ⬜     |
| UC-17 | Gérer le catalogue de technologies | Membre           | ⬜     |
| UC-18 | Gérer un projet                    | Membre           | ⬜     |
| UC-19 | Gérer les membres d'un projet      | Membre           | ⬜     |
| UC-20 | Téléverser et gérer des médias     | Membre           | ⬜     |
| UC-21 | Écrire et lire des recommandations | Membre, visiteur | ⬜     |
| UC-22 | Publier et lire le devlog          | Membre, visiteur | ⬜     |

---

## 8. User stories

Chaque cas d'utilisation regroupe ses user stories, au format « En tant que…, je veux…, afin de… », suivies de ses critères d'acceptation.

### UC-01 — Consulter la page d'accueil

- **US-01.1** — En tant que visiteur, je veux voir dès l'accueil les projets mis en avant, afin de découvrir les meilleures réalisations de l'équipe sans chercher.
- **US-01.2** — En tant que visiteur, je veux voir les membres de l'équipe avec leur titre et leur disponibilité, afin de savoir rapidement qui contacter.

Critères d'acceptation :

- seuls les projets publiés et mis en avant apparaissent, triés par position ;
- chaque membre renvoie vers son portfolio.

### UC-02 — Parcourir les portfolios

- **US-02.1** — En tant que visiteur, je veux voir la liste des membres (photo, nom, titre, disponibilité), afin de choisir le portfolio à consulter.
- **US-02.2** — En tant que visiteur, je veux accéder à chaque portfolio depuis la barre de navigation, afin de passer d'un membre à l'autre sans revenir à l'accueil.

Critères d'acceptation :

- l'entrée « Portfolios » de l'en-tête ouvre un menu qui liste chaque portfolio, avec un lien « Tous les portfolios » vers la page de liste ;
- ce menu est généré à partir des profils enregistrés, sans liste écrite dans le code, et il est présent dans tous les en-têtes (site principal et portfolios) ;
- le portfolio en cours est signalé dans le menu ;
- le menu reste utilisable sur mobile, dans le panneau latéral ;
- un membre sans profil n'apparaît ni dans la page ni dans le menu.

### UC-03 — Consulter le portfolio d'un membre

- **US-03.1** — En tant que visiteur, je veux lire la présentation d'un membre (bio, ville, disponibilité), afin de savoir qui il est et s'il cherche un stage, une alternance ou un emploi.
- **US-03.2** — En tant que visiteur, je veux voir ses technos regroupées par catégorie avec leur niveau, afin d'évaluer ses compétences.
- **US-03.3** — En tant que visiteur, je veux consulter son parcours (expériences et formations), du plus récent au plus ancien, afin de comprendre son évolution.
- **US-03.4** — En tant que visiteur, je veux voir ses projets et sa section « Now », afin de savoir ce qu'il a réalisé et sur quoi il travaille en ce moment.
- **US-03.5** — En tant que membre, je veux que mon portfolio ait sa propre mise en page, afin qu'il reflète ma personnalité.
- **US-03.6** — En tant que visiteur, je veux télécharger le CV d'un membre, afin de le joindre à un dossier de recrutement.

Critères d'acceptation :

- l'adresse est `/portfolios/<slug>` (`/en/portfolios/<slug>` en anglais) ;
- la disponibilité s'affiche sous forme de badge, et n'apparaît pas si elle n'est pas renseignée ;
- la section « Now » affiche sa date de dernière mise à jour ;
- seuls les liens renseignés s'affichent ;
- le bouton de téléchargement du CV n'apparaît que si un CV existe ; il propose le CV de la langue active, ou l'autre s'il n'y en a qu'un ;
- l'e-mail et le téléphone n'apparaissent que s'ils sont renseignés ;
- l'e-mail, le téléphone et le lien du CV ne sont pas inclus dans la page envoyée au navigateur : le visiteur clique sur « Afficher l'e-mail », « Afficher le téléphone » ou « Télécharger le CV », et le site les demande alors à l'API, pour limiter leur collecte par des robots de spam (un CV contient en général les mêmes coordonnées) ;
- l'API limite le nombre de ces demandes par visiteur (par exemple 10 par minute), pour qu'un robot ne puisse pas les récupérer en masse.

### UC-04 — Parcourir les projets

- **US-04.1** — En tant que visiteur, je veux voir tous les projets publiés sous forme de cartes (couverture, titre, résumé, technos), afin d'avoir une vue d'ensemble.
- **US-04.2** — En tant que visiteur, je veux filtrer les projets par techno ou par membre, afin de trouver ceux qui m'intéressent.

Critères d'acceptation :

- les brouillons ne sont jamais affichés ;
- les projets sont triés par position, puis du plus récent au plus ancien ;
- les filtres peuvent se combiner.

### UC-05 — Consulter un projet

- **US-05.1** — En tant que visiteur, je veux lire la présentation complète d'un projet et voir sa galerie d'images, afin de comprendre ce qu'il fait.
- **US-05.2** — En tant que visiteur, je veux voir les membres du projet et le rôle de chacun, afin de savoir qui a fait quoi.
- **US-05.3** — En tant que visiteur, je veux accéder au dépôt de code et à la démo, afin de juger du travail réel.

Critères d'acceptation :

- l'adresse est `/projects/<slug>` ;
- un brouillon renvoie une page 404 à un visiteur ;
- un lien de dépôt ou de démo absent n'est pas affiché ;
- un projet sans date de fin est présenté comme « en cours ».

### UC-06 — Consulter la page À propos

- **US-06.1** — En tant que visiteur, je veux lire une présentation de l'équipe PandaDev, afin de comprendre ce qui réunit ses membres et comment ils travaillent.

Critères d'acceptation :

- le texte est un texte fixe du site, traduit dans les fichiers de traduction, et non stocké en base.

### UC-07 — Personnaliser l'affichage

- **US-07.1** ✅ — En tant que visiteur, je veux changer la langue du site, afin de le lire en français ou en anglais.
- **US-07.2** ✅ — En tant que visiteur, je veux passer du mode clair au mode sombre, afin de lire confortablement.
- **US-07.3** — En tant que visiteur, je veux choisir un thème de couleurs inspiré d'un éditeur de code, afin de profiter d'un clin d'œil développeur.

Critères d'acceptation :

- la langue apparaît dans l'adresse (`/en/…` pour l'anglais) ;
- le mode et le thème choisis sont mémorisés pour la visite suivante ;
- chaque thème respecte les contrastes minimaux d'accessibilité.

### UC-08 — Rechercher sur le site

- **US-08.1** — En tant que visiteur, je veux ouvrir une recherche avec Ctrl+K (⌘K sur Mac) et trouver un projet, une techno ou un membre, afin d'aller directement à ce qui m'intéresse.

Critères d'acceptation :

- les résultats sont dans la langue active ;
- les brouillons sont exclus ;
- la recherche s'utilise entièrement au clavier.

### UC-09 — Consulter la frise chronologique

- **US-09.1** — En tant que visiteur, je veux voir sur une frise les projets et le parcours des membres, afin de suivre l'évolution de l'équipe.

Critères d'acceptation :

- la frise est construite à partir des dates déjà enregistrées, sans donnée supplémentaire ;
- elle peut être filtrée par membre.

### UC-10 — Consulter les statistiques

- **US-10.1** — En tant que visiteur, je veux voir des statistiques de l'équipe (nombre de projets, technos les plus utilisées…), afin de mesurer son activité.
- **US-10.2** — En tant que visiteur, je veux voir sur un projet ses statistiques GitHub (étoiles, commits, langages), afin de juger de son activité.

Critères d'acceptation :

- les statistiques de l'équipe sont calculées à partir des données existantes ;
- les statistiques GitHub sont lues depuis l'API GitHub à partir du lien du dépôt, mises en cache et jamais stockées en base ;
- si GitHub ne répond pas, le bloc est masqué sans erreur.

### UC-11 — Découvrir l'easter egg

- **US-11.1** — En tant que visiteur curieux, je veux découvrir une surprise cachée (par exemple avec le code Konami), afin de sourire en parcourant le site.

Critères d'acceptation :

- la surprise ne gêne jamais la navigation normale ;
- elle ne collecte ni n'enregistre aucune donnée.

### UC-12 — Se connecter et se déconnecter

- **US-12.1** ✅ — En tant que membre, je veux me connecter avec mon login et mon mot de passe, afin d'accéder à mon espace privé.
- **US-12.2** ✅ — En tant que membre, je veux me déconnecter, afin de protéger mon compte sur un poste partagé.
- **US-12.3** — En tant que membre, je veux changer mon mot de passe depuis mon espace privé, afin de ne jamais dépendre d'une intervention dans la base de données.

Critères d'acceptation :

- un message d'erreur traduit s'affiche si les identifiants sont incorrects ;
- l'espace privé redirige vers la page de connexion si le membre n'est pas connecté ;
- le mot de passe actuel est demandé pour en définir un nouveau ;
- le nouveau mot de passe est saisi deux fois et fait au moins 12 caractères (au plus 72 octets, limite de bcrypt) ;
- il obtient un score de robustesse d'au moins 3 sur 4 (bibliothèque zxcvbn) : les mots courants, les dates, les suites de clavier, le login et le nom du membre sont refusés ;
- une jauge indique la force du mot de passe pendant la saisie ;
- ces règles sont vérifiées par l'API, et pas seulement par le site ;
- après le changement, toutes les autres sessions sont déconnectées (l'API refuse les jetons émis avant la date du changement) ; la session en cours reçoit un nouveau jeton et reste connectée ;
- un message de confirmation traduit s'affiche après le changement.

### UC-13 — Modifier son profil

- **US-13.1** — En tant que membre, je veux modifier mon nom affiché, mon titre, ma bio et ma ville, afin de garder ma présentation à jour.
- **US-13.2** — En tant que membre, je veux changer ma photo de profil, afin d'être reconnaissable.
- **US-13.3** — En tant que membre, je veux indiquer ma disponibilité (en recherche d'emploi, de stage, d'alternance, ou indisponible), afin que les recruteurs sachent si je suis disponible.
- **US-13.4** — En tant que membre, je veux mettre à jour ma section « Now », afin de montrer sur quoi je travaille en ce moment.
- **US-13.5** — En tant que membre, je veux renseigner un e-mail et un numéro de téléphone de contact, afin que les recruteurs puissent me joindre directement.
- **US-13.6** — En tant que membre, je veux téléverser mon CV en PDF, en français et en anglais, afin que les recruteurs puissent le télécharger.

Critères d'acceptation :

- les textes sont saisis en français et en anglais ;
- l'identifiant d'URL (slug) est unique et ne contient que des minuscules, des chiffres et des tirets ;
- le slug est choisi à la création du compte (voir [3.5](#35-ajout-dun-portfolio)) et ne se modifie pas depuis l'espace privé, car il fixe l'adresse du portfolio et le nom des fichiers de sa mise en page ;
- la date de mise à jour de « Now » change automatiquement à chaque modification de la section ;
- l'e-mail et le téléphone sont facultatifs ; une adresse invalide est refusée et le numéro est enregistré au format international (`+33…`) ;
- chaque CV (français, anglais) est facultatif ; seul un PDF est accepté (10 Mo maximum, voir UC-20), et l'API vérifie que le fichier lié est bien un PDF ;
- remplacer un CV supprime l'ancien fichier ;
- un membre ne peut modifier que son propre profil.

### UC-14 — Gérer ses liens sociaux

- **US-14.1** — En tant que membre, je veux ajouter, modifier ou supprimer mes liens GitHub, Discord, YouTube et LinkedIn, afin que les visiteurs puissent me contacter ou voir mon activité.
- **US-14.2** — En tant que membre, je veux choisir l'ordre de mes liens, afin de mettre en premier le plus important.

Critères d'acceptation :

- tous les liens sont facultatifs, avec au plus un lien par réseau ;
- une adresse invalide est refusée.

### UC-15 — Gérer son parcours

- **US-15.1** — En tant que membre, je veux ajouter, modifier ou supprimer une expérience professionnelle ou une formation, afin de présenter mon parcours.

Critères d'acceptation :

- la date de fin est facultative (expérience en cours) et ne peut pas précéder la date de début ;
- une suppression demande une confirmation.

### UC-16 — Gérer ses technos

- **US-16.1** — En tant que membre, je veux ajouter une techno du catalogue à mon profil avec un score de 0 à 100, afin de montrer mon niveau.
- **US-16.2** — En tant que membre, je veux voir le niveau calculé à partir de mon score (Novice, Intermédiaire, Confirmé, Expert), afin de savoir comment il sera affiché.
- **US-16.3** — En tant que membre, je veux choisir l'ordre de mes technos, afin de mettre en avant les principales.

Critères d'acceptation :

- le niveau est calculé par la base de données et ne se saisit pas ;
- une techno ne peut être ajoutée qu'une fois par membre ;
- un score en dehors de 0 à 100 est refusé.

### UC-17 — Gérer le catalogue de technologies

- **US-17.1** — En tant que membre, je veux ajouter une techno au catalogue (nom, catégorie, icône), afin de pouvoir l'associer à mon profil ou à un projet.
- **US-17.2** — En tant que membre, je veux corriger ou supprimer une techno du catalogue, afin de garder un catalogue propre.

Critères d'acceptation :

- le nom d'une techno est unique ;
- les catégories sont : langage, framework, base de données, outil et IA ;
- supprimer une techno utilisée demande une confirmation qui indique combien de profils et de projets la perdront.

### UC-18 — Gérer un projet

- **US-18.1** — En tant que membre, je veux créer un projet en brouillon (titre, résumé, présentation, dates, liens, technos), afin de le préparer avant de le publier.
- **US-18.2** — En tant que membre du projet, je veux publier ou dépublier le projet, afin de choisir quand il devient visible.
- **US-18.3** — En tant que membre du projet, je veux mettre le projet en avant, afin qu'il apparaisse sur la page d'accueil.
- **US-18.4** — En tant que membre du projet, je veux supprimer le projet, afin de retirer un projet obsolète.
- **US-18.5** — En tant que membre du projet, je veux prévisualiser le brouillon tel qu'il apparaîtra aux visiteurs, afin de le vérifier avant de le publier.

Critères d'acceptation :

- le créateur devient automatiquement membre du projet ;
- seuls les membres du projet peuvent le modifier, le publier ou voir son brouillon ;
- les textes sont saisis en français et en anglais ;
- une suppression demande une confirmation ;
- la prévisualisation utilise la même page que le projet publié (`/projects/<slug>`), avec un bandeau « Brouillon : visible uniquement par les membres du projet » ;
- un visiteur ou un membre qui ne fait pas partie du projet reçoit une page 404 (voir UC-05).

### UC-19 — Gérer les membres d'un projet

- **US-19.1** — En tant que membre du projet, je veux ajouter un autre membre comme co-auteur, afin que le projet apparaisse aussi sur son portfolio.
- **US-19.2** — En tant que membre du projet, je veux préciser le rôle de chaque membre, afin que les visiteurs sachent qui a fait quoi.

Critères d'acceptation :

- un projet garde toujours au moins un membre : la base de données et l'API refusent de retirer son dernier membre, avec un message d'erreur traduit ;
- un compte ne peut pas être supprimé tant qu'il est membre d'un projet : il faut d'abord le retirer de ses projets, et supprimer ceux dont il est le seul membre ou leur ajouter un autre membre ;
- le rôle est facultatif, mais saisi dans les deux langues s'il est rempli.

### UC-20 — Téléverser et gérer des médias

- **US-20.1** — En tant que membre, je veux téléverser une image pour mon avatar, la couverture ou la galerie d'un projet, afin d'illustrer mon contenu.
- **US-20.2** — En tant que membre, je veux saisir le texte alternatif de chaque image, afin que le site reste accessible.
- **US-20.3** — En tant que membre du projet, je veux réordonner ou retirer des images de la galerie, afin de contrôler leur présentation.

Critères d'acceptation :

- les formats acceptés sont JPEG, PNG et WebP pour les images (converties en WebP) et PDF pour les documents ;
- la taille maximale est de 5 Mo pour une image et de 10 Mo pour un PDF ; un fichier trop lourd est refusé avec un message traduit ;
- les données EXIF (dont la position GPS) sont supprimées et le fichier reçoit un nom aléatoire ;
- supprimer une image utilisée comme avatar ou couverture la retire simplement de l'endroit où elle était affichée ;
- supprimer un compte conserve les images qu'il a ajoutées aux projets ; ses fichiers personnels qu'aucun projet n'utilise (avatar, CV) sont supprimés avec le compte.

### UC-21 — Écrire et lire des recommandations

- **US-21.1** — En tant que membre, je veux écrire une recommandation sur un autre membre, afin de valoriser son travail.
- **US-21.2** — En tant que visiteur, je veux lire les recommandations affichées sur un portfolio, afin d'avoir un autre regard sur le membre.
- **US-21.3** — En tant que membre, je veux accepter ou masquer une recommandation qui me concerne, afin de garder le contrôle de ce qui s'affiche sur mon portfolio.

Critères d'acceptation :

- un membre ne peut pas se recommander lui-même ;
- les recommandations de personnes extérieures ne sont pas prévues (modération, RGPD) ;
- une nouvelle recommandation n'est pas visible tant que le membre recommandé ne l'a pas acceptée ;
- le membre recommandé peut masquer plus tard une recommandation acceptée ;
- l'auteur peut modifier ou supprimer sa recommandation ; une modification la repasse en attente d'acceptation ;
- une table est à ajouter au schéma de la base, avec un état (`pending`, `accepted`, `hidden`).

### UC-22 — Publier et lire le devlog

- **US-22.1** — En tant que membre, je veux publier un article sur un problème résolu ou une techno découverte, afin de partager ce que j'apprends.
- **US-22.2** — En tant que visiteur, je veux lire les articles du devlog, afin de voir comment l'équipe raisonne.

Critères d'acceptation :

- un article est rédigé en français et en anglais, et peut rester en brouillon comme un projet ;
- le schéma de la base est à concevoir.

---

## 9. Priorités

### 9.1 Version 1 : obligatoire

- Consulter l'accueil, les portfolios, les projets et la page À propos (UC-01 à UC-06)
- Changer de langue et de mode clair / sombre (UC-07, US-07.1 et US-07.2)
- Se connecter et gérer tout son contenu depuis l'espace privé (UC-12 à UC-20)

### 9.2 Version 1.1 : souhaitée

- Thèmes de couleurs (UC-07, US-07.3)
- Recherche, frise chronologique et statistiques (UC-08 à UC-10)
- Easter egg (UC-11)

### 9.3 En dernier

- Recommandations (UC-21)
- Devlog (UC-22)

---

## 10. Hors périmètre

Ces idées ont été étudiées puis écartées, car elles brouillent le message professionnel du portfolio : badges et succès, soundboard, compteur de cafés, humeur du jour, citation du mois, calendrier des disponibilités, « mode recruteur » pour masquer le contenu non professionnel.
