# moqui.resource

One line per entity. E = entity, V = view-entity. Generated; do not edit.

- E moqui.resource.DbResource | src: moqui-framework | pk: resourceId | fields: parentResourceId:id, filename:text-medium, isFile:text-indicator | rels: one-nofk>DbResourceFile, many>DbResourceFileHistory
- E moqui.resource.DbResourceFile | src: moqui-framework | pk: resourceId | fields: mimeType:text-medium, versionName:text-short, rootVersionName:text-short, fileData:binary-very-long | rels: one>DbResource, many>DbResourceFileHistory
- E moqui.resource.DbResourceFileHistory | src: moqui-framework | pk: resourceId,versionName | fields: previousVersionName:text-short, versionDate:date-time, userId:id, isDiff:text-indicator, fileData:binary-very-long | rels: one>DbResourceFile, one-nofk>UserAccount
- E moqui.resource.wiki.WikiBlog | src: moqui-framework | pk: wikiBlogId | fields: wikiPageId:id, title:text-medium, author:text-medium, summary:text-long, publishDate:date-time, metaKeywords:text-long, metaDescription:text-long, smallImageLocation:text-medium | rels: one>WikiPage, many>WikiBlogCategory
- E moqui.resource.wiki.WikiBlogCategory | src: moqui-framework | pk: wikiPageCategoryId,wikiBlogId | fields: sentDate:date-time | rels: one>WikiPageCategory, one>WikiBlog
- E moqui.resource.wiki.WikiPage | src: moqui-framework | pk: wikiPageId | fields: wikiSpaceId:id, pagePath:text-medium, parentWikiPageId:id, sequenceNum:number-integer, createdByUserId:id, publishedVersionName:text-short, restrictView:text-indicator, restrictUpdate:text-indicator | rels: one>WikiSpace, one-nofk>UserAccount, many>WikiPageHistory, many>WikiPageCategoryMember
- E moqui.resource.wiki.WikiPageAlias | src: moqui-framework | pk: wikiSpaceId,aliasPath | fields: wikiPageId:id | rels: one>WikiSpace, one>WikiPage
- E moqui.resource.wiki.WikiPageCategory | src: moqui-framework | pk: wikiPageCategoryId | fields: categoryName:text-medium | rels: 
- E moqui.resource.wiki.WikiPageCategoryMember | src: moqui-framework | pk: wikiPageCategoryId,wikiPageId | fields: fromDate:date-time, thruDate:date-time | rels: one>WikiPageCategory, one>WikiPage
- E moqui.resource.wiki.WikiPageHistory | src: moqui-framework | pk: wikiPageId,historySeqId | fields: oldPagePath:text-medium, userId:id, changeDateTime:date-time, versionName:text-short | rels: one>WikiPage, one-nofk>UserAccount
- E moqui.resource.wiki.WikiPageUser | src: moqui-framework | pk: wikiPageId,userId | fields: receiveNotifications:text-indicator, allowView:text-indicator, allowUpdate:text-indicator | rels: one>WikiPage, one-nofk>UserAccount
- E moqui.resource.wiki.WikiSpace | src: moqui-framework | pk: wikiSpaceId | fields: description:text-long, rootPageLocation:text-medium, decoratorScreenLocation:text-medium, publicPageUrl:text-medium, publicAttachmentUrl:text-medium, publicBlogUrl:text-medium, restrictView:text-indicator, restrictUpdate:text-indicator, allowAnyHtml:text-indicator, screenThemeId:id | rels: one>ScreenTheme
- E moqui.resource.wiki.WikiSpaceUser | src: moqui-framework | pk: wikiSpaceId,userId | fields: receiveNotifications:text-indicator, allowAdmin:text-indicator, allowView:text-indicator, allowUpdate:text-indicator | rels: one>WikiSpace, one-nofk>UserAccount
- V moqui.resource.wiki.WikiBlogCategoryDetail | src: moqui-framework | members: WKBC=WikiBlogCategory, WPC=rel WKBC:category | alias-all: WKBC,WPC | aliases: 
- V moqui.resource.wiki.WikiBlogFindView | src: moqui-framework | members: WKBG=WikiBlog, WKPG=rel WKBG:page, WKBC=rel WKBG:categories | alias-all: WKBG,WKBC | aliases: wikiSpaceId, parentWikiPageId, publishedVersionName, pagePath
- V moqui.resource.wiki.WikiPageAndUser | src: moqui-framework | members: WKPG=WikiPage, WPU=WikiPageUser? | alias-all: WKPG,WPU | aliases: 
- V moqui.resource.wiki.WikiSpaceAndUser | src: moqui-framework | members: WKSP=WikiSpace, WSU=WikiSpaceUser? | alias-all: WKSP,WSU | aliases: 
