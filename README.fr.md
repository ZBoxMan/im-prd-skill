# im-prd-skill

[English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Português](README.pt.md) | [Français](README.fr.md)

Un Claude Agent Skill pour rédiger des PRD de produits de messagerie (IM) et sociaux. Il fournit une bibliothèque de 26 modules décrivant comment les principales applications de messagerie traitent chaque fonctionnalité, de sorte que les spécifications générées suivent par défaut les conventions de l'IM. Seuls les points sur lesquels les applications principales diffèrent réellement sont soumis au décideur, sous forme de questions à choix multiples. Il peut produire uniquement un brouillon de livraison en Markdown, ou écrire aussi les cartes d'annotation sur un canevas Figma.

Le skill a été conçu pour l'équipe ZYMIX. Cette édition publique retire les clés de fichier Figma de l'équipe, les valeurs du système de design, les arbitrages internes et les preuves brutes ; le flux de travail, la bibliothèque de règles, les modèles, les scripts et les cas d'évaluation sont intacts.

## Éditions

| Édition | Chemin | Remarques |
|---|---|---|
| English | [`en/box-prd-create/`](en/box-prd-create/) | À utiliser pour toute langue autre que le chinois. Les règles sont en anglais ; le brouillon de livraison est rédigé dans la langue de l'utilisateur. |
| 简体中文 | [`zh-CN/box-prd-create/`](zh-CN/box-prd-create/) | Édition d'origine. Inclut les cas d'évaluation (`evals/`) et l'historique complet des modifications. |

Les deux éditions portent le nom de skill `box-prd-create` ; installez-en une seule.

## Ce que cela résout

Demander directement à une IA de rédiger la spécification d'une fonctionnalité d'IM échoue souvent de trois façons : des règles incertaines sont écrites comme si elles étaient tranchées ; seul le cas nominal est couvert, au détriment d'états comme bloqué, compte supprimé, hors ligne, multi-appareil et différences entre groupe et conversation individuelle ; et les conventions du secteur se mélangent aux quelques décisions que l'équipe doit vraiment prendre, si bien que le décideur doit tout lire pour les trouver.

La façon dont ce skill y répond :

