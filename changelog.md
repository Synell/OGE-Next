# OGE Next Rel-07e815bd

## New
- Ranks, names and dates are now displayed when you hover a grade
- Ranks, names and dates are loaded for new grades
- Added a new setting to refresh the ranks, names and dates of all grades (useful if you want to see the ranks, names and dates of grades you already had before this update)
- What's New window is now displayed when you open the app after an update
- Logout button is now accessible from the "i" button in the top left corner of the sidebar

## Changes
- Bump cryptography from 41.0.3 to 41.0.6
- Updated the tooltip system so it's more customizable, instantaneous when hovering, and more consistent with the rest of the app

## Fix
- Fixed a bug where a "?" was displayed instead of the grade when the grade was 0

--------------------------------

# OGE Next Rel-07e7e910

## Fix
- Fixed a bug where the api wasn't working when at a grade value was null

--------------------------------

# OGE Next Rel-07e7bfac

## Fix
- Fixed a bug where the api wasn't working when at least one of the subject coeff was empty like this: "Subject Name ()"

--------------------------------

# OGE Next Rel-07e7bf10

## Technical Changes
- Language file system update
- Added various QSS file parameters for managing colors

## Fix
- Fixed a bug where the api wasn't working when at least one of the pole coeff was empty like this: "Pole Name ()"
- Applying a setting no longer shows a reload warning message if the edited setting(s) didn't require a reload to be applied

--------------------------------

# OGE Next Rel-07e77fd5

## Changes
- Made every color transition of each UE table round
- Added the possibility to reduce each UE table for easy average view
- Added the possibility to reduce the top new grade panel for easy access to the tables below it

## Fix
- Fixed a visual bug: the bottom of each UE table wasn't perfectly round
- "Report a bug" button wasn't working as it should (it was the link for App Manager instead of OGE Next)

--------------------------------

# OGE Next Rel-07e77fc5

## Changes
- Added a "report a bug" action

## Fix
- Fixed a visual bug (new grades, top display)

--------------------------------

# OGE Next Rel-07e77fb4

## Changes
- Added a preview of the new grades at the very top of the grades screen

--------------------------------

# OGE Next Rel-07e77f83

## Changes
- Added an icon next to new grades
- Added a message at the top of the widget saying how many grades are new

--------------------------------

# OGE Next Rel-07e77f6a

## Changes
- Added a log folder for the log files of the main application and for the errors and warnings from the api

## Fix
- Fixed empty poles with no coefficient crashing the app
- Fixed empty subjects with no coefficient crashing the app
- Fixed empty grade groups with no coefficient crashing the app
- Auto update crash (yes, again... sorry I'm dumb sometimes lol)

--------------------------------

# OGE Next Rel-07e76a31

## Changes
- Make the missing data obvious so there's no confusion about what's happening (OGE being weird as always)

--------------------------------

# OGE Next Rel-07e76a29

## Fix
- Updater fix v2 (sorry about that)
- Average being null

--------------------------------

# OGE Next Rel-07e755f6

## Changes
- Speed up the scrollbar animation duration
- Optimized settings reload
- Added cache so the next time you open the app, all your semester minus the last one are already loaded (also made possible the loading of the last semester just after the login screen)

## Fix
- OGE weirdness: when you get a new invisible grade, the website doesn't add the coefficient to the subject
- Updater was not set correctly (you need to download this version manually but this one and the next ones should update automatically)

--------------------------------

# OGE Next Rel-07e7557b

First release of OGE Next ! 🥳
