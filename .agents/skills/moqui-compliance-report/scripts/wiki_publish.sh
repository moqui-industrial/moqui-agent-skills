#!/bin/bash
# Publish report pages to a Moqui wiki space through the wiki screens (HiveMind / SimpleScreens), as a logged-in user:
# every page update is versioned by the dbresource store and shows in the page history.
#
#   wiki_publish.sh space <spaceId> "<description>"            create a space (id: 3-8 chars, letter first)
#   wiki_publish.sh protect <spaceId> <userId>[,<userId>...]     restrictUpdate=Y, these users may update (no screen
#        manages WikiSpaceUser: loaded through Tools > Entity > Data Import, needs the tools app permission;
#        userId is the UserAccount id, e.g. EX_JOHN_DOE, and is NOT checked: a wrong id silently locks nobody in)
#   wiki_publish.sh page  <spaceId> <pageName> <wikiType> <file> [parentPath]
#        wikiType: md (static Markdown), md.ftl (Markdown, then FreeMarker), html.ftl (FreeMarker only)
#   wiki_publish.sh get   <spaceId> <pagePath> [query]          print the rendered page body as text (check)
#
# env: MOQUI_URL (default http://localhost:8080), MOQUI_AUTH (user:password, default john.doe:moqui)
# The screen transitions need a session and its moquiSessionToken: a form login is done first. A space with
# restrictUpdate=Y also needs a WikiSpaceUser record with allowUpdate=Y for the user.
set -euo pipefail
URL=${MOQUI_URL:-http://localhost:8080}
AUTH=${MOQUI_AUTH:-john.doe:moqui}
JAR=$(mktemp); trap 'rm -f "$JAR"' EXIT
c() { curl -s -c "$JAR" -b "$JAR" "$@"; }
c -o /dev/null "$URL/Login"
c -o /dev/null -X POST "$URL/Login/login" --data-urlencode "username=${AUTH%%:*}" --data-urlencode "password=${AUTH#*:}"
# the token is in any rendered form of the session: the space list to create a space, the space itself otherwise
case "${1:-}" in space) TPAGE=/apps/marble/Wiki/WikiSpaces ;; protect) TPAGE=/apps/tools/Entity/DataImport ;;
  *) TPAGE="/apps/hm/wiki/${2:-}" ;; esac
TOKEN=$(c "$URL$TPAGE" | grep -o 'name="moquiSessionToken" value="[^"]*"' | head -1 | sed 's/.*value="//;s/"$//' || true)
[ -n "$TOKEN" ] || { echo "no session token from $TPAGE: login failed for ${AUTH%%:*}, or the space does not exist" >&2; exit 1; }
post() { local t=$1; shift; c -o /dev/null -w "%{http_code} %{redirect_url}\n" -X POST "$URL$t" --data-urlencode "moquiSessionToken=$TOKEN" "$@"; }
case "${1:-}" in
  space) post /apps/marble/Wiki/WikiSpaces/createSpace --data-urlencode "wikiSpaceId=$2" --data-urlencode "description=$3" ;;
  protect) XML="<entity-facade-xml><moqui.resource.wiki.WikiSpace wikiSpaceId=\"$2\" restrictUpdate=\"Y\"/>"
         for u in ${3//,/ }; do XML="$XML<moqui.resource.wiki.WikiSpaceUser wikiSpaceId=\"$2\" userId=\"$u\" allowView=\"Y\" allowUpdate=\"Y\"/>"; done
         post /apps/tools/Entity/DataImport/load --data-urlencode "xmlText=$XML</entity-facade-xml>" ;;
  page)  post /apps/hm/EditWikiPage/updatePage --data-urlencode "wikiSpaceId=$2" --data-urlencode "pageName=$3" \
              --data-urlencode "wikiType=$4" --data-urlencode "pageText@$5" --data-urlencode "parentPath=${6:-}" ;;
  get)   c "$URL/apps/hm/wiki/$2/$3${4:+?$4}" | python3 -c '
import re, sys
t = sys.stdin.read()
m = re.search(r"<!-- BEGIN section\[@name=WikiPageCommentSect", t)
body = t[:m.start()] if m else t
errs = re.findall(r"(?:FreeMarker template error|Error rendering|TemplateException)[^<]{0,300}", t)
print("\n".join("ERROR: " + e for e in errs))
print(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body))[-4000:])' ;;
  *) sed -n 2,16p "$0"; exit 2 ;;
esac