- **Bibliothèque de règles à trois niveaux** : socle (les applications principales s'accordent ; à suivre par défaut), convention (la plupart des applications font ainsi ; recommandation adoptée par défaut), divergence (les applications diffèrent ; étiquetée Must-ask (à demander) ou Default-OK (défaut acceptable)).
- **Seules les questions indispensables sont posées** : au plus 4 questions à choix multiples par tour, l'option recommandée en premier. Tout le reste est rédigé selon la recommandation et listé ligne par ligne sous « Defaulted to recommendation » (retenu selon la recommandation) pour relecture.
- **Matrice de couverture des états** : succès, échec, délai dépassé, hors ligne, autorisations, synchronisation multi-appareil et « l'autre personne vous a bloqué / a supprimé son compte / a quitté le groupe » sont vérifiés un par un.
- **L'incertitude reste visible** : les points à trancher s'écrivent `{TBD: topic, recommended: approach}` et les faits manquants `{TBC: what is missing}`. Rien n'est présenté comme tranché.
- **Barrière d'écriture** : avant de toucher à Figma, le skill liste tous les nœuds qu'il va créer et les lots ; il n'écrit sur le canevas qu'après l'approbation du décideur.

## Flux de travail

| Étape | Ce qui se passe |
|---|---|
| 0 Cadrage du produit | Confirmer le type de conversation (individuelle / groupe / canal / communauté), les plateformes, le chiffrement de bout en bout, la possibilité pour des inconnus de joindre les utilisateurs et les prérequis de faisabilité |
| 1 Verrouiller la source de vérité | Consigner le fichier et les nœuds Figma ; étiqueter chaque exigence comme définie / à confirmer / suggérée |
| 2 Vérification des normes d'IM | Lire les modules concernés : suivre les socles, adopter les conventions par défaut, traiter les divergences selon leur niveau |
| 3 Référence concurrentielle | Recherche externe uniquement pour les capacités que la bibliothèque ne couvre pas |
| 4 Matrice de couverture des états | Dimensions générales plus états indispensables du module, chacun marqué couvert / non applicable / non défini |
| 5 Brouillon d'abord | Rédiger le brouillon de livraison en Markdown et exécuter `lint_card_text.py` ; ajouter un test de lecture pour les brouillons plus longs |
| 6 Mise en page et numérotation | Planifier en une seule passe l'ordre des écrans, les lignes et la numérotation |
| 7 Barrière d'écriture | `lint_card_text.py --gate` réussit et le décideur approuve avant toute écriture |
| 8 Écriture des cartes et auto-vérification | Auto-vérification après chaque lot ; terminer par un accusé de recette |

Ordre du brouillon de livraison : Decisions for Box (décisions pour Box) → Defaulted to recommendation → Open items (points ouverts) → Role view summary (synthèse par rôle) → Cards (cartes) → Feature list (liste des fonctionnalités) → Acceptance checkpoints (points de recette, ≤ 12) → Suggested follow-ups (suites suggérées).

## Structure

```
en/box-prd-create/              # Édition anglaise (même structure dans zh-CN/)
├── SKILL.md                    # Flux de travail et routage (point d'entrée)
├── references/
│   ├── im-norms/               # 26 modules d'IM + anti-patterns + table des responsabilités
│   ├── draft-template.md       # Modèle du brouillon de livraison et des notes de travail
│   ├── self-check.md           # Auto-vérification de la livraison
│   ├── canvas-layout.md        # Mise en page du canevas Figma
│   ├── figjam.md               # Organigrammes et liste des fonctionnalités
│   ├── design-system.md        # Système de design (modèle, à remplir avec le vôtre)
│   ├── rulings.md              # Arbitrages (modèle, à remplir avec les vôtres)
│   └── HISTORY.md              # Historique des modifications
└── scripts/
    ├── lint_card_text.py       # Lint du texte des cartes (--gate pour la barrière d'écriture)
    ├── lint_skill.py           # Auto-vérification de la structure de la bibliothèque de règles
    └── brand_terms.txt         # Noms de marque interdits
```

Modules : comptes et appareils, contacts et confidentialité, liste des conversations, envoi et accusés, actions sur les messages, médias et fichiers, groupes et canaux, notifications, sûreté et sécurité, recherche/appels/stockage, structure des pages, modèles d'interaction, comptes de service et bots, paiements dans la conversation, fils/canaux/communautés, messages enrichis, traduction et IA, découverte/connexion/autorisations, compte portefeuille, invitations et croissance, âge et mineurs, sanctions et recours, publicité et personnalisation, points et abonnements, centre de confidentialité, tickets d'assistance.

## Installation

Claude Code (édition anglaise en exemple ; utilisez `zh-CN/box-prd-create` pour le chinois) :

```bash
git clone https://github.com/ZBoxMan/im-prd-skill.git
```

```bash
cp -R im-prd-skill/en/box-prd-create ~/.claude/skills/
```

claude.ai : compressez le dossier `box-prd-create` en zip et importez-le dans Paramètres → Capacités → Skills.

## Utilisation

Décrivez simplement la fonctionnalité, par exemple :

- « Ajoute les annonces de groupe aux conversations de groupe. Rédige le PRD, uniquement le brouillon de livraison pour l'instant. »
- « Ajoute "Télécharger mes données" dans les Paramètres. Écris le PRD sur Figma : figma.com/design/<fileKey>, dans la zone Paramètres. »
- « Quel délai prévoir pour annuler l'envoi d'un message ? J'en ai besoin dans le PRD. »

## L'adapter à votre équipe

- `references/design-system.md` : votre bibliothèque de design, les clés de composants et les tokens de couleur et de typographie (utilisé uniquement pour dessiner les écrans de prototype).
- `references/rulings.md` : les arbitrages de rédaction de votre équipe et les mises en page abandonnées.
- `scripts/brand_terms.txt` : les noms de marque qui ne doivent pas apparaître dans le texte des cartes.
- « ZYMIX » et « Box » dans SKILL.md désignent le nom du produit et le décideur ; remplacez-les selon vos besoins.
- L'écriture dans Figma nécessite le Desktop Bridge de [figma-console MCP](https://github.com/southleft/figma-console-mcp). Les brouillons en Markdown seul ne demandent rien de plus.
- `box-figma-prd` et `box-prd-review`, mentionnés dans SKILL.md, sont des skills compagnons privés de l'auteur (inspection du canevas et revue complète). Le flux de génération fonctionne sans eux.

## Évaluation

Réalisée sur l'édition chinoise :

- Comparaison en aveugle : 8 scénarios (multi-appareil, gestion de groupe, enveloppes rouges, signalement, sondages de groupe, fil d'amis, accueil des nouveaux utilisateurs, annulation d'envoi/modification) face à 21 skills similaires sur le même brief. Un juge Opus, sans connaître la source, a noté la justesse en IM, la couverture des cas limites, le traitement des décisions, l'implémentabilité et la lisibilité : 94 manches, 90 victoires, 4 défaites.
- Déclenchement réel : 31 prompts positifs et négatifs × 3 exécutions avec `claude -p` : 31/31 corrects, aucun faux déclenchement sur les négatifs.

Enregistrements : `zh-CN/box-prd-create/evals/trigger-results.md`. L'édition anglaise n'a pas été évaluée séparément.

## Sources et actualité

Collecté en octobre 2026 à partir du comportement public des principaux clients de messagerie, du code de clients open source, des centres d'aide officiels et de la documentation pour développeurs, ainsi que des spécifications de protocoles. Les fichiers de modules ne contiennent aucun nom de marque ; les détails par produit ne sont pas publiés. La plupart des valeurs sont des valeurs par défaut du client que les serveurs peuvent remplacer ; à revoir tous les 90 jours.

## Licence

MIT
