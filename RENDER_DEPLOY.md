# Déploiement sur Render

## Configuration créée

1. **render.yaml** - Configuration Render pour le service web
2. **requirements.txt** - Dépendances Python pour Render
3. **runtime.txt** - Version Python spécifique
4. **Port dynamique** - Le serveur utilise maintenant `$PORT` de Render

## Étapes de déploiement

1. **Créer un compte Render** (si pas déjà fait)
   - Aller sur https://render.com

2. **Connecter votre repo GitHub**
   - Push ce code sur GitHub
   - Dans Render, cliquer "New +" → "Web Service"
   - Connecter votre repo GitHub

3. **Configuration automatique**
   - Render détectera automatiquement `render.yaml`
   - Le service sera configuré automatiquement

4. **Variables d'environnement** (optionnel)
   Si vous voulez que le serveur MCP communique avec Render :
   - Ajouter dans Render Dashboard :
     ```
     PETANQUE_API_URL = https://votre-app.onrender.com
     ```

5. **Déployer**
   - Cliquer "Create Web Service"
   - Attendre le build et déploiement

## URL de votre API

Une fois déployé, votre API sera accessible à :
```
https://[nom-de-votre-service].onrender.com
```

Les endpoints seront :
- `POST https://[...].onrender.com/reset`
- `POST https://[...].onrender.com/cochonnet/place`
- `POST https://[...].onrender.com/ball/throw`
- `GET https://[...].onrender.com/state`
- `GET https://[...].onrender.com/distances`
- `GET https://[...].onrender.com/health`

## Visualisateur

Pour le visualisateur HTML, vous devrez :
1. Mettre à jour l'URL de l'API dans `visualizer.html`
2. L'héberger séparément (GitHub Pages, Netlify, etc.)

## Note importante

Le plan gratuit de Render met le service en veille après 15 minutes d'inactivité. Le premier appel peut prendre 30-60 secondes pour redémarrer.