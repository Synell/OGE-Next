# [07e86a83] - 2024-05-16

## Fix
- Fixed a bug where the app would not load the semester widget if the data is outdated (Issue #20)

--------------------------------

# [07e85508] - 2024-04-01

## Changes
- Semester names now have the years in them
- Changelog window has been redesigned to be more readable

## Fix
- Fixed a bug where the semester name was incorrect for some users (Issue #18)
- Fixed the tooltip style not being applied to some tooltips (Issue #19)

## Security
- Bump cryptography from **42.0.0** to **42.0.4** (Pull Request #17)

--------------------------------

# [07e815bd] - 2024-01-23

## New
- Ranks, names and dates are now displayed when you hover a grade (Feature #14)
- Ranks, names and dates are loaded for new grades (Feature #14)
- Added a new setting to refresh the ranks, names and dates of all grades; *Useful if you want to see the ranks, names and dates of grades you already had before this update* (Feature #14)
- What's New window is now displayed when you open the app after an update
- Logout button is now accessible from the "i" button in the top left corner of the sidebar (Feature #13)

## Security
- Bump cryptography from **41.0.3** to **41.0.6** (Pull Request #6)

## Changes
- Updated the tooltip system so it's more customizable, instantaneous when hovering, and more consistent with the rest of the app

## Fix
- Fixed a bug where a "?" was displayed instead of the grade when the grade was 0 (Issue #10)

--------------------------------

# [07e7e910] - 2023-11-03

## Fix
- Fixed a bug where the api wasn't working when at a grade value was null

--------------------------------

# [07e7bfac] - 2023-09-21

## Fix
- Fixed a bug where the api wasn't working when at least one of the subject coeff was empty like this: "Subject Name ()"

--------------------------------

# [07e7bf10] - 2023-09-02

## Technical Changes
- Language file system update
- Added various QSS file parameters for managing colors

## Fix
- Fixed a bug where the api wasn't working when at least one of the pole coeff was empty like this: "Pole Name ()"
- Applying a setting no longer shows a reload warning message if the edited setting(s) didn't require a reload to be applied

--------------------------------

# [07e77fd5] - 2023-06-26

## Changes
- Made every color transition of each UE table round
- Added the possibility to reduce each UE table for easy average view
- Added the possibility to reduce the top new grade panel for easy access to the tables below it

## Fix
- Fixed a visual bug: the bottom of each UE table wasn't perfectly round
- "Report a bug" button wasn't working as it should (it was the link for App Manager instead of OGE Next)

--------------------------------

# [07e77fc5] - 2023-06-24

## Changes
- Added a "report a bug" action (Feature #9)

## Fix
- Fixed a visual bug (new grades, top display)

--------------------------------

# [07e77fb4] - 2023-06-22

## Changes
- Added a preview of the new grades at the very top of the grades screen

--------------------------------

# [07e77f83] - 2023-06-16

## New
- Added an icon next to new grades (Feature #8)
- Added a message at the top of the widget saying how many grades are new (Feature #8)

--------------------------------

# [07e77f6a] - 2023-06-13

## Changes
- Added a log folder for the log files of the main application and for the errors and warnings from the api

## Fix
- Fixed empty poles with no coefficient crashing the app
- Fixed empty subjects with no coefficient crashing the app
- Fixed empty grade groups with no coefficient crashing the app
- Auto update crash (yes, again... sorry I'm dumb sometimes lol)

--------------------------------

# [07e76a31] - 2023-05-06

## Changes
- Make the missing data obvious so there's no confusion about what's happening; ~~OGE being weird as always~~ (Issue #7)

--------------------------------

# [07e76a29] - 2023-05-05

## Fix
- Updater fix v2 (sorry about that)
- Average being null

--------------------------------

# [07e755f6] - 2023-04-30

## Changes
- Speed up the scrollbar animation duration
- Optimized settings reload
- Added cache so the next time you open the app, all your semester minus the last one are already loaded (also made possible the loading of the last semester just after the login screen)

## Fix
- OGE weirdness: when you get a new invisible grade, the website doesn't add the coefficient to the subject
- Updater was not set correctly (you need to download this version manually but this one and the next ones should update automatically)

--------------------------------

# [07e7557b] - 2023-04-15

## New
- First release of OGE Next ! 🥳
