# Zeversolar Home Assistant Integration - Improvements

## Problem
The original Zeversolar integration had an issue where the inverter shuts down at night or in low sunlight conditions (normal behavior), but Home Assistant treated this as an error. This resulted in:
- Error logs in Home Assistant
- Red error notifications in the integration interface
- Unnecessary concerns for users

## Solution
This improved version implements smart offline handling:

### New Features
1. **Status Sensor**: A new sensor that shows "Online" or "Offline"
2. **Smart Error Handling**: Distinguishes between real errors and normal offline status
3. **Data Preservation**: Sensors remain available with last known values
4. **Improved Logging**: No error logs for normal offline situations

### Changes per File

#### `coordinator.py`
- Added: `is_online` status tracking
- Added: `last_known_data` storage for last known values
- Improved: Smart error handling that distinguishes between network errors and normal offline status
- Improved: Debug logging instead of error logging for normal offline situations
- Added: Suppression of retry library logs during offline periods

#### `sensor.py`
- Added: New "status" sensor (online/offline)
- Improved: Sensors show 0W instead of error when offline
- Improved: Energy sensor preserves last value when offline
- Added: `available` property that keeps sensors available
- Improved: Smart value handling for offline periods

#### `entity.py`
- Improved: Fallback device info when no data is available
- Added: Use of last known data for device information
- Added: Support for offline setup scenarios

#### `config_flow.py`
- Improved: Allow configuration even when inverter is offline
- Added: Offline setup support for nighttime configuration

#### `__init__.py`
- Improved: Skip initial refresh to allow setup when offline
- Added: Graceful handling of offline state during setup

#### `strings.json`
- Added: Translations for new status sensor
- Added: Online/Offline state translations

#### `icons.json`
- Updated: Better icons for inverter representation
- Added: Status-specific icons for online/offline states

### Behavior
**Day (inverter on):**
- Status: Online
- Power sensor: Shows actual wattage
- Energy sensor: Shows daily production
- All sensors available

**Night (inverter off):**
- Status: Offline
- Power sensor: Shows 0W
- Energy sensor: Retains last known value
- All sensors remain available
- No error logs or notifications

### For Users
- No more unnecessary error notifications at night
- Clear status indicator
- Preservation of important data (daily energy production)
- Automatic recovery when inverter comes back online

### Technical Details
- Backward compatible with existing installations
- Uses existing zeversolar library
- No breaking changes in API
- Minimal performance impact