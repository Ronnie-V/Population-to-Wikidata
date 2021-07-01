# Population-to-Wikidata

This script is meant to update the population numbers for French communities. 
Data can be provided as:
#Year;INSEE-code;Name;Number of inhabitants
1968;1001;L'ABERGEMENT-CLEMENCIAT;347
1975;1001;L'ABERGEMENT-CLEMENCIAT;368

Or as:
#Year;Q-item;Name;Number of inhabitants
1975;Q204388;L'ABERGEMENT-CLEMENCIAT;368

The name is only needed for human interaction.

As the definition of population has changed over time, the script does handle this:
Until 31 December 1954: population totale
Until 31 December 2003: population sans double compte
Since 1 January 2004: population municipale

The script does signal if a number was found for a given date. If so, this will not be changed, but a remark will be shown on the screen.
If the INSEE code can not be found, this will be signaled and a line will be added to a comments file. After adding the missing link (or municipality) to Wikidata, the script can be rerun.
If the INSEE code is not unique, this will be signaled and a line will be added to a comments file. After human interaction, to clearify which Q-item should be used for what year, the script can be rerun.

The script does have a variable, INSEEtoSkip (set in the code) to make it skip all lines with lower or equal INSEE codes, so the script can be run in separate batches. Cutting the source file is also an option.
The script supports a parameter to run the script against another sourcefile, for instance to retry the INSEE codes that where skipped in the first run.
