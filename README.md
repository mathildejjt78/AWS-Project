# AWS Crypto Project

Application serverless AWS Amplify pour la gestion et l'export de données de cryptomonnaies.

## Fonctionnalités

- Récupération des prix de cryptomonnaies via l'API CoinGecko
- Stockage des données dans DynamoDB
- Export des données vers S3 avec URLs pré-signées
- Gestion des utilisateurs (création et recherche)

## Architecture

### Storage
- **DynamoDB (cryptoPrices)**
  - Table principale pour les prix des cryptomonnaies
  - Structure : 
    - id (partition key)
    - timestamp (sort key)
    - name
    - symbol
    - price

- **S3 (cryptoStorage)**
  - Stockage des exports de données
  - Dossier `exports/` pour les fichiers JSON
  - URLs pré-signées valables 1 heure

### API REST (crypto)
- Endpoint `/export`
  - Méthode : GET
  - Export des données vers S3
  - Retourne une URL pré-signée

### Functions Lambda

1. **crypto**
   - Récupération des données CoinGecko
   - Mise à jour DynamoDB
   - Exécution toutes les 5 minutes

2. **signeData**
   - Export DynamoDB → S3
   - Génération de fichiers JSON horodatés
   - Création d'URLs pré-signées

3. **getUser**
   - Recherche d'utilisateurs par email
   - Utilisation d'un index secondaire 'emails'

4. **saveUser**
   - Création d'utilisateurs
   - Validation des données
   - Vérification des doublons d'email

## Installation

1. **Prérequis**
   - Node.js
   - AWS CLI
   - Amplify CLI

2. **Configuration**
```bash
# Cloner le repository
git clone git@github.com:mathildejjt78/AWS-Project.git
cd AWS-Project

# Installer les dépendances
npm install

# Configurer Amplify
amplify configure

# Initialiser le projet
amplify init
```

## Déploiement

```bash
amplify push
```

## Utilisation

### Export des données
```bash
# Récupérer l'URL d'export
curl https://[api-id].execute-api.eu-west-1.amazonaws.com/dev/export
```

### Format de réponse
```json
{
    "message": "Export successful",
    "url": "https://[s3-url]",
    "file_key": "exports/crypto_2024-03-21T10-30-00.json"
}
```

### Format des données exportées
```json
{
    "id": "bitcoin",
    "timestamp": "2024-03-21T10:30:00",
    "name": "Bitcoin",
    "symbol": "btc",
    "price": 65000.00
}
```

## Structure du projet
```
amplify/
├── backend/
│   ├── api/
│   │   └── crypto/          # API REST
│   ├── function/
│   │   ├── crypto/         # Récupération des prix
│   │   ├── signeData/      # Export vers S3
│   │   ├── getUser/        # Recherche utilisateur
│   │   └── saveUser/       # Création utilisateur
│   └── storage/
│       ├── cryptoprices/   # DynamoDB
│       └── cryptostorage/  # S3
```

## Technologies
- AWS Amplify
- AWS Lambda
- Amazon DynamoDB
- Amazon S3
- Python
- CoinGecko API

## Sécurité
- URLs pré-signées pour les téléchargements
- Validation des données utilisateur
- Gestion des erreurs
- Variables d'environnement
- Index secondaires DynamoDB
