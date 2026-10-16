#!/bin/sh
# Regenerate every generated reference of the skills from the component sources.
# Usage: ./rebuild-references.sh /path/to/moqui-framework   (a checkout with runtime/component/* populated)
# Adjust COMPS if your components live elsewhere or you add your own.
set -e
cd "$(dirname "$0")"
FW="$1"; [ -n "$FW" ] || { echo "usage: $0 /path/to/moqui-framework"; exit 1; }
RT="$FW/runtime"; C="$RT/component"
COMPS="$FW/framework $RT/base-component/tools $RT/base-component/webroot $C/mantle-udm $C/mantle-usl \
  $C/SimpleScreens $C/MarbleERP $C/PopCommerce $C/HiveMind $C/moqui-sftp $C/moqui-math $C/moqui-device"
EXISTING=""; for c in $COMPS; do [ -d "$c" ] && EXISTING="$EXISTING $c"; done
S=.agents/skills
python3 $S/moqui-model/scripts/build_model_index.py $S/moqui-model/references $EXISTING
python3 $S/moqui-actions/scripts/build_eca_index.py $S/moqui-actions/references/ecas.md $EXISTING
python3 $S/moqui-actions/scripts/build_actions_reference.py "$FW/framework/xsd/xml-actions-3.xsd" \
  $S/moqui-actions/references/elements.md $EXISTING
python3 $S/moqui-data/scripts/build_data_catalog.py $S/moqui-data/references/data-catalog.md $EXISTING
python3 $S/moqui-datadocument/scripts/build_document_catalog.py $S/moqui-datadocument/references/documents.md $EXISTING
echo "references rebuilt from:$EXISTING"
