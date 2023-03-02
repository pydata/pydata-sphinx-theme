==============
Source Buttons
==============

Source buttons are links to the source of your page's content (either on your site, or on hosting sites like GitHub).

Add an edit button
==================

You can add a button to each page that will allow users to edit the page text
directly and submit a pull request to update the documentation. To include this
button in the secondary sidebar of each page, add the following configuration to
your ``conf.py`` file in 'html_theme_options':

.. code:: python

   html_theme_options = {
       "use_edit_page_button": True,
   }

A number of providers are available for building *Edit this Page* links, including
GitHub, GitLab, and Bitbucket. For each, the default public instance URL can be
replaced with a self-hosted instance.


GitHub
------

.. code:: python

   html_context = {
       # "github_url": "https://github.com", # or your GitHub Enterprise site
       "github_user": "<your-github-org>",
       "github_repo": "<your-github-repo>",
       "github_version": "<your-branch>",
       "doc_path": "<path-from-root-to-your-docs>",
   }


GitLab
------

.. code:: python

   html_context = {
       # "gitlab_url": "https://gitlab.com", # or your self-hosted GitLab
       "gitlab_user": "<your-gitlab-org>",
       "gitlab_repo": "<your-gitlab-repo>",
       "gitlab_version": "<your-branch>",
       "doc_path": "<path-from-root-to-your-docs>",
   }


Bitbucket
---------

.. code:: python

   html_context = {
       # "bitbucket_url": "https://bitbucket.org", # or your self-hosted Bitbucket
       "bitbucket_user": "<your-bitbucket-org>",
       "bitbucket_repo": "<your-bitbucket-repo>",
       "bitbucket_version": "<your-branch>",
       "doc_path": "<path-from-root-to-your-docs>",
   }


Custom Edit URL
---------------

For a fully-customized *Edit this Page* URL, provide ``edit_page_url_template``,
a jinja2 template string which must contain ``{{ file_name }}``, and may reference
any other context values.

.. code:: python

   html_context = {
       "edit_page_url_template": "{{ my_vcs_site }}{{ file_name }}{{ some_other_arg }}",
       "my_vcs_site": "https://example.com",
       "some_other_arg": "?some-other-arg"
   }

With the predefined providers, the link text reads "Edit on GitHub/GitLab/Bitbucket".
By default, a simple "Edit" is used if you use a custom URL. However, you can set
a provider name like this:

.. code:: python

   html_context = {
       "edit_page_url_template": "...",
       "edit_page_provider_name": "Provider",
   }

This will turn the link into "Edit on Provider".


Custom link text
----------------

You can change the default text by extending the ``edit-this-page.html``
template. For example, if you have ``templates_path = ["_templates"]``
in your Sphinx configuration, you could put this code in
`_templates/edit-this-page.html`:

.. code:: html+jinja

   {% extends "!components/edit-this-page.html" %}

   {% block edit_this_page_text %}
     Edit this page
   {% endblock %}


View Source link
================

By default, this theme adds a button link to view the source of a page (i.e., the underlying ``reStructuredText`` or ``MyST Markdown`` for the page).
To disable it, use the following configuration:


.. code-block:: python

    html_show_sourcelink = False
