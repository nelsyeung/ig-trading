{{ name | escape | underline }}

.. automodule:: {{ fullname }}

   {% block attributes %}
   {% if attributes %}
   {{ _('Module Attributes') }}
   ----------------------------

   {% for item in attributes %}

   .. autodata:: {{ item }}

   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block functions %}
   {% if functions %}
   {{ _('Functions') }}
   --------------------

   {% for item in functions %}

   .. autofunction:: {{ item }}

   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block classes %}
   {% if classes %}
   {{ _('Classes') }}
   ------------------

   {% for item in classes %}

   {% if (fullname, item) in noindex_pairs %}
   {{ item }}
   {{ '~' * item|length }}

   {% endif %}
   .. autoclass:: {{ item }}
      {%- if item not in external_alias_names %}
      :members:
      :special-members: __call__
      {%- endif %}
      :show-inheritance:
      {%- if (fullname, item) in noindex_pairs %}
      :noindex:
      {%- endif %}

   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block exceptions %}
   {% if exceptions %}
   {{ _('Exceptions') }}
   ---------------------

   {% for item in exceptions %}

   {% if (fullname, item) in noindex_pairs %}
   {{ item }}
   {{ '~' * item|length }}

   {% endif %}
   .. autoexception:: {{ item }}
      :members:
      :show-inheritance:
      {%- if (fullname, item) in noindex_pairs %}
      :noindex:
      {%- endif %}

   {%- endfor %}
   {% endif %}
   {% endblock %}

{% block modules %}
{% if modules %}
Modules
-------

.. autosummary::
   :recursive:
   :toctree:
{% for item in modules %}
   {{ item }}

{%- endfor %}
{% endif %}
{% endblock %}
