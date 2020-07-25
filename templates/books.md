{% for category, titles in books|groupby('Category') %}
## {{ category }}

{% for title in titles|sort(attribute='Book Title') %}
- [{{ title['Book Title'] }}]({{ title['OpenURL']}}) ({{ title['Edition']}})  
  {{ title['Author']}}
{% endfor %}

{% endfor %}
