# Zeversolar Home Assistant Integration - Verbeteringen

## Probleem
De originele Zeversolar integratie had een probleem waarbij 's nachts of bij weinig zonlicht de omvormer uitschakelt (normaal gedrag), maar Home Assistant dit behandelde als een fout. Dit resulteerde in:
- Error logs in Home Assistant
- Rode foutmeldingen in de integratie interface
- Onnodige zorgen voor gebruikers

## Oplossing
Deze verbeterde versie implementeert slimme offline handling:

### Nieuwe Features
1. **Status Sensor**: Een nieuwe sensor die "Online" of "Offline" toont
2. **Slimme Error Handling**: Onderscheid tussen echte fouten en normale offline status
3. **Behoud van Data**: Sensoren blijven beschikbaar met laatste bekende waarden
4. **Verbeterde Logging**: Geen error logs voor normale offline situaties

### Wijzigingen per Bestand

#### `coordinator.py`
- Toegevoegd: `is_online` status tracking
- Toegevoegd: `last_known_data` opslag voor laatste bekende waarden
- Verbeterd: Slimme error handling die onderscheid maakt tussen netwerkfouten en normale offline status
- Verbeterd: Debug logging in plaats van error logging voor normale offline situaties

#### `sensor.py`
- Toegevoegd: Nieuwe "status" sensor (online/offline)
- Verbeterd: Sensoren tonen 0W in plaats van fout wanneer offline
- Verbeterd: Energy sensor behoudt laatste waarde wanneer offline
- Toegevoegd: `available` property die sensoren beschikbaar houdt

#### `entity.py`
- Verbeterd: Fallback device info wanneer geen data beschikbaar is
- Toegevoegd: Gebruik van laatste bekende data voor device informatie

#### `strings.json`
- Toegevoegd: Vertalingen voor nieuwe status sensor
- Toegevoegd: Online/Offline state vertalingen

### Gedrag
**Dag (omvormer aan):**
- Status: Online
- Power sensor: Toont actuele wattage
- Energy sensor: Toont dagelijkse opbrengst
- Alle sensoren beschikbaar

**Nacht (omvormer uit):**
- Status: Offline
- Power sensor: Toont 0W
- Energy sensor: Behoudt laatste bekende waarde
- Alle sensoren blijven beschikbaar
- Geen error logs of foutmeldingen

### Voor Gebruikers
- Geen onnodige foutmeldingen meer 's nachts
- Duidelijke status indicator
- Behoud van belangrijke data (energie opbrengst van die dag)
- Automatisch herstel wanneer omvormer weer online komt

### Technische Details
- Backward compatible met bestaande installaties
- Gebruikt bestaande zeversolar library
- Geen breaking changes in API
- Minimale performance impact