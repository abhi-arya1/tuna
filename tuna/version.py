# pylint: disable=line-too-long
"""

Tuna Version Tracking Service

--------------------------------------

Only released versions are tracked here. 
All GitHub Pushes count as a Dev Build.

--------------------------------------


Versioning Guidelines 
---------------------

Write all major versions as: 
----------------------------
"VERSION_MAJOR_MINOR_PATCH = (int) Major.Minor.Patch # MM/DD/YYYY" 

  - Major version "0" is reserved solely for pre-release and initial release builds. 
  - MM/DD/YYYY corresponds to the date of the release.


Write all minor versions as:
----------------------------
"VERSION_MAJOR_MINOR_PATCH = (int) Major.Minor.Patch Dev Build X (<branchname>) # MM/DD/YYYY"
  
  - In this scenario, "X" corresponds to the commit number on the branch.
  - The branch name is included in the version string to help identify the source of the build.
  - MM/DD/YYYY corresponds to the date of the push.
  - If Dev Builds are forgotten, no worries, as long as there is at least one per branch. 
  - On the pre-PR-approval commit, the version should be updated to the latest Major.Minor, with an incremented Patch.

"""

VERSION = "0.2.0 Dev Build 1" # Current Version

LATEST_VERSION = VERSION # Shown when running "tuna [-v | --version]" (via tuna.cli.core.constants.py)

######################################################
# MAJOR VERSIONS
######################################################

VERSION_0_1_5  = "0.1.5" # 07/12/2024
VERSION_0_1_4  = "0.1.4" # 07/10/2024
VERSION_0_1_3  = "0.1.3" # 07/09/2024
VERSION_0_1_2  = "0.1.2" # 07/09/2024
VERSION_0_1_1  = "0.1.1" # 07/08/2024
VERSION_0_1_0  = "0.1.0" # 07/07/2024
VERSION_INIT   = "0.0.1" # 07/06/2024

######################################################
######################################################
######################################################


######################################################
# MINOR VERSIONS
######################################################

VERSION_0_1_4_DEV_4 = "0.1.4 Dev Build 4 (v0.2)" # 07/10/2024
VERSION_0_1_4_DEV_3 = "0.1.4 Dev Build 3 (v0.2)" # 07/10/2024

######################################################
######################################################
######################################################
