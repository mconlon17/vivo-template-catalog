# vivo-template-catalog
Getting started to produce a catalog of templates for Vitro and VIVO.

## Expected features

1. Select VIVO or Vitro or both for inclusion in the catalog
1. Catalog produces output suitable for importing to the Confluence wiki (of course we could produce Markdown and put the catalog in the wiki of this repo.  And if Confluence could importa Markdown, all would be glorious).
1. For each template include
    1. Path/name
    1. "tree" -- a depiction of what the template calls and what is called by those things on down to the leafs
    1. language --- an attempt to discern if the template contains hard coded language, or appears to be i18n clean
    1. i18n count -- how many times does the template refer to i18n.  Helps with translation
    1. called -- how many times is the template called.  Helps us find important templates, and templates we might be able to remove
    1. ncalls -- number of calls to other templates made by this template
    1. calls -- set of templates called by the template
    1. tags -- set of tags used by the template
    
## Running template-catalog

    > python template-catalog.py [theme]

If theme starts with a v it is assumed to be a vitro theme and the "v" is removed.  So to process the vitro theme, 
use vvitro.  The default theme is wilma.

For Vitro themes, the Vitro templates are processed, then the Vitro theme templates, overriding any Vitro templates 
with the same name.

For VIVO themes, the Vitro templates are processed, then the VIVO templates overriding any Vitro templates
of the same name, then the VIVO theme templates are processed, overriding any VIVO or Vitro templates of the
same name.

## Outputs

1. For each template, the information described above
1. A tab separated list of template and tag -- one line for each template/tag combination, sorted by template, then tag
1. A tab separated list of tag and template -- one line for each tag/template combination, sorted by tag, then template


