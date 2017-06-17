# vivo-template-catalog
Getting started to produce a catalog of templates for Vitro and VIVO.

## Expected features

1. Select VIVO or Vitro or both for inclusion in the catalog
1. Catalog produces output suitable for importing to the Confluence wiki (of course we could produce Markdown and put the catalog in the wiki of this repo.  And if Confluence could importa Markdown, all would be glorious).
1. For each template include
    1. Path/name
    1. "tree" -- a depiction of what the template calls and what is called by those things on down to the leafs
    1. language --- an attempt to discern if the template contains hard coded language, or appears to be i18n clean
    1. calls -- how many times is the template called.  Helps us find important templates, and templates we might be able to remove
